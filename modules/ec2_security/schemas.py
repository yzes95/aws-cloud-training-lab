from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TrafficTestRequest(BaseModel):
    source: str = Field(default="Internet (0.0.0.0/0)", description="Source of the incoming traffic: 'Internet', 'ALB-SG', 'EC2-SG', or custom IP")
    destination_target: str = Field(default="EC2", description="Target destination: 'ALB', 'EC2', or 'RDS'")
    destination_port: int = Field(default=8000, description="Destination TCP port (e.g. 443, 8000, 5432, 22)")
    protocol: str = Field(default="tcp", description="Network protocol: tcp, udp, icmp")


class TrafficTestResponse(BaseModel):
    traffic_allowed: bool
    status_code: str
    security_group_applied: str
    rule_matched: Optional[str]
    is_stateful_response_allowed: bool
    explanation: str
    security_architecture_note: str


class IMDSRequest(BaseModel):
    role_name: str = Field(default="Ataa-EC2-Backend-Role", description="IAM Role attached to EC2 via Instance Profile")


class IMDSResponse(BaseModel):
    imds_version: str
    token_header_required: str
    endpoint: str
    role_name: str
    credentials: Dict[str, Any]
    security_explanation: str
