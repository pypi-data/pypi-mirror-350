import logging
import random
import time

import patronus

#
# formatter = logging.Formatter("[%(levelname)-5s] [%(name)-10s] %(message)s")
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# console_handler.setFormatter(formatter)
#
# plog = logging.getLogger("patronus")
# plog.setLevel(logging.DEBUG)
# plog.propagate = False
# plog.addHandler(console_handler)


cli = patronus.Client()

dataset = cli.remote_dataset("pii-questions-1.0.0")


@patronus.task
def local_task(row):
    time.sleep(random.random())
    return row.evaluated_model_input


@patronus.evaluator
def local_eval(row):
    time.sleep(random.random())
    return patronus.EvaluationResult(pass_=True, score_raw=random.random())


cli.experiment("protego-dev", dataset=dataset, task=local_task, evaluators=[local_eval])
