import random
from typing import Optional

import patronus

client = patronus.Client()


@client.register_local_evaluator("reverse")
def my_local_evaluator(
    evaluated_model_system_prompt: Optional[str],
    # evaluated_model_retrieved_context: Optional[Union[list[str], str]],
    evaluated_model_input: Optional[str],
    evaluated_model_output: Optional[str],
    # evaluated_model_gold_answer: Optional[str],
    # evaluated_model_attachments: Optional[list[dict[str, Any]]],
    # tags: Optional[dict[str, str]] = None,
    # explain_strategy: Literal["never", "on-fail", "on-success", "always"] = "always",
    **kwargs,
) -> patronus.EvaluationResult:
    v = random.random()
    pass_ = v < 0.66
    if pass_ < 0.33:
        pass_ = None
    return patronus.EvaluationResult(
        pass_=pass_,
        score_raw=v,
        text_output=evaluated_model_output[::-1],
        metadata={
            "system_prompt": evaluated_model_system_prompt and evaluated_model_system_prompt[::-1],
            "input": evaluated_model_input and evaluated_model_input[::-1],
            "output": evaluated_model_output and evaluated_model_output[::-1],
        },
        explanation="An explanation!",
        evaluation_duration_s=random.random(),
        explanation_duration_s=random.random(),
        tags={"env": "local"},
    )


resp = client.evaluate(
    "reverse",
    evaluated_model_system_prompt="sys prompt!",
    evaluated_model_input="Say Foo",
    evaluated_model_output="Foo!",
    evaluated_model_attachments=[{"url": "http://localhost:1222/foo/bar", "media_type": "image/jpeg"}],
)
print(resp.model_dump(by_alias=True))
