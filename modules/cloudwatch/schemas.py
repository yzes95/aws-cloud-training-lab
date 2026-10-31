from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LogEventRequest(BaseModel):
    log_group_name: str = Field(default="/aws/training-lab/fastapi")
    log_stream_name: str = Field(default="container-instance-01")
    message: str = Field(
        default="Donation transaction initiated for family FAM-101 with amount 500 EGP",
        description="Log message or JSON payload"
    )
    log_level: str = Field(default="INFO", description="DEBUG, INFO, WARNING, ERROR, CRITICAL")
    extra_context: Optional[Dict[str, Any]] = Field(
        default={"family_id": "FAM-101", "payment_method": "InstaPay", "ip": "192.168.1.5"}
    )


class LogEventResponse(BaseModel):
    status: str
    log_group_name: str
    log_stream_name: str
    timestamp: str
    stored_event: Dict[str, Any]
    cloudwatch_best_practice: str


class CustomMetricRequest(BaseModel):
    metric_name: str = Field(default="DonationPledgeAmount", description="Name of custom metric")
    namespace: str = Field(default="AtaaPlatform/Production", description="CloudWatch custom metric namespace")
    value: float = Field(default=500.0, description="Metric numeric value")
    unit: str = Field(default="Count", description="Count, Seconds, Bytes, Megabytes, Percent")
    dimensions: Dict[str, str] = Field(
        default={"Environment": "Production", "Category": "MedicalAid", "PaymentGateway": "InstaPay"}
    )


class CustomMetricResponse(BaseModel):
    status: str
    metric_name: str
    namespace: str
    value: float
    unit: str
    dimensions: List[Dict[str, str]]
    explanation: str


class AlarmSimulationRequest(BaseModel):
    metric_name: str = Field(default="5xxErrorRate")
    threshold: float = Field(default=5.0, description="Alarm threshold value (e.g. 5% error rate or 80% CPU)")
    current_value: float = Field(default=8.5, description="Observed current value")
    comparison_operator: str = Field(default="GreaterThanThreshold", description="GreaterThanThreshold, LessThanThreshold")
    alarm_name: str = Field(default="HighAPIErrorRateAlarm")


class AlarmSimulationResponse(BaseModel):
    alarm_name: str
    state: str  # OK, ALARM, INSUFFICIENT_DATA
    reason: str
    triggered_action: str
    sns_notification_payload: Optional[Dict[str, Any]]
    cloudwatch_monitoring_tip: str
