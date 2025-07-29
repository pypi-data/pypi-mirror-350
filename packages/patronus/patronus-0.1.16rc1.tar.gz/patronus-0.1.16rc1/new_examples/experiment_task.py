import random

import time

import typing

from typing import Optional, Union, Any

import logging
import openai

from patronus import datasets, EvaluationResult
from patronus.evals import RemoteEvaluator, StructuredEvaluator
from patronus.experiments.experiment import run_experiment, Task
from patronus.experiments.types import EvalParent, TaskResult

oai = openai.OpenAI()

logging.getLogger("patronus").addHandler(logging.StreamHandler())

dataset = [
    {"sid": "f14", "task_input": "Say hello :)", "tags": """{"from_dataset": "true"}"""}
]

# EVALUATOR = "dummy-local-1"
# CRITERIA = "patronus:fifty-fifty"
# is_polite_evaluator = RemoteEvaluator(EVALUATOR, CRITERIA)
is_polite_evaluator = RemoteEvaluator("judge", "patronus:is-polite")


class DummyEvaluator(StructuredEvaluator):

    def evaluate(
        self,
        *,
        system_prompt: Optional[str] = None,
        task_context: Union[list[str], str, None] = None,
        task_attachments: Union[list[Any], None] = None,
        task_input: Optional[str] = None,
        task_output: Optional[str] = None,
        gold_answer: Optional[str] = None,
        task_metadata: Optional[typing.Dict[str, typing.Any]] = None,
        **kwargs: Any
    ) -> EvaluationResult:
        time.sleep(1)
        r = random.random()
        passed = r > 0.5
        return EvaluationResult(pass_=passed, score=r)


def answer(row: datasets.Row, **kwargs) -> TaskResult:
    return TaskResult(
        output="Hello! :) How can I assist you today?",
        tags={"task": "answer"},
    )
    # resp = oai.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #     {
    #         "role": "user",
    #         "content": row.task_input,
    #     }
    # ])
    # return resp.choices[0].message.content


def answer_impolite(row, parent: EvalParent, tags) -> str:
    resp = oai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer in impolite manner."},
            {
                "role": "user",
                "content": parent.task.output,
            },
        ],
    )
    return TaskResult(
        output=resp.choices[0].message.content,
        tags={
            "task": "answer_impolite",
            "model": "gpt-4o-mini",
        },
    )


ex = run_experiment(
    dataset=dataset,
    chain=[
        {
            "task": answer,
            "evaluators": [is_polite_evaluator, DummyEvaluator()],
        },
        {
            "task": answer_impolite,
            "evaluators": [is_polite_evaluator, DummyEvaluator()],
        },
    ],
    tags={
        "foo": "bar",
    },
)

ex.to_csv("./out.csv")