from typing import Dict, List, Optional

from nebu import V1ResourceMeta, V1ResourceMetaRequest
from pydantic import BaseModel, Field


class V1LoraParams(BaseModel):
    """LoRA configuration parameters."""

    r: int = 8
    alpha: int = 16
    dropout: float = 0.1
    target_modules: List[str] = Field(default_factory=list)


class V1AdapterRequest(BaseModel):
    """Request payload for creating an adapter."""

    metadata: V1ResourceMetaRequest
    model_uri: Optional[str] = None
    checkpoint_uri: Optional[str] = None
    base_model: str
    lora: Optional[V1LoraParams] = None
    learning_rate: Optional[float] = None
    epochs_trained: Optional[int] = None
    last_trained: Optional[int] = None
    examples_trained: Optional[int] = None


class V1AdapterUpdateRequest(BaseModel):
    """Request payload for updating an adapter."""

    model_uri: Optional[str] = None
    checkpoint_uri: Optional[str] = None
    epochs_trained: Optional[int] = None
    examples_trained: Optional[int] = None
    last_trained: Optional[int] = None
    labels: Optional[Dict[str, str]] = None
    learning_rate: Optional[float] = None
    lora: Optional[V1LoraParams] = None


class V1Adapter(BaseModel):
    """Response payload representing an adapter."""

    metadata: V1ResourceMeta
    model_uri: str
    checkpoint_uri: str
    base_model: str
    epochs_trained: int
    examples_trained: int
    last_trained: int
    lora: Optional[V1LoraParams] = None
    learning_rate: Optional[float] = None


class V1Adapters(BaseModel):
    """Response payload for a list of adapters."""

    adapters: List[V1Adapter]
