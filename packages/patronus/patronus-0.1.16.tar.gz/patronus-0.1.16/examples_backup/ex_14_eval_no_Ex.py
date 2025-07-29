import asyncio

import patronus
from patronus import EvaluateRequest

cli = patronus.Client()

eval_is_code = cli.remote_evaluator("judge", "patronus:is-code")
await cli.api.evaluate(
    EvaluateRequest(
        evaluators=[{"evaluator": "judge", "profile_name": "patronus:is-code"}],
        evaluated_model_output="print('hello world')",
        app="protego-dev-no-ex",
    )
)

# await eval_is_code.evaluate(
#     evaluated_model_output="""
#         ```python
#         print("Hello World")
#         ```
#         """,
#     app="protego-dev-no-ex",
# )
#


async def main():
    resp = await eval_is_code.evaluate(
        evaluated_model_output="""
        ```python
        print("Hello World")
        ```
        """,
        app="protego-dev-no-ex",
    )
    print(resp)
    print()
    print()

    resp2 = await cli.api.evaluate(
        EvaluateRequest(
            evaluators=[{"evaluator": "judge", "profile_name": "patronus:is-code"}],
            evaluated_model_output="print('hello world')",
            app="protego-dev-no-ex",
        )
    )
    print(resp2)


asyncio.run(main())
