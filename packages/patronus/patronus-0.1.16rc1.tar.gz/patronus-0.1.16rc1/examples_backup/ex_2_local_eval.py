import logging
import random

import patronus
from patronus import evaluator, Client, task, retry

cli = Client()

formatter = logging.Formatter("[%(levelname)-5s] [%(name)-10s] %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

plog = logging.getLogger("patronus")
plog.setLevel(logging.DEBUG)
plog.propagate = False
plog.addHandler(console_handler)


@task
@retry(max_attempts=3)
async def say_hi(evaluated_model_input: str) -> str:
    r = random.random()
    # if r < 0.5:
    #     raise Exception(f"Task random exception; r={r}")
    return f"Hi {evaluated_model_input}"


@evaluator(criteria="123")
# @retry(max_attempts=3)
def iexact_match(evaluated_model_output: str, evaluated_model_gold_answer: str) -> bool:
    # async def iexact_match(evaluated_model_output: str, evaluated_model_gold_answer: str) -> bool:
    r = random.random()
    # if r < 0.5:
    #     raise Exception(f"Evaluation random exception; r={r}")
    # await asyncio.sleep(random.random() * 3)
    return evaluated_model_output.lower().strip() == evaluated_model_gold_answer.lower().strip()


@evaluator
def rnd(row) -> patronus.EvaluationResult:
    r = random.random()
    pass_ = r > 0.5
    return patronus.EvaluationResult(pass_=pass_, score_raw=r)


entry = {
    "evaluated_model_input": "Bar",
    "evaluated_model_gold_answer": "eloh Bar!",
}

ex = cli.experiment(
    "local-imatch-evals",
    data=[entry] * 10,
    task=say_hi,
    evaluators=[iexact_match, rnd],
    max_concurrency=5,
)
