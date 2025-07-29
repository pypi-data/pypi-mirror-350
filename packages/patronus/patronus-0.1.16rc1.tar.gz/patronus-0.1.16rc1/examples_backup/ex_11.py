import patronus


cli = patronus.Client()

dataset = [
    {
        "evaluated_model_input": "1",
    },
    {
        "evaluated_model_input": "2",
    },
]


@patronus.task
def identity_task(row):
    return row.evaluated_model_input


@patronus.evaluator
def is_odd(task_result: patronus.TaskResult):
    return int(task_result.evaluated_model_output) % 2 == 1


@patronus.task
def stringify(parent: patronus.EvalParent):
    if parent.evals[is_odd].pass_:
        return "odd"
    else:
        return parent.task.evaluated_model_output


@patronus.evaluator
def is_number(task_result: patronus.TaskResult):
    try:
        int(task_result.evaluated_model_output)
        return True
    except ValueError:
        return False


ex = cli.experiment(
    "protego-dev",
    dataset=dataset,
    chain=[
        {"task": identity_task, "evaluators": [is_odd]},
        {"task": stringify, "evaluators": [is_number]},
    ],
)
df = ex.to_dataframe()
print(df)

df.to_csv("ex11.df.csv")
