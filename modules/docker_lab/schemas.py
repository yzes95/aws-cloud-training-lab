from pydantic import BaseModel, Field


class PortMappingRequest(BaseModel):
    host_port: int = Field(default=8080)
    container_port: int = Field(default=8000)
    protocol: str = Field(default="tcp")
