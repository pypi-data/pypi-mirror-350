from patronus import Client, EvaluationResult

client = Client()

name = "local_evaluator name"


@client.register_local_evaluator(name)
def my_evaluator(**kwargs):
    return EvaluationResult(text_output="abc")


client.evaluate(
    name,
    evaluated_model_input="Who are you?",
    evaluated_model_output="My name is Barry.",
    evaluated_model_retrieved_context="My name is John.",
)
