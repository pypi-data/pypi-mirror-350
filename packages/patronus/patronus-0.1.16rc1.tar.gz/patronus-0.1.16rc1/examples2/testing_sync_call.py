# import os
# from patronus import Client
#
# client = Client(
#     # This is the default and can be omitted
#     api_key=os.environ.get("PATRONUS_API_KEY"),
# )
# result = client.evaluate(
#     evaluator="lynx",
#     criteria="patronus:hallucination",
#     evaluated_model_input="Who are you?",
#     evaluated_model_output="My name is Barry.",
#     evaluated_model_retrieved_context="My name is John.",
# )
# print(f"Pass: {result.pass_}")
# print(f"Explanation: {result.explanation}")# More feature-rich example
# # Using async/await
# import asyncio
# from patronus import Client
#
# client = Client()
#
# no_apologies = client.remote_evaluator(
#     "judge",
#     "patronus:no-apologies",
#     explain_strategy="always",
#     max_attempts=3,
# )
#
#
# async def evaluate():
#     result = await no_apologies.evaluate(
#         evaluated_model_input="How to kill a docker container?",
#         evaluated_model_output="""
#         I cannot assist with that question as it has been marked as inappropriate.
#         I must respectfully decline to provide an answer."
#         """,
#     )
#     print(f"Pass: {result.pass_}")
#     print(f"Explanation: {result.explanation}")
#
#
# asyncio.run(evaluate())
import asyncio
from patronus import Client, api_types

client = Client()


async def evaluate():
    resp = await client.api.evaluate(
        api_types.EvaluateRequest(
            evaluators=[api_types.EvaluateEvaluator(evaluator="lynx", criteria="patronus:hallucination")],
            evaluated_model_input="Who are you?",
            evaluated_model_output="My name is Barry.",
            evaluated_model_retrieved_context="My name is John.",
        )
    )
    print(resp.model_dump_json(indent=2))


asyncio.run(evaluate())
