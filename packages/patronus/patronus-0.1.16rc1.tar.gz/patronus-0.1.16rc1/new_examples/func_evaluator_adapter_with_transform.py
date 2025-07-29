from typing import Optional

import typing

from patronus import evaluator, datasets
from patronus.experiments import FuncEvaluatorAdapter, run_experiment
from patronus.experiments.types import TaskResult, EvalParent


@evaluator()
def exact_match(actual, expected):
    return actual == expected


class AdaptedExactMatch(FuncEvaluatorAdapter):
    def __init__(self):
        super().__init__(exact_match)

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
    dataset=[{"task_output": "string", "gold_answer": "string"}],
    evaluators=[AdaptedExactMatch()],
)
