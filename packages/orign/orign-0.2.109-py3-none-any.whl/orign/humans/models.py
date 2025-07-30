from typing import Any, List, Optional, Union

from nebu.meta import V1ResourceMeta, V1ResourceMetaRequest, V1ResourceReference
from pydantic import BaseModel, Field


class V1HumanRequest(BaseModel):
    metadata: V1ResourceMetaRequest
    medium: str
    channel: Optional[str] = None
    callback: V1ResourceReference


class V1UpdateHumanRequest(BaseModel):
    medium: Optional[str] = None
    channel: Optional[str] = None
    callback: Optional[V1ResourceReference] = None


class V1HumanStatus(BaseModel):
    is_active: Optional[bool] = None
    last_active: Optional[str] = None


class V1Human(BaseModel):
    metadata: V1ResourceMeta
    medium: str
    channel: Optional[str] = None
    callback: V1ResourceReference
    status: V1HumanStatus


class V1Humans(BaseModel):
    humans: List[V1Human] = Field(default_factory=list)


class V1ApprovalRequest(BaseModel):
    content: str
    messages: Optional[Any] = None
    images: Optional[List[str]] = None
    videos: Optional[List[str]] = None


class V1ApprovalResponse(BaseModel):
    content: str
    messages: Optional[Any] = None
    images: Optional[List[str]] = None
    videos: Optional[List[str]] = None
    approved: bool = False


V1FeedbackRequestKind = Union[V1ApprovalRequest]  # type: ignore
V1FeedbackResponseKind = Union[V1ApprovalResponse]  # type: ignore


class V1FeedbackRequest(BaseModel):
    kind: str
    request: Optional[V1FeedbackRequestKind] = None


class V1Feedback(BaseModel):
    kind: str
    request: V1FeedbackRequestKind
    response: Optional[V1FeedbackResponseKind] = None


class V1FeedbackResponse(BaseModel):
    kind: str
    response: Optional[V1FeedbackResponseKind] = None


class V1HumanMessage(BaseModel):
    content: str


class ListFeedbackParams(BaseModel):
    pending: Optional[bool] = None


class V1FeedbackRequestData(BaseModel):
    kind: str
    data: Any


class V1FeedbackResponseData(BaseModel):
    kind: str
    data: Any


class V1FeedbackItem(BaseModel):
    feedback_id: str = Field(alias="feedbackId")
    human_namespace: str
    human_name: str
    status: Optional[str] = None
    created_at: int
    updated_at: int
    request: V1FeedbackRequestData
    response: Optional[V1FeedbackResponseData] = None


class V1ListFeedbackResponse(BaseModel):
    feedback: List[V1FeedbackItem] = Field(default_factory=list)
