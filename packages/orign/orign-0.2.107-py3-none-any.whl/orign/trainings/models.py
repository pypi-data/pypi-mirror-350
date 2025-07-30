from enum import Enum
from typing import Any, Dict, List, Optional

from nebu import V1ResourceMeta, V1ResourceMetaRequest, V1ResourceReference
from pydantic import BaseModel, Field


class V1TrainingStatus(str, Enum):
    """Represents the status of a training."""

    STARTING = "starting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


class V1TrainingRequest(BaseModel):
    """Request body for creating a new training."""

    metadata: V1ResourceMetaRequest
    config: Optional[Dict[str, Any]] = None  # Flexible config (e.g., hyperparameters)
    adapter: Optional[V1ResourceReference] = None
    unique_adapter_active: bool = False


class V1TrainingUpdateRequest(BaseModel):
    """Request body for updating a training (e.g., status, summary)."""

    status: Optional[V1TrainingStatus] = None
    summary_metrics: Optional[Dict[str, Any]] = None  # Final metrics summary


class V1Training(BaseModel):
    """Represents a single training resource."""

    metadata: V1ResourceMeta
    config: Optional[Dict[str, Any]] = None
    status: V1TrainingStatus
    summary_metrics: Optional[Dict[str, Any]] = None
    adapter: Optional[V1ResourceReference] = None
    # Timestamps etc. are assumed to be in metadata


class V1Trainings(BaseModel):
    """Response body for listing multiple trainings."""

    trainings: List[V1Training] = Field(default_factory=list)


class V1LogRequest(BaseModel):
    """Request body for logging metrics/data during a training."""

    step: Optional[int] = None  # Optional step counter (e.g., epoch, batch number)
    timestamp: Optional[int] = None  # Optional explicit timestamp (ms since epoch)
    data: Dict[str, Any]  # The actual metrics/values being logged
