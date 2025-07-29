import logging

import patronus


formatter = logging.Formatter("[%(levelname)-5s] [%(name)-10s] %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

plog = logging.getLogger("patronus")
plog.setLevel(logging.DEBUG)
plog.propagate = False
plog.addHandler(console_handler)


dataset = patronus.read_csv("./out.csv")

cli = patronus.Client()

dummy_eval = cli.remote_evaluator("dummy")

cli.experiment(
    "protego-dev",
    dataset=dataset,
    evaluators=[dummy_eval],
)
