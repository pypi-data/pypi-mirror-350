import textwrap

from patronus import Client

import logging

formatter = logging.Formatter("[%(levelname)-5s] [%(name)-10s] %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

plog = logging.getLogger("patronus")
plog.setLevel(logging.DEBUG)
plog.propagate = False
plog.addHandler(console_handler)

cli = Client()

evaluate_proper_language = cli.remote_evaluator(
    "custom-large",
    "detect-requested-programming-languages",
    criteria_config={
        "pass_criteria": textwrap.dedent(
            """
            The MODEL OUTPUT should provide only valid code in a well-known programming language.
            The MODEL OUTPUT should consist of the code in a programming language specified in the USER INPUT.
            """
        ),
    },
    allow_update=True,
)

data = [
    {
        "evaluated_model_input": "Write a hello world example in Python.",
        "evaluated_model_output": "print('Hello World!')",
    },
    {
        "evaluated_model_input": "Write a hello world example in JavaScript.",
        "evaluated_model_output": "print('Hello World!')",
    },
]

cli.experiment(
    "Programming Language Detection",
    data=data,
    evaluators=[evaluate_proper_language],
)
