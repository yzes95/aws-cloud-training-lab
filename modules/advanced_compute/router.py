from typing import Any, Dict
from fastapi import APIRouter
from .schemas import ECSTaskDefRequest
from .service import advanced_compute_service

router = APIRouter(prefix="/api/v1/advanced", tags=["🚀 Advanced Compute: ECS, Fargate & Kubernetes"])


@router.get("/compute-options-comparison", summary="EC2 vs ECS vs Fargate vs EKS")
def compare_compute_options() -> Dict[str, Any]:
    """Comparison matrix for AWS container compute."""
    return advanced_compute_service.compare_compute_options()


@router.post("/generate-ecs-task-def", summary="Generate ECS Task Definition JSON for Fargate")
def generate_ecs_task_definition(request: ECSTaskDefRequest) -> Dict[str, Any]:
    """Generate ECS Task Definition JSON."""
    return advanced_compute_service.generate_ecs_task_definition(request)


@router.get("/kubernetes-fundamentals-guide", summary="Docker to Kubernetes Mapping")
def get_kubernetes_concepts() -> Dict[str, Any]:
    """Docker concepts mapped to Kubernetes abstractions."""
    return advanced_compute_service.get_kubernetes_concepts_guide()
