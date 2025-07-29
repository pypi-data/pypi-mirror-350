import asyncio

import patronus
from patronus.evals import bundled_eval, evaluator, AsyncRemoteEvaluator

patronus.init()

is_polite = AsyncRemoteEvaluator("judge", "patronus:is-polite")

@evaluator()
def exact_match(actual, expected):
    return actual == expected

@evaluator()
def iexact_match(actual: str, expected: str):
    return actual.strip().lower() == expected.strip().lower()

async def main():
    await is_polite.evaluate(task_output="You little ***")



asyncio.run(main())