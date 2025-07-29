import abc
import asyncio
import functools
import typing
from typing import Optional


import pydantic
from opentelemetry import trace
from opentelemetry import _logs

# Would be imported from patronus.trace?
tracer = trace.get_tracer("patronus")
logger = _logs.get_logger("patronus")


class Evaluation(pydantic.BaseModel):
    pass_: Optional[bool] = None
    score: Optional[float] = None
    text_output: Optional[str] = None
    metadata: Optional[dict] = None
    tags: Optional[dict] = None

    # explanation: Optional[str] = None
    # evaluation_duration: Optional[datetime.timedelta] = None
    # explanation_duration: Optional[datetime.timedelta] = None


"""
wraps reports the function call as:
- evaluation *span* if it returns Evaluation object
- function *span* otherwise
"""


@patronus.wrap
def my_scorer(foo, bar, *, tar): ...


def _trace_evaluation(func):
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        with tracer.start_as_current_span() as span:
            span: trace.Span
            span.set_attributes(
                {
                    "function_name": func.__name__,
                }
            )
            return await func(*args, **kwargs)
        ...

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs): ...

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


class StructuredEvaluator(abc.ABC):
    def __new__(mcs, name, bases, namespace):
        if "evaluate" in namespace:
            namespace["evaluate"] = _trace_evaluation(namespace["evaluate"])

        return super().__new__(mcs, name, bases, namespace)

    @abc.abstractmethod
    def evaluate(
        self,
        *,
        system_prompt: Optional[str] = None,
        task_context: Optional[list[str]] = None,
        task_input: Optional[str] = None,
        task_output: Optional[str] = None,
        gold_answer: Optional[str] = None,
        task_metadata: Optional[dict[str, typing.Any]] = None,
        parent: Optional[typing.Any] = None,
        **kwargs,
    ) -> typing.Union[Optional[Evaluation], typing.Awaitable[Optional[Evaluation]]]: ...

    @abc.abstractmethod
    def explain(self, evaluation: Evaluation) -> typing.Union[Optional[str], typing.Awaitable[Optional[str]]]:
        return None


class RemoteEvaluator(StructuredEvaluator):
    def __init__(self, api, evaluator, criteria): ...

    def evaluate(
        self,
        *,
        system_prompt: Optional[str] = None,
        task_context: Optional[list[str]] = None,
        task_input: Optional[str] = None,
        task_output: Optional[str] = None,
        gold_answer: Optional[str] = None,
        task_metadata: Optional[dict[str, typing.Any]] = None,
        **kwargs,
    ) -> typing.Union[Optional[Evaluation], typing.Awaitable[Optional[Evaluation]]]: ...
