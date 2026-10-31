from typing import Any, Dict
from fastapi import APIRouter
from .schemas import (
    IMDSRequest,
    IMDSResponse,
    TrafficTestRequest,
    TrafficTestResponse,
)
from .service import ec2_service

router = APIRouter(prefix="/api/v1/ec2", tags=["🖥️ EC2 & Security Groups"])


@router.post(
    "/security-group/test-traffic",
    summary="Test Security Group Rules & Stateful Packet Flow",
    response_model=TrafficTestResponse
)
def test_security_group_traffic(request: TrafficTestRequest):
    """Simulates how AWS Security Groups filter inbound traffic across the 3-tier architecture:
    - Test Internet -> ALB (Port 443) -> Allowed
    - Test Internet -> EC2 (Port 8000) -> Blocked
    - Test ALB-SG -> EC2 (Port 8000) -> Allowed
    - Test EC2-SG -> RDS (Port 5432) -> Allowed
    - Explains why return response traffic is automatically allowed (Stateful inspection).
    """
    return ec2_service.test_security_group_traffic(request)


@router.post(
    "/imds-v2",
    summary="Simulate EC2 Instance Metadata Service v2 (IMDSv2)",
    response_model=IMDSResponse
)
def simulate_imds_v2(request: IMDSRequest):
    """Demonstrates how EC2 retrieves temporary IAM Role credentials via IMDSv2:
    - Explains token-based SSRF defense (`PUT` token session handshake)
    - Shows why applications on EC2 never need hardcoded AWS credentials
    """
    return ec2_service.simulate_imds_v2(request)


@router.get(
    "/instance-types-guide",
    summary="EC2 Instance Types, Pricing Models & Shared Responsibility Guide",
    response_model=Dict[str, Any]
)
def get_ec2_pricing_guide():
    """Returns an interactive guide to EC2 compute families (t3, c5, r5, m5),
    pricing strategies (On-Demand, Spot, Reserved, Savings Plans), and the AWS Shared Responsibility Model.
    """
    return ec2_service.get_ec2_and_pricing_guide()
