from typing import Any, Dict, List
from .schemas import (
    DockerfileInspectionResponse,
    DockerFundamentalsGuideResponse,
    PortMappingExplainRequest,
    PortMappingExplainResponse,
)


class DockerLabService:
    """Service providing interactive training for Docker fundamentals, port mapping, and containerization."""

    def explain_port_mapping(self, req: PortMappingExplainRequest) -> PortMappingExplainResponse:
        """Visualizes and explains Docker container port mapping (-p host:container)."""
        cmd_flag = f"-p {req.host_port}:{req.container_port}"
        return PortMappingExplainResponse(
            docker_flag=cmd_flag,
            host_access_url=f"http://localhost:{req.host_port}/docs",
            container_internal_listener=f"0.0.0.0:{req.container_port}",
            how_traffic_flows=[
                f"1. A browser sends an HTTP request to the host machine: http://localhost:{req.host_port}",
                f"2. The host's Docker daemon network bridge intercepts traffic arriving on host port {req.host_port}",
                f"3. Docker forwards the raw packets via NAT into the container's isolated network namespace",
                f"4. The container's application (Uvicorn running on 0.0.0.0:{req.container_port}) receives and processes the request",
                "5. The response packets return along the reverse NAT path back to the client browser!"
            ],
            common_mistakes=[
                "Binding Uvicorn to 127.0.0.1 instead of 0.0.0.0: If Uvicorn listens on 127.0.0.1 inside a container, it ONLY accepts traffic from inside the container itself and Docker port mapping fails!",
                f"Mixing up host and container ports: `-p {req.host_port}:{req.container_port}` means `HOST:CONTAINER`. Reversing them causes 404 or connection refused.",
                "Port conflicts: If another app on your Windows PC is already using host port 8000, you can easily map `-p 8080:8000` without changing any Python code."
            ]
        )

    def get_production_dockerfile_guide(self) -> DockerfileInspectionResponse:
        """Returns a production-grade multi-stage Dockerfile for FastAPI with line-by-line explanation."""
        dockerfile_content = (
            "# Stage 1: Build & Dependencies\n"
            "FROM python:3.13-slim AS builder\n"
            "WORKDIR /app\n"
            "ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1\n"
            "RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*\n"
            "COPY requirements.txt .\n"
            "RUN pip install --no-cache-dir --user -r requirements.txt\n\n"
            "# Stage 2: Final Minimal Runtime Image\n"
            "FROM python:3.13-slim AS runner\n"
            "WORKDIR /app\n"
            "# Create non-root user for container security\n"
            "RUN useradd -u 1001 -m appuser\n"
            "# Copy only installed Python packages from builder stage\n"
            "COPY --from=builder /root/.local /home/appuser/.local\n"
            "COPY . .\n"
            "USER appuser\n"
            "ENV PATH=/home/appuser/.local/bin:$PATH\n"
            "EXPOSE 8000\n"
            'CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]\n'
        )

        layers = [
            {"FROM python:3.13-slim": "Uses minimal Debian-slim image (~150MB instead of full Python 1GB image)."},
            {"COPY requirements.txt . BEFORE COPY . .": "Takes advantage of Docker layer caching! Dependencies are only re-installed when requirements.txt changes, not on every code edit."},
            {"USER appuser": "Critical security rule: NEVER run containers as root in production! Running as non-root prevents container breakout attacks."},
            {"EXPOSE 8000": "Documentation flag informing orchestrators (ALB, ECS, Kubernetes) which port the container expects."},
            {"CMD uvicorn main:app --host 0.0.0.0": "Specifies default entrypoint command. Must bind to 0.0.0.0 to accept traffic forwarded from host port mapping."}
        ]

        return DockerfileInspectionResponse(
            recommended_dockerfile=dockerfile_content,
            layer_explanations=layers,
            security_best_practices=[
                "1. Multi-Stage Builds: Build tools (gcc, compilers) stay in Stage 1 and are not included in the final production image.",
                "2. Non-Root Execution: Enforce `USER appuser` to eliminate root privilege escalation risks.",
                "3. Pin Package Versions: Always specify versions in requirements.txt (e.g. `fastapi==0.115.0`) for deterministic builds.",
                "4. Use .dockerignore: Exclude `.venv/`, `.git/`, `.env`, and `__pycache__/` from the build context."
            ],
            caching_optimization_tips=[
                "Docker executes Dockerfiles from top to bottom, caching each layer.",
                "Always place instructions that change rarely (like `COPY requirements.txt` and `pip install`) BEFORE instructions that change frequently (like `COPY . .`)."
            ]
        )

    def get_fundamentals_guide(self) -> DockerFundamentalsGuideResponse:
        """Comprehensive refresher on Images vs Containers, Storage, and Environment Variables."""
        return DockerFundamentalsGuideResponse(
            images_vs_containers={
                "Docker Image": "A read-only, immutable blueprint or template containing the OS layer, runtime (Python 3.13), libraries, and application code. Think of it as a compiled class.",
                "Docker Container": "A running, isolated instance of a Docker image with a thin read/write layer on top. Think of it as an object instantiated from a class. You can run 10 containers from 1 single image simultaneously!"
            },
            persistent_storage={
                "Container Ephemeral Layer": "Default storage in a container is ephemeral. If the container is deleted, all newly created files in that container are permanently lost!",
                "Docker Volumes (`-v my-data:/app/data`)": "Managed directly by Docker on the host filesystem. Best for persistent databases (PostgreSQL data) and production storage.",
                "Bind Mounts (`-v ${PWD}:/app`)": "Mounts a specific folder from your host computer into the container. Ideal for active development with live code reload!"
            },
            environment_variables={
                "Inline flag (`-e KEY=VALUE`)": "Injects a single variable into the container at startup.",
                "Env file flag (`--env-file .env`)": "Loads a collection of environment variables from a local file without hardcoding them into the image.",
                "Security Note": "Never hardcode passwords or AWS keys into a Dockerfile via `ENV SECRET=xyz`, because anyone who pulls the image can read them with `docker history`!"
            },
            dev_vs_prod_consistency=(
                "Why Docker Solves 'It Works On My Machine':\n"
                "In traditional deployment, your laptop might have Windows + Python 3.13 + specific DLLs, "
                "while production EC2 runs Ubuntu 24.04 with different glibc versions. Docker packages "
                "the EXACT same Linux userland, Python runtime, and C dependencies into an identical container image. "
                "If it runs in Docker on Windows, it runs identically on EC2, ECS, or Kubernetes!"
            ),
            useful_commands_cheat_sheet={
                "Build image": "docker build -t ataa-training-backend:latest .",
                "Run container with port": "docker run -d -p 8000:8000 --name my-app ataa-training-backend",
                "List running containers": "docker ps",
                "View container live logs": "docker logs -f my-app",
                "Execute shell inside container": "docker exec -it my-app /bin/bash",
                "Stop and remove container": "docker stop my-app && docker rm my-app",
                "Start with docker-compose": "docker-compose up -d --build"
            }
        )


docker_lab_service = DockerLabService()
