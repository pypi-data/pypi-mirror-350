from typing import Any, Dict, List, Optional

from nebu.containers.models import (
    V1ResourceMeta,
    V1ResourceMetaRequest,
)
from nebu.meta import V1ResourceReference
from pydantic import BaseModel, Field


class V1Trainer(BaseModel):
    processor: V1ResourceReference
    model: Optional[str] = None
    adapter: Optional[str] = None
    args: Optional[Dict[str, Any]] = None


class V1ReplayBufferRequest(BaseModel):
    metadata: V1ResourceMetaRequest
    train_every: Optional[int] = None
    sample_n: Optional[int] = Field(default=100)
    sample_strategy: Optional[str] = Field(default="Random")
    trainer: Optional[V1Trainer] = None
    num_epochs: Optional[int] = Field(default=1)


class V1UpdateReplayBufferRequest(BaseModel):
    train_every: Optional[int] = None
    sample_n: Optional[int] = None
    sample_strategy: Optional[str] = None
    trainer: Optional[V1Trainer] = None
    num_epochs: Optional[int] = None


class V1ReplayBufferStatus(BaseModel):
    num_records: Optional[int] = None
    train_idx: Optional[int] = None
    num_train_jobs: Optional[int] = None
    last_train_job: Optional[str] = None
    num_epochs: Optional[int] = None


class V1ReplayBuffer(BaseModel):
    metadata: V1ResourceMeta
    train_every: Optional[int] = None
    sample_n: Optional[int] = None
    sample_strategy: Optional[str] = None
    status: V1ReplayBufferStatus
    trainer: Optional[V1Trainer] = None
    num_epochs: Optional[int] = None


class V1ReplayBuffersResponse(BaseModel):
    buffers: List[V1ReplayBuffer]


class V1ReplayBufferData(BaseModel):
    examples: List[Dict[str, Any]]
    train: Optional[bool] = None


class V1SampleResponse(BaseModel):
    dataset_uri: Optional[str] = None
    samples: Optional[List[Dict[str, Any]]] = None


class V1SampleBufferQuery(BaseModel):
    n: int = 100
    strategy: str = "Random"
    link: bool = False


class TrainerMixin(BaseModel):
    model: str
    dataset: str
    adapter: str
