import json
import pandas as pd
from patronus import Client, task, evaluator, Row, TaskResult
from patronus import Evaluator, EvaluationResult, Row
from openai import OpenAI

client = Client(api_key="")
oai = OpenAI(api_key="")
# anthropic = anthropic.Anthropic(api_key="")

evaluation_prompt = """
        Given the utterance from a non-native English speaker, please grade the output on the following. 
        The sentence sounds natural, native and fluent in English.
        The sentence uses the correct grammatical structures and prepositional particles.
        The meaning of the sentence is clear and easy to follow.
        The sentence has a formal and polite tone instead of informal speech.
        Your score should be a scale from 1-5. You must respond with the following JSON:
        {
            score: <score>
        }

        UTTERANCE: {row.evaluated_model_input}
        """


@task
def call_gpt(row: Row):
    model = "gpt-4o"

    evaluation_result = (
        oai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": evaluation_prompt},
                {"role": "user", "content": row.evaluated_model_input},
            ],
        )
        .choices[0]
        .message.content
    )
    score = json.loads(evaluation_result)["score"]
    evaluated_model_output = str(score)
    return evaluated_model_output
