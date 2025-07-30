from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from chatmux.openai import ChatRequest, ChatResponse
from nebu import V1ResourceMeta, V1ResourceMetaRequest
from pydantic import BaseModel, Field


# Task related models
class V1TaskRequest(BaseModel):
    metadata: V1ResourceMetaRequest
    description: str
    max_steps: int


class V1AttemptStatus(str, Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"


# Chat event model
class V1ChatEvent(BaseModel):
    id: str
    task_id: Optional[str] = None
    attempt_id: Optional[str] = None
    request: ChatRequest
    response: ChatResponse


class V1Step(BaseModel):
    id: str
    task_id: str
    attempt_id: str
    state: "V1EnvState"
    action: "V1Action"
    model_id: Optional[str] = None
    chat_event: Optional[V1ChatEvent] = None
    reason: Optional[str] = None
    review_ids: Optional[List[str]] = None


class V1Attempt(BaseModel):
    id: str
    task_id: str
    status: V1AttemptStatus
    steps: List[V1Step]
    review_ids: Optional[List[str]] = None


class V1Task(BaseModel):
    metadata: V1ResourceMeta
    description: str
    attempts: List[V1Attempt]


class V1Tasks(BaseModel):
    tasks: List[V1Task]


# Action and State models
class V1Action(BaseModel):
    name: str
    parameters: Dict[str, Any]  # Corresponds to HashMap<String, Value>


class V1EnvState(BaseModel):
    images: Optional[List[Optional[str]]] = None
    coordinates: Optional[Tuple[int, int]] = None
    video: Optional[str] = None
    text: Optional[str] = None
    timestamp: Optional[float] = None


# Step request model
class V1StepRequest(BaseModel):
    state: V1EnvState
    action: V1Action
    model_id: Optional[str] = None
    chat_event: Optional[V1ChatEvent] = None
    reason: Optional[str] = None


# Review related models
class V1ReviewerType(str, Enum):
    HUMAN = "human"
    AI = "ai"


class V1ResourceType(str, Enum):
    TASK = "task"
    ATTEMPT = "attempt"
    STEP = "step"


class V1ReviewRequest(BaseModel):
    reviewer: str
    approved: bool
    resource_type: V1ResourceType
    resource_id: str
    with_resources: Optional[List[str]] = None
    reviewer_type: V1ReviewerType = Field(default=V1ReviewerType.HUMAN)
    reason: Optional[str] = None
    parent_id: Optional[str] = None
    correction: Optional[str] = None
    correction_schema: Optional[Dict[str, Any]] = None  # Corresponds to Option<Value>


class V1Review(BaseModel):
    id: str
    reviewer: str
    approved: bool
    resource_type: V1ResourceType
    resource_id: str
    with_resources: Optional[List[str]] = None
    reviewer_type: V1ReviewerType
    reason: Optional[str] = None
    parent_id: Optional[str] = None
    correction: Optional[str] = None
    correction_schema: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class V1Reviews(BaseModel):
    reviews: List[V1Review]
