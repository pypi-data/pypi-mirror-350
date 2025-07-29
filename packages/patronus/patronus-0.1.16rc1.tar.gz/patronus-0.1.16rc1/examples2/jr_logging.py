import time

from typing import Optional

import asyncio

import functools
import httpx


import random

import patronus
from patronus import evals
from patronus import tracing

import logging

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
# logging.getLogger("patronus.sdk").addHandler(console_handler)
#
patronus.init()

log = tracing.get_logger()


@tracing.traced()
def raiser():
    resp = httpx.get("https://kshfkas.asdjfkhad.adfhieae/foo/bar")
    print(resp)


class EvalTooBig(evals.Evaluator):
    async def evaluate(self, fib_n: int) -> Optional[evals.EvaluationResult]:
        await asyncio.sleep(random.random() / 10)
        score = 1 - (fib_n / 50)
        score = score if score > 0 else 0
        return evals.EvaluationResult(pass_=fib_n < 50, score=score, metadata={"fib_n": fib_n})


is_too_big = EvalTooBig()


@evals.evaluator()
def eval_too_big(fib_n: int):
    """
    Check whether fib_n is too big. This is fib_n < 50.
    """
    # await asyncio.sleep(random.random()/10)
    time.sleep(random.random() / 10)
    score = 1 - (fib_n / 50)
    score = score if score > 0 else 0
    return evals.EvaluationResult(pass_=fib_n < 50, score=score, metadata={"fib_n": fib_n})


@functools.lru_cache()
@tracing.traced()
def fib(n):
    log.info(f"calling fib({n})...")
    if n <= 2:
        # await eval_too_big(n)
        eval_too_big(n)
        # await is_too_big.evaluate(n)
        return n

    ret = fib(n - 1) + fib(n - 2)
    # coro1 = fib(n-1)
    # coro2 = fib(n-2)
    # ret =  (await coro1) + (await coro2)

    # log.info(f"fib({n!r}) = {ret!r}")
    # await eval_too_big(ret)
    eval_too_big(n)
    # await is_too_big.evaluate(n)
    return ret


import contextlib


@contextlib.contextmanager
def bundle_evaluations():
    yield None


@tracing.traced()
async def main():
    log.info("Starting...")

    client.evaluate(
        evaluators=[eval_too_big, is_too_big],
    )

    with bundle_evaluations() as bundle:
        eval_too_big(5)
        await is_too_big.evaluate(5)

    n = 8
    # r = await fib(n)
    r = fib(n)
    try:
        raiser()
    except Exception as e:
        pass
    log.info(f"End. r={r!r}")


if __name__ == "__main__":
    asyncio.run(main())
