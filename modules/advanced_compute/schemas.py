from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ComputeComparisonResponse(BaseModel):
    decision_matrix: Dict[str, Any]
    when_to_use_what: str
    cost_tradeoff: str


class ECSTaskDefRequest(BaseModel):
    family_name: str = Field(default="ataa-backend-task", description="ECS Task Definition family name")
    container_name: str = Field(default="fastapi-app")
    image_uri: str = Field(default="123456789012.dkr.ecr.eu-central-1.amazonaws.com/ataa-backend:latest")
    cpu: str = Field(default="256", description="256 (.25 vCPU), 512 (.5 vCPU), 1024 (1 vCPU)")
    memory: str = Field(default="512", description="Memory in MiB")
    container_port: int = Field(default=8000)
    task_role_arn: str = Field(default="arn:aws:iam::123456789012:role/AtaaBackendTaskRole")
    execution_role_arn: str = Field(default="arn:aws:iam::123456789012:role/ecsTaskExecutionRole")


class ECSTaskDefResponse(BaseModel):
    task_definition_json: Dict[str, Any]
    explanation: str
    task_role_vs_execution_role: str


class KubernetesBasicsResponse(BaseModel):
    abstractions: Dict[str, Any]
    docker_to_k8s_analogy: Dict[str, str]
    learning_roadmap: str
