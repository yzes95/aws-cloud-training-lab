from typing import Any, Dict
from .schemas import (
    ComputeComparisonResponse,
    ECSTaskDefRequest,
    ECSTaskDefResponse,
    KubernetesBasicsResponse,
)


class AdvancedComputeService:
    """Service providing training on ECS, Fargate vs EC2, ALB Routing, and Kubernetes fundamentals."""

    def compare_compute_options(self) -> ComputeComparisonResponse:
        """Compares EC2, ECS on EC2, ECS Fargate, and EKS."""
        return ComputeComparisonResponse(
            decision_matrix={
                "EC2 (Virtual Machine)": {
                    "Type": "Infrastructure as a Service (IaaS)",
                    "Management Overhead": "High (You manage OS patching, Docker daemon, security updates, SSH)",
                    "Scaling Speed": "Minutes (must boot full VM)",
                    "Best For": "Predictable continuous workloads, total OS control, learning cloud fundamentals"
                },
                "ECS on EC2 (Container Orchestration)": {
                    "Type": "AWS Native Container Orchestration",
                    "Management Overhead": "Medium (AWS manages container placement, you manage EC2 instances)",
                    "Scaling Speed": "Fast if EC2 cluster has spare capacity",
                    "Best For": "High-density container packing to maximize server utilization"
                },
                "ECS Fargate (Serverless Containers)": {
                    "Type": "Serverless Container Compute",
                    "Management Overhead": "Lowest (Zero servers to manage, patch, or monitor)",
                    "Scaling Speed": "Seconds to minutes per container task",
                    "Best For": "Production containerized microservices without DevOps server management"
                },
                "Amazon EKS (Managed Kubernetes)": {
                    "Type": "Enterprise Kubernetes as a Service",
                    "Management Overhead": "Very High (Requires deep Kubernetes expertise: YAML manifests, Helm, CNI, CRDs)",
                    "Scaling Speed": "Fast via Cluster Autoscaler and Karpenter",
                    "Best For": "Multi-cloud enterprise applications running hundreds of microservices"
                }
            },
            when_to_use_what=(
                "Architecture Decision Guide for Yahya's Projects:\n"
                "1. For Learning / Portfolio (Ataa Now): EC2 + Docker gives you hands-on OS experience, "
                "understanding ports, systemd, and SSH.\n"
                "2. For Modern Production: Migrate from EC2 to AWS ECS Fargate. You write your Dockerfile, "
                "push to AWS ECR, and Fargate runs the container without you ever patching a Linux kernel!\n"
                "3. Don't start with Kubernetes for a simple API: Kubernetes introduces massive complexity "
                "that is overkill for small-to-medium teams."
            ),
            cost_tradeoff=(
                "Cost Analysis:\n"
                "- EC2 t2.micro / t3.micro: ~$8.50 - $10 / month (or Free Tier for 12 months).\n"
                "- ECS Fargate (0.25 vCPU, 0.5GB RAM running 24/7): ~$9.50 / month.\n"
                "- EKS Control Plane: $73 / month JUST for the cluster fee before any compute!"
            )
        )

    def generate_ecs_task_definition(self, req: ECSTaskDefRequest) -> ECSTaskDefResponse:
        """Generates a production AWS ECS Task Definition JSON for Fargate."""
        task_def = {
            "family": req.family_name,
            "networkMode": "awsvpc",
            "requiresCompatibilities": ["FARGATE"],
            "cpu": req.cpu,
            "memory": req.memory,
            "taskRoleArn": req.task_role_arn,
            "executionRoleArn": req.execution_role_arn,
            "containerDefinitions": [
                {
                    "name": req.container_name,
                    "image": req.image_uri,
                    "essential": True,
                    "portMappings": [
                        {
                            "containerPort": req.container_port,
                            "hostPort": req.container_port,
                            "protocol": "tcp"
                        }
                    ],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": f"/ecs/{req.family_name}",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "fastapi"
                        }
                    },
                    "environment": [
                        {"name": "APP_ENV", "value": "production"},
                        {"name": "DEBUG", "value": "false"}
                    ],
                    "secrets": [
                        {
                            "name": "DATABASE_URL",
                            "valueFrom": "arn:aws:ssm:eu-central-1:123456789012:parameter/ataa/prod/database/url"
                        }
                    ]
                }
            ]
        }

        return ECSTaskDefResponse(
            task_definition_json=task_def,
            explanation=(
                "ECS Task Definition Anatomy:\n"
                "1. `networkMode: awsvpc`: Every container gets its own Elastic Network Interface (ENI) "
                "and private IP in your VPC. This allows Security Groups to be applied directly to individual containers!\n"
                "2. `secrets.valueFrom`: ECS natively pulls secrets from SSM Parameter Store or Secrets Manager "
                "before starting the container, injecting them directly into container environment variables without storing them in image files."
            ),
            task_role_vs_execution_role=(
                "CRITICAL DISTINCTION: Task Role vs Execution Role:\n"
                "- `executionRoleArn`: Used by the ECS AGENT to pull the Docker image from ECR and create CloudWatch log streams. (Infrastructure permissions).\n"
                "- `taskRoleArn`: Used by YOUR PYTHON APPLICATION CODE inside the container to make AWS API calls (e.g. S3 PutObject, DynamoDB query). (Application permissions)."
            )
        )

    def get_kubernetes_concepts_guide(self) -> KubernetesBasicsResponse:
        """Maps Docker concepts to Kubernetes abstractions."""
        return KubernetesBasicsResponse(
            abstractions={
                "Pod": "The smallest deployable unit in K8s. Usually contains ONE container (plus optional sidecar containers). Pods share network IP and localhost.",
                "ReplicaSet": "Ensures that a specified number of identical Pod instances (e.g. 3 copies of FastAPI) are running at all times.",
                "Deployment": "The standard workload resource. Manages declarative rolling updates, rollbacks, and ReplicaSets.",
                "Service (ClusterIP / NodePort / LoadBalancer)": "Provides a persistent internal IP and DNS name to load-balance traffic across dynamic ephemeral Pods.",
                "Ingress": "Manages external HTTP/HTTPS routing into internal Services (similar to AWS ALB).",
                "ConfigMap & Secret": "Decouples configuration and sensitive tokens from container images."
            },
            docker_to_k8s_analogy={
                "Dockerfile / Image": "Remains identical! Kubernetes runs standard OCI Docker images.",
                "`docker run -d my-app`": "In Kubernetes -> `kubectl create deployment my-app --image=...`",
                "`docker run -p 80:80`": "In Kubernetes -> `kubectl expose deployment my-app --port=80 --type=LoadBalancer`",
                "`docker-compose.yml`": "In Kubernetes -> Helm Chart or Kustomize manifest files."
            },
            learning_roadmap=(
                "Recommended Learning Sequence:\n"
                "1. Master single-host Docker (Building images, ports, volumes, compose) -> CURRENT STEP.\n"
                "2. Master AWS ECS & Fargate (Serverless container deployment without K8s overhead).\n"
                "3. Once comfortable with ECS, explore Kubernetes (Minikube / k3s locally, then Amazon EKS)."
            )
        )


advanced_compute_service = AdvancedComputeService()
