import random
import time

import numpy as np
import faker
import patronus

project = f"Experiments tag.model {int(time.time())} {faker.Faker().word()}"

ex_name_rnd = random.Random(time.time())

faker.Faker.seed(123)
fake = faker.Faker()

data = [
    {
        "evaluated_model_input": fake.text(30),
        "evaluated_model_output": fake.text(30),
    }
    for _ in range(30)
]
dataset = patronus.Dataset.from_records(records=data, dataset_id="local-ds-123")

MAX_ITERS = 1

for iteration in range(MAX_ITERS):
    random.seed(12)
    it_rnd = random.Random(iteration)
    b_rnd = random.Random(iteration)

    cli = patronus.Client()

    @patronus.evaluator
    def score_A(evaluated_model_input, evaluated_model_output, tags) -> patronus.EvaluationResult:
        if tags.get("model") == "small":
            v = float(np.clip(np.random.normal(loc=0.5, scale=0.15), 0.2, 0.8))
            v -= it_rnd.random() * 0.05 + iteration / 100
        else:
            v = float(np.clip(np.random.normal(loc=0.5, scale=0.15), 0.2, 0.8))
            v += it_rnd.random() * 0.05 + iteration / 100
        return patronus.EvaluationResult(pass_=v > 0.5, score_raw=v, tags={"model": fake.word()})

    @patronus.evaluator
    def score_B(tags) -> patronus.EvaluationResult:
        if tags.get("model") == "small":
            # 0.55 - 0.73 - 0.66
            if iteration < 0.62 * MAX_ITERS:
                v = (0.73 - 0.55) / MAX_ITERS * iteration
            else:
                v = (0.73 - 0.66) / MAX_ITERS * iteration
        else:
            # 0.61 - 0.39 - 0.44
            if iteration < 0.44 * MAX_ITERS:
                v = (0.61 - 0.39) / MAX_ITERS * iteration
            else:
                v = (0.44 - 0.39) / MAX_ITERS * iteration
        v += (b_rnd.random() - 0.5) * 0.05
        return patronus.EvaluationResult(score_raw=v)

    cli.experiment(
        project,
        dataset=dataset,
        evaluators=[score_A, score_B],
        max_concurrency=1,
        tags={
            "model": "small" * 100,
        },
        experiment_name=f"ex-small",
    )

    cli.experiment(
        project,
        dataset=dataset,
        evaluators=[score_A, score_B],
        max_concurrency=1,
        tags={
            "model": "large" * 100,
        },
        experiment_name=f"ex-large",
    )
