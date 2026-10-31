from fastapi import APIRouter
from .schemas import (
    ComputeComparisonResponse,
    ECSTaskDefRequest,
    ECSTaskDefResponse,
    KubernetesBasicsResponse,
)
from .service import advanced_compute_service

router = APIRouter(prefix="/api/v1/advanced", tags=["🚀 Advanced Compute: ECS, Fargate & Kubernetes"])


@router.get(
    "/compute-options-comparison",
    summary="EC2 vs ECS on EC2 vs ECS Fargate vs EKS",
    response_model=ComputeComparisonResponse
)
def compare_compute_options():
    """Provides a decision matrix and cost-benefit analysis for container compute options in AWS."""
    return advanced_compute_service.compare_compute_options()


@router.post(
    "/generate-ecs-task-def",
    summary="Generate Production ECS Task Definition JSON for Fargate",
    response_model=ECSTaskDefResponse
)
def generate_ecs_task_definition(request: ECSTaskDefRequest):
    """Generates an AWS ECS Task Definition for containerized FastAPI deployment:
    - Explains Task Role vs Execution Role
    - Demonstrates native SSM secret injection into container environment
    """
    return advanced_compute_service.generate_ecs_task_definition(request)


@router.get(
    "/kubernetes-fundamentals-guide",
    summary="Docker to Kubernetes Mapping & Abstractions Guide",
    response_model=KubernetesBasicsResponse
)
def get_kubernetes_concepts():
    """Maps Docker CLI concepts to Kubernetes abstractions (Pods, Deployments, Services, Ingress)."""
    return advanced_compute_service.get_kubernetes_concepts_guide()
