import patronus

client = patronus.Client()
resp = client.evaluate(
    "judge",
    "patronus:is-code",
    evaluated_model_output="print('hello world');",
    capture="none",
)
