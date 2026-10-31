"""Direct Unit Tests for all AWS Training Modules."""
import pytest
from main import health_check
from modules.iam.router import (
    audit_credentials,
    evaluate_policy,
    get_auth_vs_authz_guide,
    simulate_assume_role,
)
from modules.iam.schemas import (
    AssumeRoleRequest,
    CredentialAuditRequest,
    PolicyEvaluationRequest,
)
from modules.ec2_security.router import (
    get_ec2_pricing_guide,
    simulate_imds_v2,
    test_security_group_traffic as api_test_security_group_traffic,
)
from modules.ec2_security.schemas import IMDSRequest, TrafficTestRequest
from modules.secrets_config.router import (
    compare_secrets_options,
    get_secrets_manager_secret,
    get_ssm_parameter,
)
from modules.secrets_config.schemas import ParameterGetRequest, SecretGetRequest
from modules.s3_storage.router import (
    create_bucket,
    generate_presigned_url,
    get_storage_classes,
    upload_object,
)
from modules.s3_storage.schemas import (
    CreateBucketRequest,
    PresignedUrlRequest,
    UploadObjectRequest,
)
from modules.cloudwatch.router import (
    put_custom_metric,
    put_log_event,
    simulate_metric_alarm,
)
from modules.cloudwatch.schemas import (
    AlarmSimulationRequest,
    CustomMetricRequest,
    LogEventRequest,
)
from modules.vpc_networking.router import (
    calculate_subnets,
    get_vpc_endpoints_guide,
    route_packet,
)
from modules.vpc_networking.schemas import PacketRouteRequest, SubnetCalculationRequest
from modules.docker_lab.router import (
    explain_port_mapping,
    get_docker_fundamentals,
    get_production_dockerfile,
)
from modules.docker_lab.schemas import PortMappingExplainRequest
from modules.advanced_compute.router import (
    compare_compute_options,
    generate_ecs_task_definition,
    get_kubernetes_concepts,
)
from modules.advanced_compute.schemas import ECSTaskDefRequest


# Health Check
def test_health():
    res = health_check()
    assert res["status"] == "healthy"
    assert "aws_mode" in res


# IAM Module
def test_iam_auth_vs_authz():
    res = get_auth_vs_authz_guide()
    assert "authentication" in res
    assert "authorization" in res
    assert res["authentication"]["http_status"].startswith("401")
    assert res["authorization"]["http_status"].startswith("403")


def test_iam_evaluate_policy_allow():
    req = PolicyEvaluationRequest(
        user_or_role="AtaaEC2Role",
        action="s3:PutObject",
        resource_arn="arn:aws:s3:::ataa-verification-documents/cases/medical.pdf"
    )
    res = evaluate_policy(req)
    assert res.allowed is True
    assert res.is_least_privilege_compliant is True


def test_iam_evaluate_policy_deny():
    req = PolicyEvaluationRequest(
        user_or_role="AtaaEC2Role",
        action="s3:DeleteObject",
        resource_arn="arn:aws:s3:::ataa-verification-documents/cases/medical.pdf"
    )
    res = evaluate_policy(req)
    assert res.allowed is False
    assert "Deny" in res.decision_reason


def test_iam_assume_role():
    req = AssumeRoleRequest(role_arn="arn:aws:iam::123456789012:role/TestRole")
    res = simulate_assume_role(req)
    assert res.access_key_id.startswith("ASIA")
    assert "expiration" in res.model_dump()


def test_iam_credential_auditor():
    req = CredentialAuditRequest(
        code_or_config_snippet="AWS_ACCESS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE'"
    )
    res = audit_credentials(req)
    assert res.found_secrets is True
    assert res.risk_level == "CRITICAL"


# EC2 & Security Groups
def test_ec2_security_groups():
    # Public to ALB
    res_alb = api_test_security_group_traffic(
        TrafficTestRequest(source="Internet", destination_target="ALB", destination_port=443)
    )
    assert res_alb.traffic_allowed is True
    assert res_alb.is_stateful_response_allowed is True

    # Internet to EC2 (blocked)
    res_ec2_blocked = api_test_security_group_traffic(
        TrafficTestRequest(source="Internet", destination_target="EC2", destination_port=8000)
    )
    assert res_ec2_blocked.traffic_allowed is False

    # ALB to EC2 (allowed)
    res_ec2_allowed = api_test_security_group_traffic(
        TrafficTestRequest(source="sg-alb-public-ingress", destination_target="EC2", destination_port=8000)
    )
    assert res_ec2_allowed.traffic_allowed is True


