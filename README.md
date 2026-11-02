# AWS Training Lab

I built this project to train myself on AWS core services and cloud architecture patterns. 

Rather than deploying a frontend, I am using FastAPI and Swagger UI (`/docs`) as my interactive testing console. This lets me write code for one single AWS service at a time, test it directly with real boto3 calls (or LocalStack), and build my intuition for cloud engineering step by step.

Others are welcome to look through or fork this project, but it is primarily my personal training workspace.

## Current Status
- **Status:** Skeleton & learning workspace.
- Each module contains route declarations and Pydantic schemas, with service logic marked with `# TODO` so I can implement them myself.
- When an endpoint is called before I implement it, the API cleanly returns `501 Not Implemented`.
- Detailed study notes, concepts, and suggested boto3 calls are documented in [`LEARNING_PATH.md`](LEARNING_PATH.md).

## What I Am Covering & Priority

### High Priority
- **IAM:** Authentication vs Authorization, IAM Users vs Roles, Policies & Permissions, Least Privilege, Temporary Credentials (STS), why hardcoded AWS keys are dangerous.
- **EC2 & Security Groups:** Stateful Security Groups vs stateless NACLs, Instance Metadata Service v2 (IMDSv2) token flow, EC2 instance types and pricing models.
- **Secrets & Environment Variables:** SSM Parameter Store (SecureString with KMS) vs AWS Secrets Manager (automated rotation) vs `.env` files.

### Medium Priority
- **Amazon S3:** Bucket security (Block Public Access, Versioning, Encryption), Presigned URLs (direct client uploads without proxying bytes through the backend), Storage Classes & Lifecycle Rules.
- **CloudWatch & Logs:** Structured JSON logging, custom metrics with dimensions, metric alarms and SNS alert flows.
- **VPC Basics:** Subnets, CIDR notation (why AWS reserves 5 IP addresses per subnet), Internet Gateway vs NAT Gateway, and free S3 VPC Gateway Endpoints.

### Docker Refresher
- Images vs Containers, Dockerfiles (multi-stage builds, non-root users, layer caching), container port mapping (`-p host:container`), persistent storage (volumes vs bind mounts), environment variables.

### Low Priority / Advanced
- **Advanced Compute & Orchestration:** ECS Task Definitions (Task Role vs Execution Role), EC2 vs ECS Fargate vs EKS decision matrix, Docker to Kubernetes mapping.

## Relation to the Ataa Donation Platform
This lab is directly modeled around the architecture I designed for the [Ataa Donation Platform](https://github.com/yzes95/Donation-Platform) and its [Backend](https://github.com/yzes95/Donation-Platform-Backend):
- S3 presigned URLs in this lab mirror how Ataa allows donors and family representatives to upload medical documents directly to S3.
- The IAM role and IMDSv2 exercises mirror how the EC2 backend accesses S3 and CloudWatch without hardcoded credentials.
- The VPC and security group exercises mirror Ataa's private data subnets.

## Progress Checklist
- [ ] 1. IAM Users, Roles & Least Privilege Policies
- [ ] 2. Environment Variables, SSM Parameter Store & Secrets Manager
- [ ] 3. EC2, Security Groups & IMDSv2
- [ ] 4. Amazon S3 Buckets, Uploads & Presigned URLs
- [ ] 5. CloudWatch Logs, Custom Metrics & Alarms
- [ ] 6. VPC, Subnets, Routing & Endpoints
- [ ] 7. Dockerfile & Containerization
- [ ] 8. ECS Fargate Task Definition

## How I Run This Locally

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Linux/macOS: source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. Open the Swagger UI interactive playground:
   [http://localhost:8000/docs](http://localhost:8000/docs)

5. (Optional) Run against LocalStack:
   Set `LOCALSTACK_ENDPOINT_URL="http://localhost:4566"` in `.env`.

## License
MIT
