from typing import Any, Dict
from .schemas import IMDSRequest, TrafficTestRequest


class EC2SecurityService:
    """Service stubs for EC2 and Security Groups training."""

    def test_security_group_traffic(self, req: TrafficTestRequest) -> Dict[str, Any]:
        # TODO: Simulate or test security group rules using boto3 ec2.describe_security_groups
        # Explain stateful inspection (inbound allowed -> outbound return traffic automatically allowed)
        raise NotImplementedError("TODO: Implement Security Group traffic test.")

    def simulate_imds_v2(self, req: IMDSRequest) -> Dict[str, Any]:
        # TODO: Explain or test IMDSv2 token session flow:
        # PUT http://169.254.169.254/latest/api/token -> GET /latest/meta-data/iam/security-credentials/<role>
        raise NotImplementedError("TODO: Implement IMDSv2 metadata demonstration.")

    def get_ec2_and_pricing_guide(self) -> Dict[str, Any]:
        # TODO: Return your summary of EC2 instance types and pricing models (On-Demand, Spot, Reserved)
        raise NotImplementedError("TODO: Implement EC2 pricing and instance guide.")


ec2_service = EC2SecurityService()
