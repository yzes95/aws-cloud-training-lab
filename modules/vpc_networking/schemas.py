from pydantic import BaseModel, Field


class SubnetCalculationRequest(BaseModel):
    cidr_block: str = Field(default="10.0.1.0/24")


class PacketRouteRequest(BaseModel):
    source_subnet_type: str = Field(default="Private Subnet (EC2)")
    destination: str = Field(default="Internet (apt-get update / docker pull)")
