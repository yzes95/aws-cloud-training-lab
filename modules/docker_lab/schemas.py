from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PortMappingExplainRequest(BaseModel):
    host_port: int = Field(default=8080, description="Port exposed on the host machine (e.g. 8080, 80)")
    container_port: int = Field(default=8000, description="Internal port where Uvicorn/FastAPI listens inside the container")
    protocol: str = Field(default="tcp")


class PortMappingExplainResponse(BaseModel):
    docker_flag: str
    host_access_url: str
    container_internal_listener: str
    how_traffic_flows: List[str]
    common_mistakes: List[str]


class DockerfileInspectionResponse(BaseModel):
    recommended_dockerfile: str
    layer_explanations: List[Dict[str, str]]
    security_best_practices: List[str]
    caching_optimization_tips: List[str]


class DockerFundamentalsGuideResponse(BaseModel):
    images_vs_containers: Dict[str, str]
    persistent_storage: Dict[str, str]
    environment_variables: Dict[str, str]
    dev_vs_prod_consistency: str
    useful_commands_cheat_sheet: Dict[str, str]
