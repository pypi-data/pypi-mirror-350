import asyncio
import random
import typing
from typing import Optional

from patronus import datasets
from patronus.evals import EvaluationResult, AsyncEvaluator
from patronus.experiments import run_experiment
from patronus.experiments.adapters import EvaluatorAdapter
from patronus.experiments.types import TaskResult, EvalParent


class MatchEvaluator(AsyncEvaluator):
    def __init__(self, sanitizer=None):
        if sanitizer is None:
            sanitizer = lambda x: x
        self.sanitizer = sanitizer

    async def evaluate(self, actual: str, expected: str) -> EvaluationResult:
        await asyncio.sleep(random.random())
        matched = self.sanitizer(actual) == self.sanitizer(expected)
        return EvaluationResult(pass_=matched, score=int(matched))


exact_match = MatchEvaluator()
fuzzy_match = MatchEvaluator(lambda x: x.strip().lower())


class MatchAdapter(EvaluatorAdapter):
    def __init__(self, evaluator: MatchEvaluator):
        super().__init__(evaluator)

    def transform(
        self,
        row: datasets.Row,
        task_result: Optional[TaskResult],
        parent: EvalParent,
        **kwargs
    ) -> tuple[list[typing.Any], dict[str, typing.Any]]:
        args = [row.task_output, row.gold_answer]
        kwargs = {}
        # Passing arguments via kwargs would also work in this case.
        # kwargs = {"actual": row.task_output, "expected": row.gold_answer}
        return args, kwargs


run_experiment(
    dataset=[{"task_output": "string\t", "gold_answer": "string"}],
    evaluators=[MatchAdapter(exact_match), MatchAdapter(fuzzy_match)],
)
