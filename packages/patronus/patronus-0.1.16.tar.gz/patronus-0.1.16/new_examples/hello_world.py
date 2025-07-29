from patronus.evals import evaluator, RemoteEvaluator
from patronus.experiments import run_experiment, Row, TaskResult, FuncEvaluatorAdapter


def my_task(row: Row, **kwargs):
    return f"{row.task_input} World"


# Reference remote Judge Patronus Evaluator with is-concise criteria.
# This evaluator runs remotely on Patronus infrastructure.
is_concise = RemoteEvaluator("judge", "patronus:is-concise")


@evaluator()
def exact_match(row: Row, task_result: TaskResult, **kwargs):
    print(f"{task_result.output=}  :: {row.task_output=}")
    return task_result.output == row.task_output


result = run_experiment(
    project_name="Tutorial Project",
    dataset=[
        {
            "task_input": "Hello",
            "gold_answer": "Hello World",
        },
    ],
    task=my_task,
    evaluators=[is_concise, FuncEvaluatorAdapter(exact_match)],
)

result.to_csv("./experiment.csv")
