from typing import Any, Dict, List
from pydantic import BaseModel, Field


class SubnetCalculationRequest(BaseModel):
    cidr_block: str = Field(default="10.0.1.0/24", description="Subnet CIDR block (e.g. 10.0.1.0/24, 10.0.0.0/16)")


class SubnetCalculationResponse(BaseModel):
    cidr_block: str
    total_ips: int
    aws_reserved_ips: int
    usable_ips: int
    reserved_breakdown: Dict[str, str]
    aws_exam_tip: str


class PacketRouteRequest(BaseModel):
    source_subnet_type: str = Field(
        default="Private Subnet (EC2)",
        description="'Public Subnet (ALB)', 'Private Subnet (EC2)', or 'Private Subnet (RDS)'"
    )
    destination: str = Field(
        default="Internet (apt-get update / docker pull)",
        description="'Internet (apt-get update)', 'Amazon S3 (Upload Document)', 'Internal RDS (5432)', or 'Inbound Client'"
    )


class PacketRouteResponse(BaseModel):
    route_path: List[str]
    gateways_crossed: List[str]
    can_traffic_succeed: bool
    requires_nat_gateway: bool
    uses_vpc_endpoint: bool
    explanation: str
    cost_optimization_tip: str


class VpcEndpointsGuideResponse(BaseModel):
    gateway_endpoints: Dict[str, Any]
    interface_endpoints: Dict[str, Any]
    cost_comparison: str
