import typing

from typing import Optional, Union, Any

import patronus
from patronus import StructuredEvaluator, EvaluationResult
from patronus.api.api_types import Evaluation
from patronus.evals import RemoteEvaluator, evaluator, bundled_eval
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor


patronus.init(integrations=HTTPXClientInstrumentor())


@evaluator()
def is_even(n):
    return n % 2 == 0


class ExactMatch(StructuredEvaluator):

    def evaluate(self, *, system_prompt: Optional[str] = None, task_context: Union[list[str], str, None] = None,
                 task_attachments: Union[list[Any], None] = None, task_input: Optional[str] = None,
                 task_output: Optional[str] = None, gold_answer: Optional[str] = None,
                 task_metadata: Optional[typing.Dict[str, typing.Any]] = None, **kwargs: Any) -> EvaluationResult:
        return EvaluationResult(pass_=task_output==gold_answer)


@patronus.traced("workflow")
def main():
    with patronus.Patronus() as c:
        c.evaluate(
            evaluators=[("judge", "patronus:is-polite"), ExactMatch()],
            task_output="Hello! :) How can I assist you today?"
        )
    RemoteEvaluator("judge", "patronus:is-polite").evaluate(task_output="Hello?")


main()

# RemoteEvaluator("judge", "patronus:is-polite").evaluate(task_output="Hello?")