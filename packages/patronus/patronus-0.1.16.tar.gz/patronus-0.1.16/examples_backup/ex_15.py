from patronus import Client

client = Client()

evaluator = client.remote_evaluator(EVALUATOR, PROFILE_NAME, max_attempts=3)

await evaluator.evaluate(
    evaluated_model_system_prompt="SYSTEM_PROMPT",
    evaluated_model_retrieved_context=["RETRIEVED_CONTEXT"],
    evaluated_model_input="MODEL_INPUT",
    evaluated_model_output="MODEL_OUTPUT",
    evaluated_model_gold_answer="GOLD_ANSWER",
    app="playground",
)
