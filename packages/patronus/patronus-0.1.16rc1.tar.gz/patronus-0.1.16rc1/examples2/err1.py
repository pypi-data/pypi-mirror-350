import patronus


client = patronus.Client()

ex_match = client.remote_evaluator("exact-match", "patronus:exact-match")

dataset = [
    {"evaluated_model_output": "hello", "evaluated_model_gold_answer": "Hello!"},
]


client.experiment(
    "JR",
    dataset=dataset,
    evaluators=[ex_match],
)
