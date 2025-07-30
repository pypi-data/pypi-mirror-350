from typing import Any, Dict, List, Optional

from nebu.meta import V1ResourceMeta, V1ResourceMetaRequest, V1ResourceReference
from pydantic import BaseModel, ConfigDict, Field

from orign.buffers.models import V1Trainer


class V1TrainLLM(BaseModel):
    strategy: Optional[str] = Field(default="Random")
    n: Optional[int] = Field(default=1000)
    extra_args: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(use_enum_values=True)


class V1OnlineLLMRequest(BaseModel):
    metadata: V1ResourceMetaRequest
    model: str
    server: V1ResourceReference
    trainer: V1Trainer
    input_schema: Optional[str] = None
    train_every: Optional[int] = None
    sample_n: Optional[int] = None
    sample_strategy: Optional[str] = None
    num_epochs: Optional[int] = None
    adapter: Optional[str] = None
    model_config = ConfigDict(use_enum_values=True)


class V1UpdateOnlineLLMRequest(BaseModel):
    model: Optional[str] = None
    server: Optional[V1ResourceReference] = None
    trainer: Optional[V1Trainer] = None
    input_schema: Optional[str] = None
    no_delete: Optional[bool] = None
    train_every: Optional[int] = None
    sample_n: Optional[int] = None
    sample_strategy: Optional[str] = None
    num_epochs: Optional[int] = None
    adapter: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class V1OnlineLLMStatus(BaseModel):
    is_online: Optional[bool] = None
    endpoint: Optional[str] = None
    last_error: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class V1OnlineLLM(BaseModel):
    metadata: V1ResourceMeta
    model: str
    buffer: V1ResourceReference
    server: V1ResourceReference
    trainer: V1Trainer
    input_schema: Optional[str] = None
    status: V1OnlineLLMStatus = Field(default_factory=V1OnlineLLMStatus)
    train_every: Optional[int] = None
    sample_n: Optional[int] = None
    sample_strategy: Optional[str] = None
    num_epochs: Optional[int] = None
    adapter: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class V1OnlineLLMs(BaseModel):
    llms: List[V1OnlineLLM]

    model_config = ConfigDict(use_enum_values=True)


class V1GenerateRequest(BaseModel):
    content: Any
    user_key: Optional[str] = None
