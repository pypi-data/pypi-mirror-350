import abc
import typing

import patronus


class EvaluationResult(pydantic.BaseModel):
    pass_: Optional[bool] = pydantic.Field(default=False, serialization_alias="pass")
    score: Optional[float] = None
    text_output: Optional[str] = None
    metadata: Optional[dict[str, typing.Any]] = None
    explanation: Optional[str] = None
    tags: Optional[dict[str, str]] = None

    evaluation_duration_s: Optional[float] = None
    explanation_duration_s: Optional[float] = None


# bool -> pass_, score=[0, 1]
# number -> score
# text -> text_output


@patronus.evaluator
def my_eval(a, b, c) -> bool:
    return a + b + c == 17


@patronus.evaluator
def my_eval2(a, b, c) -> EvaluationResult:
    return EvaluationResult(
        pass_=False,
        score=0.25,
        text_output="Poor",
        metadata={
            "judge_model": "gpt-4o",
        },
    )


class Evaluator(abc.ABC):
    @abc.abstractmethod
    def evaluate(
        self,
        system_prompt,
        task_context,
        task_input,
        task_output,
        gold_answer,
        attachments,
    ) -> typing.Union[
        typing.Optional[EvaluationResult],
        typing.Awaitable[typing.Optional[EvaluationResult]],
    ]: ...


class MyEval2(patronus.Evaluator):
    async def evaluate(self, task_output, gold_answer, **kwargs): ...


cli = patronus.Client()

cli.register_local_evaluator("my-eval2", MyEval2)


def main():
    resp = call_llm()

    # my_eval(1, 2, 3)

    cli.evaluate(
        evaluators=[
            my_eval,
            "my-eval2",
            ("judge", "is-code"),
            ("glider"),
        ],
        system_prompt=...,
        task_context=...,
        task_input=...,
        task_output=...,
        gold_answer=...,
        attachments=...,
    )

    output = my_eval(resp.a, resp.b, resp.c)
