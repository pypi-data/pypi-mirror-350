import patronus
from patronus.datasets import Row
from patronus.types import _EvalParent, TaskResult

cli = patronus.Client()


@patronus.task
def task_one(row):
    return f"Hello {row.evaluated_model_input}"


@patronus.evaluator
def eval_one(row: Row, task_result: TaskResult):
    return task_result.evaluated_model_output == row.gold_answer


@patronus.task
def task_two(parent: _EvalParent) -> TaskResult:
    return TaskResult(evaluated_model_output=f"{parent.task.evaluated_model_output}!")


@patronus.evaluator
def eval_two(evaluated_model_output: str, row: Row):
    return evaluated_model_output == row.gold_answer


dataset = [{"evaluated_model_input": "Adam", "evaluated_model_gold_answer": "Hello Adam!"}]

dummy_eval = cli.remote_evaluator("dummy")

cli.experiment(
    "foo",
    dataset=dataset,
    chain=[
        {"task": task_one, "evaluators": [eval_one, dummy_eval]},
        {"task": task_two, "evaluators": [eval_two, dummy_eval]},
    ],
)
#
# async def main():
#     res = await dummy_eval.evaluate(evaluated_model_output="????")
#     print(res)
#
# run_until_complete(main())
