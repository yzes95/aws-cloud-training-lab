"""AWS Cloud Training Lab - Interactive Service API."""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
    {"name": "Health", "description": "Lab runtime health check."},
    {"name": "🔐 IAM & Least Privilege", "description": "IAM Users, Roles, Policies, STS, and Credentials Security."},
    {"name": "🖥️ EC2 & Security Groups", "description": "Security Groups, Stateful filtering, and IMDSv2."},
    {"name": "🔑 Secrets & Environment Variables", "description": "SSM Parameter Store and AWS Secrets Manager."},
    {"name": "🪣 S3 Object Storage", "description": "S3 Buckets, Uploads, Presigned URLs, and Storage Classes."},
    {"name": "📊 CloudWatch & Logs", "description": "CloudWatch Logs, Custom Metrics, and Alarms."},
    {"name": "🌐 VPC & Cloud Networking", "description": "Subnets, CIDR calculation, Route Tables, and Endpoints."},
    {"name": "🐳 Docker Fundamentals & Containers", "description": "Docker images, containers, ports, and Dockerfiles."},
    {"name": "🚀 Advanced Compute: ECS, Fargate & Kubernetes", "description": "ECS Task Definitions and Orchestration concepts."},
]

app = FastAPI(
    title=settings.APP_NAME,
    description="Interactive Swagger UI for writing and testing AWS service integrations one-by-one.",
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Custom exception handler for unimplemented TODO service stubs
@app.exception_handler(NotImplementedError)
def not_implemented_handler(request: Request, exc: NotImplementedError):
    return JSONResponse(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        content={"detail": str(exc), "status": "TODO"}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint showing current lab configuration."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "aws_region": settings.AWS_REGION,
        "localstack_target": settings.LOCALSTACK_ENDPOINT_URL or "disabled (targeting real AWS)",
        "swagger_docs": "/docs",
        "redoc_docs": "/redoc"
    }


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
