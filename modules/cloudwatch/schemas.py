from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class LogEventRequest(BaseModel):
    log_group_name: str = Field(default="/aws/training-lab/fastapi")
    log_stream_name: str = Field(default="api-instance-1")
    message: str = Field(default="Sample log event from FastAPI")
    log_level: str = Field(default="INFO")
    extra_context: Optional[Dict[str, Any]] = None


class CustomMetricRequest(BaseModel):
    metric_name: str = Field(default="DonationCount")
    namespace: str = Field(default="AtaaPlatform/Training")
    value: float = Field(default=1.0)
    unit: str = Field(default="Count")
    dimensions: Optional[Dict[str, str]] = None


class AlarmSimulationRequest(BaseModel):
    metric_name: str = Field(default="5xxErrorRate")
    threshold: float = Field(default=5.0)
    current_value: float = Field(default=8.5)
    comparison_operator: str = Field(default="GreaterThanThreshold")
    alarm_name: str = Field(default="HighAPIErrorRateAlarm")
