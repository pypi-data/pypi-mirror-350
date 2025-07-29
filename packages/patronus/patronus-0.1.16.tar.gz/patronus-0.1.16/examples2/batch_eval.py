from typing import Optional

import patronus

client = patronus.Client()


@client.register_local_evaluator("scorer_a")
def scorer_a(
    evaluated_model_output: Optional[str],
    **kwargs,
):
    x = len(evaluated_model_output) / 10
    if x < 1:
        return patronus.EvaluationResult(score_raw=x)
    else:
        return patronus.EvaluationResult(score_raw=1)


@client.register_local_evaluator("iexact_match")
def iexact_match(
    evaluated_model_output: Optional[str],
    evaluated_model_gold_answer: Optional[str],
    **kwargs,
):
    if not evaluated_model_output or not evaluated_model_gold_answer:
        return None
    pass_ = evaluated_model_output.strip().lower() == evaluated_model_gold_answer.strip().lower()
    return patronus.EvaluationResult(pass_=pass_)


def batch_eval(
    client: patronus.Client,
    evaluators: list,
    **kwargs,
):
    ret = []
    for evaluator in evaluators:
        evaluator_id, criteria = None, None
        if isinstance(evaluator, (list, tuple)):
            if len(evaluator) == 1:
                evaluator_id = evaluator[0]
            elif len(evaluator) >= 2:
                evaluator_id, criteria = evaluator
        else:
            evaluator_id = evaluator

        ret.append(client.evaluate(evaluator_id, criteria, **kwargs))
    return ret


batch_eval(
    client,
    evaluators=[
        "scorer_a",
        "iexact_match",
        ("judge", "patronus:fuzzy-match"),
    ],
    evaluated_model_input="What is the oldest tree",
    evaluated_model_output="  great basin bristlecone pine\t",
    evaluated_model_gold_answer="Great Basin Bristlecone Pine",
)
