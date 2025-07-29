from patronus import evaluator
from patronus.experiments import FuncEvaluatorAdapter, run_experiment
from patronus.datasets import Row


@evaluator()
def exact_match(row: Row, **kwargs):
    return row.task_output == row.gold_answer


adapter = FuncEvaluatorAdapter(exact_match)

run_experiment(
    dataset=[{"task_output": "string", "gold_answer": "string"}], evaluators=[adapter]
)
