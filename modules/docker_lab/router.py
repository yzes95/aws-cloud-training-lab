from fastapi import APIRouter
from .schemas import (
    DockerfileInspectionResponse,
    DockerFundamentalsGuideResponse,
    PortMappingExplainRequest,
    PortMappingExplainResponse,
)
from .service import docker_lab_service

router = APIRouter(prefix="/api/v1/docker", tags=["🐳 Docker Fundamentals & Containers"])


@router.get(
    "/fundamentals-refresher",
    summary="Docker Fundamentals Guide: Images vs Containers, Storage & Env Vars",
    response_model=DockerFundamentalsGuideResponse
)
def get_docker_fundamentals():
    """Provides a refresher on Docker core concepts:
    - Images vs Containers
    - Persistent Storage (Volumes vs Bind Mounts)
    - Environment Variables & Security
    - Why Docker guarantees development-to-production consistency
    - Essential CLI cheat sheet
    """
    return docker_lab_service.get_fundamentals_guide()


@router.post(
    "/port-mapping-explainer",
    summary="Port Mapping Simulator (-p host:container)",
    response_model=PortMappingExplainResponse
)
def explain_port_mapping(request: PortMappingExplainRequest):
    """Simulates how `-p host_port:container_port` works under the hood with NAT and network namespaces:
    - Explains common mistakes (binding to 127.0.0.1 vs 0.0.0.0)
    - Traces packet journey from host browser into the isolated container
    """
    return docker_lab_service.explain_port_mapping(request)


@router.get(
    "/production-dockerfile-guide",
    summary="Production-Ready Dockerfile & Layer Caching Analysis",
    response_model=DockerfileInspectionResponse
)
def get_production_dockerfile():
    """Returns an optimized multi-stage Dockerfile for FastAPI with line-by-line breakdown:
    - Layer caching optimization
    - Non-root user security enforcement
    - Build vs runtime image separation
    """
    return docker_lab_service.get_production_dockerfile_guide()
