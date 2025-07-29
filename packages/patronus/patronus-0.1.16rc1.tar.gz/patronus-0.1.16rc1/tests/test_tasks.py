import patronus
from patronus.datasets import Row


def test_non_parametrized_task_decorator_use():
    @patronus.task
    def identity_task(row: Row):
        return row.task_input

    assert identity_task.name == "identity_task"


def test_parametrized_task_decorator_use():
    task_name = "identity"

    @patronus.task(name=task_name)
    def _my_task(row: Row):
        return row.task_input

    assert _my_task.name == task_name
