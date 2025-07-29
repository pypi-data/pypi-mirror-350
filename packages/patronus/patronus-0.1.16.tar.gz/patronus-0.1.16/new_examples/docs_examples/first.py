# https://docs.patronus.ai/docs/tutorials/evals/function_based
import typing

from typing import Optional, Union, Any
from patronus import EvaluationResult
from patronus.evals import evaluator, StructuredEvaluator, RemoteEvaluator
from patronus.datasets import Row
from patronus.experiments.experiment import run_experiment


class IExactMatch(StructuredEvaluator):

    def evaluate(
        self,
        *,
        task_output: Optional[str] = None,
        gold_answer: Optional[str] = None,
        **falafele: Any
    ) -> EvaluationResult:
        passed = task_output.lower().strip() == gold_answer.lower().strip()
        return EvaluationResult(pass_=passed, score=int(passed))


run_experiment(
    dataset=[
        {
            "task_input": "Translate 'Good night' to French.",
            "task_output": "bonne nuit",
            "gold_answer": "Bonne nuit",
        },
        {
            "task_input": "Summarize: 'AI improves efficiency'.",
            "task_output": "ai improves efficiency",
            "gold_answer": "AI improves efficiency",
        },
    ],
    evaluators=[IExactMatch(), RemoteEvaluator("judge", "patronus:fuzzy-match")],
    experiment_name="Case Insensitive Match",
)
