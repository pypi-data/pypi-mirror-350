from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Action(BaseModel):
    """An action on a tool"""

    name: str = Field(..., description="The name of the action to be performed.")
    parameters: Dict[str, Any] = Field(
        ...,
        description="A dictionary containing parameters necessary for the action, with keys as parameter names and values as parameter details.",
    )


class ActionSelection(BaseModel):
    """An action selection from the model"""

    observation: Optional[str] = Field(
        ..., description="Observations of the current state of the environment"
    )
    reason: Optional[str] = Field(
        ...,
        description="The reason why this action was chosen, explaining the logic or rationale behind the decision.",
    )
    action: Action = Field(
        ...,
        description="The action object detailing the specific action to be taken, including its name and parameters.",
    )
    expectation: Optional[str] = Field(
        ...,
        description="The expected outcome of the action e.g. 'a login page should open'",
    )
