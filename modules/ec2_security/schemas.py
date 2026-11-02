from pydantic import BaseModel, Field


class TrafficTestRequest(BaseModel):
    source: str = Field(default="0.0.0.0/0")
    destination_target: str = Field(default="EC2")
    destination_port: int = Field(default=8000)
    protocol: str = Field(default="tcp")


class IMDSRequest(BaseModel):
    role_name: str = Field(default="MyEC2Role")
