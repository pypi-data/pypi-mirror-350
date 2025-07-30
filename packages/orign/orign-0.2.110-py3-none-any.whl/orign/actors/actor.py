from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from openai.types.chat import ChatCompletion
from pydantic import BaseModel

from .models import Action
from .state import EnvState


@dataclass
class Step:
    """A step in an episode"""

    state: EnvState
    action: Action
    action_opts: Optional[List[Action]] = None
    task: Optional[str] = None
    model_id: Optional[str] = None
    prompt: Optional[ChatCompletion | Dict[str, ChatCompletion]] = None
    reason: Optional[str] = None
    stop: Optional[bool] = None


class ReasonedAction(BaseModel):
    action: Action
    reason: str


class Actor(ABC):
    """An actor that can act on a task"""

    @abstractmethod
    def act(self, task: str, mcp_servers: List[Any], history: List[Step]) -> Step:
        pass


def actor(func: Callable[[str, List[Any], List[Step]], Step]) -> Actor:
    """
    Decorator that converts a function into an Actor.

    The decorated function should have the same signature as Actor.act:
    func(task: str, mcp_servers: List[Any], history: List[Step]) -> Step
    """

    class FunctionActor(Actor):
        def act(self, task: str, mcp_servers: List[Any], history: List[Step]) -> Step:
            return func(task, mcp_servers, history)

    return FunctionActor()
