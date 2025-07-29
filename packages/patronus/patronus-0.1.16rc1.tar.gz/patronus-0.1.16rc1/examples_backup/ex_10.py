import logging
import typing

from openai import OpenAI

import patronus
from patronus.evaluators_remote import EvaluateCall

cli = patronus.Client()
oai = OpenAI()

dataset = [
    {
        "model": "gpt-4o-mini",
        "input": (
            "Write a hello world in Python language. "
            "Make sure that the output is a valid python code. "
            "The python cannot be a pythonic, well written code. "
            "It should be done in very unpythonic way."
        ),
    },
    {
        "model": "gpt-4o",
        "input": "Write hello world in Java",
    },
]


@patronus.task
def call_llm(row: patronus.Row) -> patronus.TaskResult:
    model_output = (
        oai.chat.completions.create(
            model=row.model,
            messages=[
                {"role": "user", "content": row.input},
            ],
            temperature=0,
        )
        .choices[0]
        .message.content
    )
    return patronus.TaskResult(
        evaluated_model_output=model_output,
        metadata={"model": row.model},
        tags={"model": row.model},
    )


base_eval_python_code = cli.remote_evaluator(
    "custom-small",
    criteria="is-python-code",
    criteria_config={"pass_criteria": """The MODEL OUTPUT should be a valid python code."""},
)


@base_eval_python_code.wrap
def eval_python_code(evaluate: EvaluateCall, row, task_result: patronus.TaskResult, **kwargs):
    return evaluate(
        evaluated_model_input=row.input,
        evaluated_model_output=task_result.evaluated_model_output,
    )


is_python_code = cli.remote_evaluator(
    "judge",
    criteria="is-pythonic",
    criteria_config={"pass_criteria": """The MODEL OUTPUT should be pythonic code."""},
)


@is_python_code.warp
async def is_idiomatic_python(evaluate, row: patronus.Row, parent: patronus.EvalParent, experiment_id):
    if not parent:
        return None
    if (e := parent.find_eval_result(eval_python_code)) is not None and e.pass_ is False:
        return None

    return await evaluate(
        evaluated_model_input=row.evaluated_model_input,
        evaluated_model_output=parent.task.evaluated_model_output,
        experiment_id=experiment_id,
    )


@patronus.task
def make_code_pythonic(row, parent: patronus.EvalParent) -> typing.Optional[patronus.TaskResult]:
    if not parent or not parent.parent:
        return None

    model_output = (
        oai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Given the piece of code make sure it's written idiomatically in given language.",
                },
                {"role": "user", "content": parent.parent.task.evaluated_model_output},
            ],
            temperature=0,
        )
        .choices[0]
        .message.content
    )
    return model_output


ex = cli.experiment(
    "protego-dev",
    dataset=dataset,
    chain=[
        {"task": call_llm, "evaluators": [eval_python_code]},
        {"task": ..., "evaluators": [is_idiomatic_python]},
    ],
)

df = ex.to_dataframe()

df.to_csv("./demo.csv")
