import typing

import asyncio
import textwrap

from typing import Union, Optional

import openai

from examples.demo import gold_answer
from patronus import evals, datasets, EvaluationResult, traced
from patronus.evals import RemoteEvaluator, AsyncRemoteEvaluator
from patronus.experiments import TaskResult, EvalParent
from patronus.experiments.adapters import StructuredEvaluatorAdapter, EvaluatorAdapter
from patronus.experiments.experiment import Experiment, run_experiment

oai = openai.OpenAI()

system_prompt = """\
Detect whether message is a spam or not.

The following may be considered as spam messages:
- Unsolicited bulk emails promoting products or services
- Messages with misleading or deceptive subject lines
- Communications that hide or falsify the sender's identity
- Messages containing suspicious links or attachments
- Repeated unwanted messages after requests to stop
- Phishing attempts requesting personal or financial information
- Messages promoting questionable or fraudulent schemes
- Automated comments or posts on social media platforms
- Unwanted messages sent through messaging apps or SMS

Provide reasoning and finish the message with 'The message is spam? true' or 'The message is spam? false'.
"""

system_prompt_postambule = "I remember to finish the message with 'true' or 'false'. No more text will be generated after these words."

dataset = [
    {
        "message": "Congratulations! You’ve won a $500 Amazon gift card. Claim it here",
        "is_spam": "true",
    },
    {
        "message": "ACTION REQUIRED. Please verify your Bank of America account information to avoid a hold on your account. Click here to confirm",
        "is_spam": "true",
    },
    {
        "message": "You’ve been overcharged for your 2021 taxes. Get your IRS tax refund here",
        "is_spam": "true",
    },
    {
        "message": "Interview: next steps",
        "is_spam": "false",
    },
]


class JudgeSpamDetector(StructuredEvaluatorAdapter):

    def __init__(self):
        evaluator = AsyncRemoteEvaluator("judge", "is-spam")
        super().__init__(evaluator)

    async def evaluate(self, row: datasets.Row, task_result, parent, **kwargs):
        return await self._evaluate(
            task_output=row.message,
            gold_answer=row.is_spam,
        )


class MyEvaluatorAdapter(StructuredEvaluatorAdapter):

    def __init__(self):
        evaluator = RemoteEvaluator("judge", "...")
        super().__init__(evaluator)

    def evaluate(self, row: datasets.Row, task_result, parent, **kwargs):
        return self._evaluate(
            task_input=row.task_input, task_output=row.task_output, tags={"t1": "t2"}
        )


class GPTSpamDetectorEvaluator(evals.Evaluator):

    def evaluate(self, message: str, expected: str, **kwargs):
        response = oai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": message,
                },
                {
                    "role": "assistant",
                    "content": system_prompt_postambule,
                },
            ],
        )
        m = response.choices[0].message.content
        is_true = m.endswith("true")
        is_false = m.endswith("false")
        if is_true is False and is_false is False:
            raise ValueError(f"Model returned unexpected message; model response: {m}")

        return EvaluationResult(pass_=is_true, score=float(is_true))


class AdaptedGPTSpamDetector(EvaluatorAdapter):
    def __init__(self):
        evaluator = GPTSpamDetectorEvaluator()
        super().__init__(evaluator)

    def transform(self, row: datasets.Row, task_result: Optional[TaskResult], parent: EvalParent, **kwargs) -> tuple[
        list[typing.Any], dict[str, typing.Any]]:
        return [row.message, row.is_spam], {}


@traced()
def main(foo, bar):
    run_experiment(
        dataset=dataset,
        evaluators=[AdaptedGPTSpamDetector(), JudgeSpamDetector()],
        max_concurrency=10,
    )


if __name__ == "__main__":
    main("foo", None)
