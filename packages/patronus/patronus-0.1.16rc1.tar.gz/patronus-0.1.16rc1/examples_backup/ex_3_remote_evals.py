from patronus import Client, task

cli = Client()

import logging

formatter = logging.Formatter("[%(levelname)-5s] [%(name)-10s] %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

plog = logging.getLogger("patronus")
plog.setLevel(logging.DEBUG)
plog.propagate = False
plog.addHandler(console_handler)

eval_patronus_is_similar = cli.remote_evaluator(
    evaluator_id_or_alias="custom-small",
    criteria="system:is-similar-to-gold-answer",
    max_attempts=4,
)


@task
def say_hi(evaluated_model_input: str) -> str:
    return f"Hi {evaluated_model_input}"


entry = {"evaluated_model_input": "Foo", "evaluated_model_gold_answer": "Hi Foo"}

ex = cli.experiment(
    "patronus-evals",
    data=[entry] * 20,
    task=say_hi,
    evaluators=[eval_patronus_is_similar],
)

ex.to_dataframe()
