from fastapi import APIRouter
from .schemas import (
    PacketRouteRequest,
    PacketRouteResponse,
    SubnetCalculationRequest,
    SubnetCalculationResponse,
    VpcEndpointsGuideResponse,
)
from .service import vpc_service

router = APIRouter(prefix="/api/v1/vpc", tags=["🌐 VPC & Cloud Networking"])


@router.post(
    "/calculate-subnets",
    summary="Subnet CIDR Calculator: Reserved vs Usable IP Addresses",
    response_model=SubnetCalculationResponse
)
def calculate_subnets(request: SubnetCalculationRequest):
    """Calculates usable vs AWS-reserved IP addresses for any CIDR block:
    - Demonstrates why AWS reserves 5 IP addresses per subnet (.0, .1, .2, .3, .255)
    - Key topic for AWS Certified Cloud Practitioner and Solutions Architect exams
    """
    return vpc_service.calculate_subnet_ips(request)


@router.post(
    "/route-packet",
    summary="Trace Network Packet Path (IGW vs NAT Gateway vs VPC Endpoints)",
    response_model=PacketRouteResponse
)
def route_packet(request: PacketRouteRequest):
    """Traces packet flow from public or private subnets to Internet, S3, or RDS:
    - Demonstrates when a NAT Gateway is required for private compute
    - Demonstrates how S3 Gateway Endpoints bypass the internet completely for free
    """
    return vpc_service.trace_packet_route(request)


@router.get(
    "/vpc-endpoints-guide",
    summary="VPC Endpoints Guide: Gateway vs Interface (PrivateLink)",
    response_model=VpcEndpointsGuideResponse
)
def get_vpc_endpoints_guide():
    """Provides a clear breakdown comparing S3/DynamoDB Gateway Endpoints (free route table entries)
    against Interface Endpoints powered by AWS PrivateLink.
    """
    return vpc_service.get_vpc_endpoints_guide()
