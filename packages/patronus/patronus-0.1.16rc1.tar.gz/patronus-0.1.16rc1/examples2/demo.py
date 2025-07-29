import typing

from typing import Optional, Union, Any

import asyncio

import random

import time

from patronus import init, Patronus, AsyncPatronus, traced
from patronus.evals import evaluator, StructuredEvaluator, AsyncStructuredEvaluator, bundled_eval, EvaluationResult

init()


@evaluator()
def exact_match(output: str, gold_answer: str):
    time.sleep(random.random() / 20)
    return gold_answer == output


@evaluator()
def iexact_match(output: str, gold_answer: str):
    time.sleep(random.random() / 10)
    return gold_answer.strip().lower() == output.strip().lower()


@evaluator()
async def a_exact_match(output: str, gold_answer: str):
    await asyncio.sleep(random.random() / 20)
    return gold_answer == output


@evaluator()
async def a_iexact_match(output: str, gold_answer: str):
    await asyncio.sleep(random.random() / 10)
    return gold_answer.strip().lower() == output.strip().lower()


@evaluator()
async def a_iexact_match2(output: str, gold_answer: str, x: int):
    await asyncio.sleep(random.random() / 10)
    return gold_answer.strip().lower() == output.strip().lower()


task_output = " Hello world\t"
gold_answer = "Hello World"


@traced()
def workflow_sync_eval():
    exact_match(task_output, gold_answer)
    iexact_match(task_output, gold_answer)


@traced()
def workflow_bundled_eval():
    with bundled_eval():
        exact_match(task_output, gold_answer)
        iexact_match(task_output, gold_answer)


@traced()
async def workflow_bundled_eval_async():
    with bundled_eval():
        await asyncio.gather(
            a_exact_match(task_output, gold_answer),
            a_iexact_match(task_output, gold_answer),
            a_iexact_match2(task_output, gold_answer, 10),
        )


class ExactMatch(StructuredEvaluator):
    def evaluate(
        self,
        *,
        system_prompt: Optional[str] = None,
        task_context: Union[list[str], str, None] = None,
        task_input: Optional[str] = None,
        task_output: Optional[str] = None,
        gold_answer: Optional[str] = None,
        task_metadata: Optional[typing.Dict[str, typing.Any]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        time.sleep(random.random() / 20)
        try:
            return EvaluationResult(pass_=task_output == gold_answer)
        finally:
            print("Finished iexact match")


class IExactMatch(StructuredEvaluator):
    def evaluate(
        self,
        *,
        system_prompt: Optional[str] = None,
        task_context: Union[list[str], str, None] = None,
        task_input: Optional[str] = None,
        task_output: Optional[str] = None,
        gold_answer: Optional[str] = None,
        task_metadata: Optional[typing.Dict[str, typing.Any]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        time.sleep(random.random() / 20)
        try:
            return EvaluationResult(pass_=task_output.strip().lower() == gold_answer.strip().lower())
        finally:
            print("Finished iexact match")


class AsyncIExactMatch(AsyncStructuredEvaluator):
    async def evaluate(
        self,
        *,
        system_prompt: Optional[str] = None,
        task_context: Union[list[str], str, None] = None,
        task_input: Optional[str] = None,
        task_output: Optional[str] = None,
        gold_answer: Optional[str] = None,
        task_metadata: Optional[typing.Dict[str, typing.Any]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        await asyncio.sleep(random.random() / 20)
        try:
            return EvaluationResult(pass_=task_output.strip().lower() == gold_answer.strip().lower())
        finally:
            print("Finished iexact match")


@traced()
def structured_workflow():
    class_exact_match_eval = ExactMatch()
    class_iexact_match_eval = IExactMatch()

    cli = Patronus()
    cli.evaluate_bg(
        evaluators=[class_exact_match_eval, class_iexact_match_eval],
        task_output=task_output,
        gold_answer=gold_answer,
    )


@traced()
async def structured_workflow_async():
    class_exact_match_eval = ExactMatch()
    class_iexact_match_eval = IExactMatch()
    class_async_imatch = AsyncIExactMatch()

    async with AsyncPatronus(max_workers=2) as cli:
        cli.evaluate_bg(
            evaluators=[
                class_exact_match_eval,
                class_iexact_match_eval,
                class_async_imatch,
                class_exact_match_eval,
                class_iexact_match_eval,
            ],
            task_output=task_output,
            gold_answer=gold_answer,
        )


if __name__ == "__main__":
    #
    # workflow_sync_eval()
    # workflow_bundled_eval()
    # asyncio.run(workflow_bundled_eval_async())
    # structured_workflow()
    asyncio.run(structured_workflow_async())
