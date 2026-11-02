from typing import Any, Dict
from fastapi import APIRouter
from .schemas import PortMappingRequest
from .service import docker_lab_service

router = APIRouter(prefix="/api/v1/docker", tags=["🐳 Docker Fundamentals & Containers"])


@router.get("/fundamentals-refresher", summary="Images vs Containers, Storage & Env Vars")
def get_docker_fundamentals() -> Dict[str, Any]:
    """Summary of Docker core concepts."""
    return docker_lab_service.get_fundamentals_guide()


@router.post("/port-mapping-explainer", summary="Port Mapping Simulator (-p host:container)")
def explain_port_mapping(request: PortMappingRequest) -> Dict[str, Any]:
    """Explain how host-to-container port mapping operates."""
    return docker_lab_service.explain_port_mapping(request)


@router.get("/production-dockerfile-guide", summary="Production Dockerfile Best Practices")
def get_production_dockerfile() -> Dict[str, Any]:
    """Multi-stage build and security best practices."""
    return docker_lab_service.get_production_dockerfile_guide()
