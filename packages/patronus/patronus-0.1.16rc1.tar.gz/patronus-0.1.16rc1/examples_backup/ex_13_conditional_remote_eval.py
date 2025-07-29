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
            },
            {
                "url": "https://fastly.picsum.photos/id/776/200/200.jpg?hmac=Rq9krBqm0Qss3AbgE4BjL1Iu891xLPTkf1xNf0ezp38",
                "media_type": "image/jpeg",
            },
        ],
    }
]

judge_mm = cli.remote_evaluator("judge-mm", "patronus:caption-describes-non-primary-objects")
# judge = cli.remote_evaluator("judge-small", "patronus:is-concise")


# @judge.wrap
# def conditional_judge(evaluate, row, parent):
#     return evaluate()


ex = cli.experiment("protego-dev", dataset=dataset, evaluators=[judge_mm])
# ex = cli.experiment("protego-dev", dataset=dataset, evaluators=[judge])
