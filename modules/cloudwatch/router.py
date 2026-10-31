from fastapi import APIRouter
from .schemas import (
    AlarmSimulationRequest,
    AlarmSimulationResponse,
    CustomMetricRequest,
    CustomMetricResponse,
    LogEventRequest,
    LogEventResponse,
)
from .service import cloudwatch_service

router = APIRouter(prefix="/api/v1/cloudwatch", tags=["📊 CloudWatch & Logs"])


@router.post(
    "/log-event",
    summary="Ingest Structured Log Event into CloudWatch",
    response_model=LogEventResponse
)
def put_log_event(request: LogEventRequest):
    """Streams a structured JSON log event into a CloudWatch Log Group & Stream:
    - Demonstrates JSON formatting for CloudWatch Logs Insights
    - Explains retention policies to optimize storage costs
    """
    return cloudwatch_service.put_log_event(request)


@router.post(
    "/put-metric",
    summary="Publish Custom Metric with Dimensions",
    response_model=CustomMetricResponse
)
def put_custom_metric(request: CustomMetricRequest):
    """Emits custom application metrics to CloudWatch (e.g. DonationPledgeAmount, ErrorCount) with multidimensional tagging."""
    return cloudwatch_service.put_custom_metric(request)


@router.post(
    "/simulate-alarm",
    summary="Simulate CloudWatch Metric Alarm Evaluation & SNS Notification",
    response_model=AlarmSimulationResponse
)
def simulate_metric_alarm(request: AlarmSimulationRequest):
    """Evaluates alarm thresholds (e.g. 5xx Error Rate > 5% or CPU > 80%) and demonstrates automated Amazon SNS dispatch."""
    return cloudwatch_service.simulate_metric_alarm(request)
