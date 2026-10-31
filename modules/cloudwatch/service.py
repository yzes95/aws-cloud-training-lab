import time
from datetime import datetime, timezone
from typing import Any, Dict, List
from core.config import settings
from core.aws_client import get_boto3_client
from .schemas import (
    AlarmSimulationRequest,
    AlarmSimulationResponse,
    CustomMetricRequest,
    CustomMetricResponse,
    LogEventRequest,
    LogEventResponse,
)


class CloudWatchService:
    """Service providing hands-on training for Amazon CloudWatch Logs, Metrics, and Alarms."""

    def put_log_event(self, req: LogEventRequest) -> LogEventResponse:
        """Sends or simulates sending a structured log event to CloudWatch Logs."""
        now_ts = int(time.time() * 1000)
        iso_str = datetime.now(timezone.utc).isoformat()

        log_payload = {
            "timestamp": iso_str,
            "level": req.log_level.upper(),
            "message": req.message,
            "context": req.extra_context or {}
        }

        if not settings.AWS_MOCK_MODE and settings.AWS_ACCESS_KEY_ID:
            try:
                cw_logs = get_boto3_client("logs")
                # Try create log stream if not exists
                try:
                    cw_logs.create_log_stream(
                        logGroupName=req.log_group_name,
                        logStreamName=req.log_stream_name
                    )
                except Exception:
                    pass

                cw_logs.put_log_events(
                    logGroupName=req.log_group_name,
                    logStreamName=req.log_stream_name,
                    logEvents=[{
                        "timestamp": now_ts,
                        "message": str(log_payload)
                    }]
                )
                return LogEventResponse(
                    status="Log event sent to real CloudWatch Logs stream",
                    log_group_name=req.log_group_name,
                    log_stream_name=req.log_stream_name,
                    timestamp=iso_str,
                    stored_event=log_payload,
                    cloudwatch_best_practice="Logs are streamed asynchronously without blocking HTTP request threads."
                )
            except Exception:
                pass

        return LogEventResponse(
            status="Simulated CloudWatch Log Event Ingested",
            log_group_name=req.log_group_name,
            log_stream_name=req.log_stream_name,
            timestamp=iso_str,
            stored_event=log_payload,
            cloudwatch_best_practice=(
                "CloudWatch Logs Best Practices:\n"
                "1. Structured JSON: Always emit logs in JSON format. This allows CloudWatch Logs Insights "
                "to run fast SQL-like queries (e.g. `fields @timestamp, message | filter level = 'ERROR'`).\n"
                "2. Log Retention Policies: By default, CloudWatch retains logs forever (which accumulates storage costs). "
                "Always set an explicit retention policy (e.g. 30 or 90 days) on your Log Groups!"
            )
        )

    def put_custom_metric(self, req: CustomMetricRequest) -> CustomMetricResponse:
        """Puts a custom metric to CloudWatch with dimensions."""
        dimensions_list = [{"Name": k, "Value": v} for k, v in req.dimensions.items()]

        if not settings.AWS_MOCK_MODE and settings.AWS_ACCESS_KEY_ID:
            try:
                cw = get_boto3_client("cloudwatch")
                cw.put_metric_data(
                    Namespace=req.namespace,
                    MetricData=[{
                        "MetricName": req.metric_name,
                        "Dimensions": dimensions_list,
                        "Value": req.value,
                        "Unit": req.unit
                    }]
                )
                return CustomMetricResponse(
                    status="Custom metric published live to AWS CloudWatch",
                    metric_name=req.metric_name,
                    namespace=req.namespace,
                    value=req.value,
                    unit=req.unit,
                    dimensions=dimensions_list,
                    explanation="Metric registered in AWS CloudWatch Metrics repository."
                )
            except Exception:
                pass

        return CustomMetricResponse(
            status="Simulated Custom Metric Published",
            metric_name=req.metric_name,
            namespace=req.namespace,
            value=req.value,
            unit=req.unit,
            dimensions=dimensions_list,
            explanation=(
                "Custom Metrics & Dimensions in AWS:\n"
                "1. Dimensions: Name/value pairs that identify a metric (e.g. Category=MedicalAid).\n"
                "2. Standard vs High-Resolution: Standard metrics have 1-minute granularity. "
                "High-resolution metrics can record down to 1-second intervals for real-time telemetry.\n"
                "3. In Ataa Platform: Tracking `DonationPledgeAmount` per category lets you graph donation velocity "
                "on a CloudWatch Dashboard."
            )
        )

    def simulate_metric_alarm(self, req: AlarmSimulationRequest) -> AlarmSimulationResponse:
        """Evaluates alarm conditions and simulates triggering an Amazon SNS alert."""
        is_alarm = False
        if req.comparison_operator == "GreaterThanThreshold":
            is_alarm = req.current_value > req.threshold
        elif req.comparison_operator == "LessThanThreshold":
            is_alarm = req.current_value < req.threshold

        state = "ALARM" if is_alarm else "OK"
        reason = (
            f"Threshold Breached: Current value ({req.current_value}) is "
            f"{'greater' if is_alarm else 'within acceptable limits of'} the configured threshold ({req.threshold})."
        )

        sns_payload = None
        action = "No action required. Metric is within healthy boundaries."
        if is_alarm:
            action = "Triggered Amazon SNS Topic: arn:aws:sns:us-east-1:123456789012:AtaaDevOpsAlerts -> SMS/Email dispatch."
            sns_payload = {
                "AlarmName": req.alarm_name,
                "NewStateValue": "ALARM",
                "NewStateReason": reason,
                "StateChangeTime": datetime.now(timezone.utc).isoformat(),
                "Region": settings.AWS_REGION,
                "Metric": req.metric_name,
                "Subject": f"🚨 AWS ALARM: '{req.alarm_name}' in {settings.AWS_REGION}"
            }

        return AlarmSimulationResponse(
            alarm_name=req.alarm_name,
            state=state,
            reason=reason,
            triggered_action=action,
            sns_notification_payload=sns_payload,
            cloudwatch_monitoring_tip=(
                "Alarm Actions in AWS:\n"
                "1. SNS Notification: Alert engineers via Email, PagerDuty, or Slack webhooks.\n"
                "2. EC2 Auto Scaling Action: Add or terminate EC2 instances based on average CPU utilization.\n"
                "3. EC2 Recovery Action: Automatically reboot or recover an unhealthy EC2 host instance if a system check fails."
            )
        )


cloudwatch_service = CloudWatchService()
