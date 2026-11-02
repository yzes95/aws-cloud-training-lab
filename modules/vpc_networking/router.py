from typing import Any, Dict
from fastapi import APIRouter
from .schemas import PacketRouteRequest, SubnetCalculationRequest
from .service import vpc_service

router = APIRouter(prefix="/api/v1/vpc", tags=["🌐 VPC & Cloud Networking"])


@router.post("/calculate-subnets", summary="Subnet CIDR Calculator & AWS 5 Reserved IPs")
def calculate_subnets(request: SubnetCalculationRequest) -> Dict[str, Any]:
    """Calculate total vs usable IP addresses."""
    return vpc_service.calculate_subnet_ips(request)


@router.post("/route-packet", summary="Trace Packet Route (IGW vs NAT Gateway vs VPC Endpoints)")
def route_packet(request: PacketRouteRequest) -> Dict[str, Any]:
    """Trace route of network packet."""
    return vpc_service.trace_packet_route(request)


@router.get("/vpc-endpoints-guide", summary="VPC Endpoints Summary (Gateway vs Interface)")
def get_vpc_endpoints_guide() -> Dict[str, Any]:
    """Summary of VPC Gateway and Interface Endpoints."""
    return vpc_service.get_vpc_endpoints_guide()
