import functools
from collections.abc import Callable
from typing import TYPE_CHECKING, TypeVar, Union

from typing_extensions import Optional

from divi.decorators.observable import observable
from divi.evaluation.evaluator import EvaluatorConfig
from divi.evaluation.scores import Score
from divi.signals.span import Kind
from divi.utils import is_async

if TYPE_CHECKING:
    from openai import AsyncOpenAI, OpenAI

C = TypeVar("C", bound=Union["OpenAI", "AsyncOpenAI"])


def _get_observable_create(
    create: Callable,
    name: Optional[str] = None,
    scores: Optional[list[Score]] = None,
    eval: Optional[EvaluatorConfig] = None,
) -> Callable:
    @functools.wraps(create)
    def observable_create(*args, stream: bool = False, **kwargs):
        decorator = observable(
            kind=Kind.llm, name=name, scores=scores, eval=eval
        )
        return decorator(create)(*args, stream=stream, **kwargs)

    # TODO Async Observable Create
    return observable_create if not is_async(create) else create


def obs_openai(
    client: C,
    name: Optional[str] = "Agent",
    scores: Optional[list[Score]] = None,
    eval: Optional[EvaluatorConfig] = None,
) -> C:
    """Make OpenAI client observable."""
    client.chat.completions.create = _get_observable_create(
        client.chat.completions.create,
        name=name,
        scores=scores,
        eval=eval,
    )
    return client
