from typing import Any, Dict
from fastapi import APIRouter
from .schemas import (
    AlarmSimulationRequest,
    CustomMetricRequest,
    LogEventRequest,
)
from .service import cloudwatch_service

router = APIRouter(prefix="/api/v1/cloudwatch", tags=["📊 CloudWatch & Logs"])


@router.post("/log-event", summary="Send Structured Log Event to CloudWatch")
def put_log_event(request: LogEventRequest) -> Dict[str, Any]:
    """Emit log events using boto3 logs."""
    return cloudwatch_service.put_log_event(request)


@router.post("/put-metric", summary="Publish Custom Metric with Dimensions")
def put_custom_metric(request: CustomMetricRequest) -> Dict[str, Any]:
    """Publish custom metric using boto3 cloudwatch."""
    return cloudwatch_service.put_custom_metric(request)


@router.post("/simulate-alarm", summary="Simulate or Create Metric Alarm")
def simulate_metric_alarm(request: AlarmSimulationRequest) -> Dict[str, Any]:
    """Evaluate metric alarm thresholds and notification logic."""
    return cloudwatch_service.simulate_metric_alarm(request)
