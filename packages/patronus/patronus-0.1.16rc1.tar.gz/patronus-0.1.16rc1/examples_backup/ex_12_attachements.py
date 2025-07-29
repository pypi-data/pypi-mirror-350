import asyncio

import patronus


cli = patronus.Client()

dataset = [
    {
        "evaluated_model_input": "Say hello world",
        "evaluated_model_output": "Hello World?",
        "evaluated_model_attachments": [
            {
                "url": "https://fastly.picsum.photos/id/776/200/200.jpg?hmac=Rq9krBqm0Qss3AbgE4BjL1Iu891xLPTkf1xNf0ezp38",
                "media_type": "image/jpeg",
            }
        ],
    },
    {
        "evaluated_model_input": "ABCD",
        "evaluated_model_output": "EFGHIJ",
        "evaluated_model_attachments": {
            "url": "https://fastly.picsum.photos/id/776/200/200.jpg?hmac=Rq9krBqm0Qss3AbgE4BjL1Iu891xLPTkf1xNf0ezp38",
            "media_type": "image/jpeg",
        },
    },
]

judge_mm = cli.remote_evaluator("judge-mm", "patronus:caption-describes-non-primary-objects")

ex = cli.experiment("p1", dataset=dataset, evaluators=[judge_mm])
