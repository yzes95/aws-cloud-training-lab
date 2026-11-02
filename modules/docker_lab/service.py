from typing import Any, Dict
from .schemas import PortMappingRequest


class DockerLabService:
    """Service stubs for Docker fundamentals and exercises."""

    def get_fundamentals_guide(self) -> Dict[str, Any]:
        # TODO: Implement your summary of Docker Images vs Containers, Storage, and Environment Variables
        raise NotImplementedError("TODO: Implement Docker fundamentals guide.")

    def explain_port_mapping(self, req: PortMappingRequest) -> Dict[str, Any]:
        # TODO: Implement port mapping explanation (-p host:container)
        raise NotImplementedError("TODO: Implement port mapping explainer.")

    def get_production_dockerfile_guide(self) -> Dict[str, Any]:
        # TODO: Implement multi-stage Dockerfile best practices (layer caching, non-root user)
        raise NotImplementedError("TODO: Implement Dockerfile best practices guide.")


docker_lab_service = DockerLabService()