def test_ec2_imds_v2():
    res = simulate_imds_v2(IMDSRequest(role_name="AtaaRole"))
    assert "IMDSv2" in res.imds_version
    assert "Token" in res.credentials


def test_ec2_pricing_guide():
    res = get_ec2_pricing_guide()
    assert "instance_families" in res
    assert "pricing_models" in res


# Secrets & Environment Variables
def test_secrets_ssm():
    res = get_ssm_parameter(ParameterGetRequest(parameter_path="/ataa/prod/db/url"))
    assert res.type == "SecureString"
    assert "postgresql://" in res.value


def test_secrets_manager():
    res = get_secrets_manager_secret(SecretGetRequest(secret_id="ataa/prod/jwt"))
    assert res.rotation_enabled is True
    assert "secret_value" in res.model_dump()


def test_secrets_comparison():
    res = compare_secrets_options()
    assert "Plain .env file" in res.comparison_table
    assert "AWS Secrets Manager" in res.comparison_table


# S3 Object Storage
def test_s3_bucket_and_upload():
    b_res = create_bucket(CreateBucketRequest(bucket_name="test-ataa-bucket"))
    assert b_res.public_access_blocked is True
    assert b_res.versioning_status == "Enabled"

    u_res = upload_object(UploadObjectRequest(bucket_name="test-ataa-bucket", object_key="doc.pdf"))
    assert "s3_uri" in u_res.model_dump()
    assert "https_url" in u_res.model_dump()


def test_s3_presigned_url():
    req = PresignedUrlRequest(bucket_name="test-bucket", object_key="receipt.pdf", operation="put_object")
    res = generate_presigned_url(req)
    assert "presigned_url" in res.model_dump()
    assert res.http_method == "PUT"
    assert res.expires_in_seconds == 900


def test_s3_storage_classes():
    res = get_storage_classes()
    assert "S3 Standard" in res.classes
    assert "S3 Glacier Deep Archive" in res.classes


# CloudWatch & Logs
def test_cloudwatch_logging_and_metrics():
    l_res = put_log_event(LogEventRequest(message="Test log message"))
    assert "timestamp" in l_res.model_dump()

    m_res = put_custom_metric(CustomMetricRequest(metric_name="DonationCount", value=1.0))
    assert m_res.value == 1.0


def test_cloudwatch_alarm():
    req = AlarmSimulationRequest(
        metric_name="5xxErrors",
        threshold=5.0,
        current_value=8.2,
        comparison_operator="GreaterThanThreshold"
    )
    res = simulate_metric_alarm(req)
    assert res.state == "ALARM"
    assert res.sns_notification_payload is not None


# VPC & Networking
def test_vpc_subnet_reserved_ips():
    res = calculate_subnets(SubnetCalculationRequest(cidr_block="10.0.1.0/24"))
    assert res.total_ips == 256
    assert res.aws_reserved_ips == 5
    assert res.usable_ips == 251


def test_vpc_routing():
    # Private to S3
    res_s3 = route_packet(PacketRouteRequest(
        source_subnet_type="Private Subnet (EC2)",
        destination="Amazon S3 (Upload Document)"
    ))
    assert res_s3.uses_vpc_endpoint is True
    assert res_s3.requires_nat_gateway is False

    # Private to Internet
    res_inet = route_packet(PacketRouteRequest(
        source_subnet_type="Private Subnet (EC2)",
        destination="Internet (apt-get update / docker pull)"
    ))
    assert res_inet.requires_nat_gateway is True


def test_vpc_endpoints_guide():
    res = get_vpc_endpoints_guide()
    assert "ONLY Amazon S3 and Amazon DynamoDB" in res.gateway_endpoints["Supported Services"]


# Docker Lab
def test_docker_refresher():
    res = get_docker_fundamentals()
    assert "Docker Image" in res.images_vs_containers
    assert "Docker Container" in res.images_vs_containers


def test_docker_port_mapping():
    res = explain_port_mapping(PortMappingExplainRequest(host_port=8080, container_port=8000))
    assert res.docker_flag == "-p 8080:8000"
    assert "localhost:8080" in res.host_access_url


def test_dockerfile_guide():
    res = get_production_dockerfile()
    assert "FROM python:3.13-slim" in res.recommended_dockerfile
    assert "USER appuser" in res.recommended_dockerfile


# Advanced Compute
def test_advanced_compute():
    matrix = compare_compute_options()
    assert "ECS Fargate (Serverless Containers)" in matrix.decision_matrix

    task_def = generate_ecs_task_definition(ECSTaskDefRequest())
    assert task_def.task_definition_json["networkMode"] == "awsvpc"

    k8s = get_kubernetes_concepts()
    assert "Pod" in k8s.abstractions
