from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
import uuid

class PipelineStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"

class FailureType(str, Enum):
    NETWORK = "network"
    VALIDATION_SERVICE = "validation_service"
    DATABASE = "database"
    UNKNOWN = "unknown"

class AlertLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class PipelineEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime
    event_type: str
    details: Dict[str, Any]
    status: PipelineStatus
    failure_type: Optional[FailureType] = None
    component: Optional[str] = None
    alert_level: Optional[AlertLevel] = None

class RecoveryResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    success: bool
    message: str
    action_taken: str
    timestamp: datetime
    failure_type: Optional[FailureType] = None
    related_event_id: Optional[str] = None

class HealthCheckResponse(BaseModel):
    status: PipelineStatus
    timestamp: datetime
    components: Dict[str, Any]
    failure_type: Optional[FailureType] = None