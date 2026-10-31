"""AWS Cloud Training Lab - Interactive API.

A standalone FastAPI project designed for hands-on learning, testing, and experimenting
with individual Amazon Web Services (AWS) and Docker fundamentals using Swagger UI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from modules.iam import router as iam_router
from modules.ec2_security import router as ec2_router
from modules.secrets_config import router as secrets_router
from modules.s3_storage import router as s3_router
from modules.cloudwatch import router as cloudwatch_router
from modules.vpc_networking import router as vpc_router
from modules.docker_lab import router as docker_router
from modules.advanced_compute import router as advanced_router

tags_metadata = [
    {
        "name": "Health",
        "description": "Lab runtime health check, active AWS mode (Mock vs Real AWS), and environment details."
    },
    {
        "name": "🔐 IAM & Least Privilege",
        "description": "High Priority: IAM Users vs Roles, Policies evaluation, Principle of Least Privilege, STS Temporary Credentials (`ASIA`), and static credential leak audit."
    },
    {
        "name": "🖥️ EC2 & Security Groups",
        "description": "High Priority: Stateful Security Group rule simulation, Ingress/Egress packet filtering, IMDSv2 token session defense, and EC2 compute families/pricing."
    },
    {
        "name": "🔑 Secrets & Environment Variables",
        "description": "High Priority: SSM Parameter Store, AWS Secrets Manager with automated rotation, and comparison against plain `.env` files."
    },
    {
        "name": "🪣 S3 Object Storage",
        "description": "Medium Priority: Bucket operations, versioning, Block Public Access, presigned URLs (direct client upload), and Storage Classes lifecycle."
    },
    {
        "name": "📊 CloudWatch & Logs",
        "description": "Medium Priority: Structured JSON logging, custom metrics with multidimensional tagging, and CloudWatch Metric Alarms with SNS notification dispatch."
    },
    {
        "name": "🌐 VPC & Cloud Networking",
        "description": "Medium Priority: Subnet CIDR calculation (AWS 5 reserved IPs), Route Tables, Internet Gateway (IGW) vs NAT Gateway, and free S3 Gateway Endpoints."
    },
    {
        "name": "🐳 Docker Fundamentals & Containers",
        "description": "Refresher: Images vs Containers, Container port mapping (`-p host:container`), multi-stage Dockerfiles, layer caching, and dev-vs-prod consistency."
    },
    {
        "name": "🚀 Advanced Compute: ECS, Fargate & Kubernetes",
        "description": "Low Priority: ECS on EC2 vs Serverless Fargate vs EKS, ECS Task Definition generation, Task Role vs Execution Role, and Docker-to-Kubernetes analogies."
    },
]

app = FastAPI(
    title=settings.APP_NAME,
    description="""
# ☁️ AWS Cloud Training Lab & Service Playground

Welcome to your hands-on AWS training project! This application allows you to write, test,
and experiment with individual AWS services one-by-one with **zero frontend needed** — simply use the interactive
Swagger UI (`/docs`) below.

### 🎯 Key Capabilities:
- **Dual Testing Mode**: Run offline for **100% FREE** with built-in mock simulation, or connect to **LocalStack** or **Real AWS** by toggling `AWS_MOCK_MODE` in `.env`.
- **Architectural Link to Ataa Donation Platform**: Every module demonstrates the exact patterns used in the Ataa production architecture (e.g. S3 presigned URLs for family medical receipts, EC2 Instance Profiles for zero hardcoded keys, and CloudWatch telemetry).
- **Curated AWS CCP & SAA Topics**: Directly covers IAM, EC2, Security Groups, VPC, S3, Secrets Manager, CloudWatch, and Docker fundamentals.
    """,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware (allows local Swagger UI and API tools like Postman/cURL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint showing current lab configuration and active AWS connection mode."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "aws_mode": "Offline Mock Simulation (Free)" if settings.AWS_MOCK_MODE else "Live AWS / LocalStack",
        "aws_region": settings.AWS_REGION,
        "swagger_docs": "/docs",
        "redoc_docs": "/redoc"
    }


# Include all AWS training routers
app.include_router(iam_router)
app.include_router(ec2_router)
app.include_router(secrets_router)
app.include_router(s3_router)
app.include_router(cloudwatch_router)
app.include_router(vpc_router)
app.include_router(docker_router)
app.include_router(advanced_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
