from typing import Any, Dict
from core.aws_client import get_boto3_client
from .schemas import PacketRouteRequest, SubnetCalculationRequest


class VPCNetworkingService:
    """Service stubs for VPC, Subnets, Routing, and Gateways."""

    def calculate_subnet_ips(self, req: SubnetCalculationRequest) -> Dict[str, Any]:
        # TODO: Calculate CIDR IP count and subtract the 5 AWS reserved IPs (.0, .1, .2, .3, .255)
        # Python's built-in `ipaddress` module can be used: ipaddress.ip_network(req.cidr_block)
        raise NotImplementedError("TODO: Implement CIDR calculation logic.")

    def trace_packet_route(self, req: PacketRouteRequest) -> Dict[str, Any]:
        # TODO: Trace or describe packet journey (IGW vs NAT Gateway vs S3 VPC Gateway Endpoint)
        raise NotImplementedError("TODO: Implement packet routing simulation.")

    def get_vpc_endpoints_guide(self) -> Dict[str, Any]:
        # TODO: Return comparison of S3 Gateway Endpoints (free route table entries) vs Interface Endpoints (PrivateLink)
        raise NotImplementedError("TODO: Implement VPC endpoints guide.")


vpc_service = VPCNetworkingService()
