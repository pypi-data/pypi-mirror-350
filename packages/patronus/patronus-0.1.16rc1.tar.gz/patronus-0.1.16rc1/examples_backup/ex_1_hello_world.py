import random
import time

import patronus
from patronus import Client, task, Row, TaskResult

client = Client()


@task
def my_task(row: Row):
    time.sleep(random.random())
    if row.sid == 4:
        return 123
    return f"{row.evaluated_model_input} World"


@patronus.evaluator
def exact_match(row: Row, task_result: TaskResult):
    time.sleep(random.random())
    return task_result.evaluated_model_output == row.evaluated_model_gold_answer


ex = client.experiment(
    "Hello World",
    dataset=[
        {
            "evaluated_model_input": "Hello",
            "evaluated_model_retrieved_context": "Hello",
            "evaluated_model_gold_answer": "Hello World",
        },
        {
            "evaluated_model_input": "Hello",
            "evaluated_model_retrieved_context": ["Hello", "World"],
            "evaluated_model_gold_answer": "Hello World",
        },
        {
            "evaluated_model_input": "Hello",
            "evaluated_model_retrieved_context": None,
            "evaluated_model_gold_answer": "Hello World",
        },
        {
            "evaluated_model_input": "Hello",
            "evaluated_model_gold_answer": "Hello World",
        },
    ]
    * 20,
    task=my_task,
    evaluators=[exact_match],
    max_concurrency=3,
)

df = ex.to_dataframe()
# print(df.info())
# print(df)


# ex2 = client.experiment(
#     "Hello World",
#     dataset=df,
#     task=my_task,
#     evaluators=[exact_match],
# )
# print("!!!!!!! EX2 !!!!!!!!!")
# print(ex2.to_dataframe().info())
