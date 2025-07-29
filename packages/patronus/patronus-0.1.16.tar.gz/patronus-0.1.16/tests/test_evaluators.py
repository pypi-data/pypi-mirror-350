import patronus
from patronus.datasets import Row


def test_non_parametrized_evaluator_decorator_use():
    @patronus.evaluator
    def ematch(row: Row):
        return row.task_input == row.task_output

    assert ematch.display_name() == "ematch"


def test_parametrized_evaluator_decorator_use():
    eval_name, profile_name = "my-evaluator", "profile1"

    @patronus.evaluator(name=eval_name, criteria=profile_name)
    def ematch(row: Row):
        return row.task_input == row.task_output

    assert ematch.display_name() == f"{eval_name}:{profile_name}"
