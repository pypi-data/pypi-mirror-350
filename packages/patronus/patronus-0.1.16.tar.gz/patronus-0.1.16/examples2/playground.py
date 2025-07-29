import logging

import asyncio
import random
import threading
import time
import typing
from opentelemetry.trace import get_current_span
from typing import Optional, Union

import patronus
from patronus import evals, traced, EvaluationResult, StructuredEvaluator, AsyncStructuredEvaluator
from patronus.evals import bundled_eval

patronus.init()
log = patronus.get_logger()
log.addHandler(logging.StreamHandler())


EVALUATOR = "judge"
CRITERIA = "patronus:fuzzy-match"
# EVALUATOR = "dummy-local-1"
# CRITERIA = "patronus:fifty-fifty"


@evals.evaluator()
def scorer_a(x: int, y: int):
    span = get_current_span()
    print(f"scorer a, current span: {span}")
    time.sleep(random.random() / 10)
    return x == y


@evals.evaluator()
async def scorer_b(x: int, y: int):
    await asyncio.sleep(random.random() / 10)
    return x**2 == y


class ClassScorer(evals.Evaluator):
    def evaluate(self, x: int, y: int) -> Optional[EvaluationResult]:
        time.sleep(random.random() / 10)
        return EvaluationResult(pass_=x == y)


@patronus.traced()
async def main():
    x, y = 2, 4

    class_scorer = ClassScorer()

    with evals.evaluators.bundled_eval():
        await asyncio.gather(
            asyncio.to_thread(scorer_a, x, y),
            scorer_b(x, y),
            asyncio.to_thread(class_scorer.evaluate, x, y),
        )


@patronus.traced()
def threaded_workflow():
    x, y = 2, 4
    class_scorer = ClassScorer()

    with evals.evaluators.bundled_eval():
        t1 = threading.Thread(target=scorer_a, args=(x, y))
        t2 = threading.Thread(target=scorer_a, args=(x, y))
        t3 = threading.Thread(target=class_scorer.evaluate, args=(x, y))
        t1.start(), t2.start(), t3.start()
        t1.join(), t2.join(), t3.join()

    print("Done.")


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
        **kwargs: typing.Any,
    ) -> EvaluationResult:
        time.sleep(random.random())
        try:
            return EvaluationResult(pass_=task_output.lower().strip() == gold_answer.lower().strip())
        finally:
            print("IExactMatch finished.")


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
        **kwargs: typing.Any,
    ) -> EvaluationResult:
        time.sleep(random.random())
        try:
            return EvaluationResult(pass_=task_output == gold_answer)
        finally:
            print("ExactMatch finished.")


class AsyncExactMatch(AsyncStructuredEvaluator):
    async def evaluate(
        self,
        *,
        system_prompt: Optional[str] = None,
        task_context: Union[list[str], str, None] = None,
        task_input: Optional[str] = None,
        task_output: Optional[str] = None,
        gold_answer: Optional[str] = None,
        task_metadata: Optional[typing.Dict[str, typing.Any]] = None,
        **kwargs: typing.Any,
    ) -> EvaluationResult:
        await asyncio.sleep(random.random())
        try:
            return EvaluationResult(pass_=task_output == gold_answer)
        finally:
            print(f"{self.__class__.__qualname__} finished.")


iexact_match = IExactMatch()
exact_match = ExactMatch()
async_exact_match = AsyncExactMatch()


@traced()
def raiser():
    time.sleep(random.random() / 10)
    raise Exception("Hello exception")


@traced()
def oneoff():
    score = scorer_a(1, 2)
    print(score)
    try:
        raiser()
    except Exception:
        pass


@patronus.traced()
def pat_cli_workflow():
    pc = patronus.pat_client.Patronus(workers=4)
    with bundled_eval():
        iexact_match.evaluate(task_output="hello world\t", gold_answer="Hello World")
        exact_match.evaluate(task_output="hello world\t", gold_answer="Hello World")
    res = pc.evaluate(
        evaluators=[iexact_match, exact_match],
        task_output="hello world\t",
        gold_answer="Hello World",
    )
    print(res)


@traced()
def workflow_in_bg():
    with patronus.pat_client.Patronus(shutdown_on_exit=False) as pc:
        resp = pc.evaluate_bg(
            evaluators=[iexact_match, exact_match],
            task_output="hello world\t",
            gold_answer="Hello World",
        )
        evals = resp.get()
        evals.raise_on_exception()
        print(f"all succeeded: {evals.all_succeeded()}")
        print(f"any failed: {evals.any_failed()}")
        print(f"Succeeded evals: {list(evals.succeeded_evaluations())}")
        print(f"Failed evals: {list(evals.failed_evaluations())}")


@traced()
async def workflow_async_cli():
    patronus.get_logger().info("Staring workflow...")
    await async_exact_match.evaluate(task_output="hello world\t", gold_answer="Hello World")
    async with patronus.pat_client.AsyncPatronus(2) as pc:
        resp = await pc.evaluate(
            evaluators=[async_exact_match, exact_match, iexact_match, async_exact_match, iexact_match],
            task_output="hello world\t",
            gold_answer="Hello World",
        )
    print(resp)


@traced()
async def workflow_async_cli_bg():
    pc = patronus.pat_client.AsyncPatronus()
    resp = pc.evaluate_bg(
        evaluators=[async_exact_match, exact_match, iexact_match],
        task_output="hello world\t",
        gold_answer="Hello World",
    )
    await pc.close()


@traced()
def workflow_remote_eval():
    ev = evals.evaluators.RemoteEvaluator(EVALUATOR, CRITERIA)
    resp = ev.evaluate(task_output="hello world\t", gold_answer="Hello World")
    with patronus.pat_client.Patronus(2) as pc:
        pc.evaluate_bg(evaluators=[ev, ev, ev], task_output="hello world\t", gold_answer="Hello World")
    print("Response")
    print("========")
    print(resp)


@traced()
async def workflow_remote_eval_async():
    ev = evals.evaluators.AsyncRemoteEvaluator(EVALUATOR, CRITERIA)
    # resp = await ev.evaluate(task_output="hello world\t", gold_answer="Hello World")
    async with patronus.pat_client.AsyncPatronus(2) as pc:
        pc.evaluate_bg(evaluators=[ev, ev, ev, iexact_match], task_output="hello world\t", gold_answer="Hello World")
    print("Response")
    print("========")
    # print(resp)


@traced()
async def complete_anthropic():
    await asyncio.sleep(random.random())
    await asyncio.sleep(random.random())
    await asyncio.sleep(random.random())
    log.info("complete_anthropic finished.")


@traced()
async def complete():
    await complete_anthropic()
    await asyncio.sleep(random.random())
    log.info("complete finished.")
    scorer_a(1, 2)


def in_worker():
    asyncio.run(complete())


@traced()
async def agent_workflow():
    await complete()
    await asyncio.sleep(random.random())
    log.info("agent_workflow finished.")


if __name__ == "__main__":
    oneoff()
    asyncio.run(main())
    threaded_workflow()
    pat_cli_workflow()
    workflow_in_bg()
    asyncio.run(workflow_async_cli())
    asyncio.run(workflow_async_cli_bg())
    workflow_remote_eval()
    asyncio.run(workflow_remote_eval_async())
    asyncio.run(agent_workflow())
