from typing import Any, Dict
from fastapi import APIRouter
from .schemas import IMDSRequest, TrafficTestRequest
from .service import ec2_service

router = APIRouter(prefix="/api/v1/ec2", tags=["🖥️ EC2 & Security Groups"])


@router.post("/security-group/test-traffic", summary="Test Security Group rules and stateful flow")
def test_security_group_traffic(request: TrafficTestRequest) -> Dict[str, Any]:
    """Test ingress and egress packet filtering through security groups."""
    return ec2_service.test_security_group_traffic(request)


@router.post("/imds-v2", summary="Demonstrate EC2 IMDSv2 token session")
def simulate_imds_v2(request: IMDSRequest) -> Dict[str, Any]:
    """Demonstrate IMDSv2 token flow for EC2 IAM role credentials."""
    return ec2_service.simulate_imds_v2(request)


@router.get("/instance-types-guide", summary="EC2 Instance types and pricing summary")
def get_ec2_pricing_guide() -> Dict[str, Any]:
    """Summary of EC2 instance types and pricing options."""
    return ec2_service.get_ec2_and_pricing_guide()
