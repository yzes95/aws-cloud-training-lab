# ☁️ AWS Cloud Training Lab & Service Playground

<div align="center">

**A hands-on, modular FastAPI backend built for writing, testing, and mastering individual Amazon Web Services (AWS) and Docker fundamentals — with zero frontend required.**

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![AWS](https://img.shields.io/badge/AWS-Services_Playground-FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/Pytest-24_Passed-0A9EDC.svg?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Interactive API Docs (Swagger UI)](http://localhost:8000/docs) • [ReDoc](http://localhost:8000/redoc) • [Health Endpoint](http://localhost:8000/health)

</div>

---

## 📌 Project Overview & Purpose

This project is an **isolated, standalone engineering lab** designed specifically to help you write code for single AWS services, test them interactively, and build deep intuition for AWS cloud architecture without wrestling with frontend code or incurring unexpected cloud bills.

### 🌟 Why This Project Exists:
1. **Interactive Swagger UI Playground (`/docs`)**: You do not need to build any frontend UI. Every AWS service is exposed as an interactive endpoint in FastAPI's Swagger UI with parameters, schemas, and live execution.
2. **Dual-Mode Operation (100% Free Offline or Live AWS)**:
   - **Offline Mock Mode (`AWS_MOCK_MODE=true`)**: Train, test, and experiment offline for free with realistic AWS SDK responses — no AWS account or credit card required.
   - **Live AWS / LocalStack Mode (`AWS_MOCK_MODE=false`)**: Plug in your AWS credentials or run against LocalStack to execute live boto3 API calls against the cloud.
3. **Direct Architecture Bridge to Ataa Donation Platform**: Each module implements the exact security, storage, and networking patterns used in the [Ataa Family Donation Platform](https://github.com/yzes95/Donation-Platform).

---

## 🏗️ Architecture: How This Lab Maps to the Ataa Donation Platform

```
                            ┌─── Amazon VPC (10.0.0.0/16) ──────────────────────────────────────────┐
                            │                                                                       │
                            │  ┌─ Public Subnet (10.0.1.0/24) ───┐   ┌─ Private Subnet (10.0.2.0/24) ──┐  │
    Client / Donors ──────► │  │  Internet Gateway & ALB (443)   │──►│  EC2 Instance (t2.micro)        │  │
    (Swagger UI / React)    │  │  - Terminates SSL via ACM       │   │  - Docker Container (Port 8000) │  │
                            │  └─────────────────────────────────┘   │  - Attached IAM Role (No Keys!) │  │
                            │                                        └───────────┬──────────────┬──────┘  │
                            │                                                    │              │         │
                            │  ┌─ Private Data Subnet (10.0.3.0/24) ─────────────▼┐             │         │
                            │  │  Amazon RDS PostgreSQL (Port 5432)               │             │         │
                            │  │  - SG allows ingress ONLY from EC2-SG            │             │         │
                            │  └──────────────────────────────────────────────────┘             │         │
                            │                                                                   │         │
                            │  ┌─ Free VPC Gateway Endpoint ────────────────────────────────────▼──────┐  │
                            │  │  Amazon S3 (Presigned URLs for Family Verification Documents)         │  │
                            │  └───────────────────────────────────────────────────────────────────────┘  │
                            │                                                                             │
                            │  Amazon CloudWatch (Logs, Custom Metrics, and Alarms via SNS)               │
                            └─────────────────────────────────────────────────────────────────────────────┘
```

| AWS Service | How it is used in Ataa Donation Platform | Corresponding Training Module in this Lab |
|---|---|---|
| **IAM & Roles** | Attached to EC2 instance to upload files without static keys | `modules/iam/` (`/api/v1/iam/*`) |
| **EC2 & SGs** | Host Dockerized FastAPI backend behind ALB in private subnet | `modules/ec2_security/` (`/api/v1/ec2/*`) |
| **Secrets Manager / SSM** | Stores DB passwords and payment gateway credentials | `modules/secrets_config/` (`/api/v1/secrets/*`) |
| **Amazon S3** | Stores sensitive family verification and medical documents | `modules/s3_storage/` (`/api/v1/s3/*`) |
| **CloudWatch** | Monitors donation pledge velocity and system error rates | `modules/cloudwatch/` (`/api/v1/cloudwatch/*`) |
| **VPC & Subnets** | Multi-tier network isolation (Public ALB, Private EC2/RDS) | `modules/vpc_networking/` (`/api/v1/vpc/*`) |
| **Docker** | Containerizes FastAPI for reproducible deployments | `modules/docker_lab/` (`/api/v1/docker/*`) |
| **ECS & Fargate** | Target production upgrade from manual EC2 server management | `modules/advanced_compute/` (`/api/v1/advanced/*`) |

---

## 📚 Syllabus & Covered AWS Topics

### 1. 🔐 High Priority: IAM, Roles, Policies & Least Privilege (`/api/v1/iam`)
- **Authentication (AuthN) vs Authorization (AuthZ)**:
  - AuthN (401): Identity verification (*Who are you?* e.g. Access Key / Bearer JWT).
  - AuthZ (403): Permission evaluation (*What are you allowed to do?* e.g. IAM Policies).
- **IAM Users vs IAM Roles**:
  - Why permanent IAM user access keys (`AKIA...`) are dangerous and obsolete for server workloads.
  - Why IAM Roles using temporary STS credentials (`ASIA...`) eliminate key compromise risks.
- **Policies & Permissions Engine**:
  - Simulates the official AWS IAM Evaluation Logic: `Default Deny` $\rightarrow$ `Explicit Allow` $\rightarrow$ `Explicit Deny Overrides Everything`.
- **Principle of Least Privilege**:
  - Detects and warns against dangerous wildcards (`Action: "*"` or `Resource: "*"`).
  - Provides scoped policies limited to specific ARNs (e.g. `arn:aws:s3:::ataa-verification-documents/cases/*`).
- **Static Credential Leak Auditor**:
  - Scans code and configuration files for accidentally committed AWS keys.

### 2. 🖥️ High Priority: EC2 & Security Groups (`/api/v1/ec2`)
- **Stateful Security Groups vs Stateless NACLs**:
  - Security Groups operate at the instance/ENI layer and are **stateful** (inbound traffic automatically allows outbound response traffic).
  - Demonstrates chained security groups: ALB allows `0.0.0.0/0:443`, EC2 allows only `sg-alb:8000`, RDS allows only `sg-ec2:5432`.
- **Instance Metadata Service v2 (IMDSv2)**:
  - Explains the `PUT` session token handshake that protects EC2 from SSRF credential theft.
- **EC2 Instance Types & Pricing**:
  - Burstable general-purpose (t2/t3/t4g), Compute-optimized (c5/c6), and Memory-optimized (r5/r6).
  - On-Demand vs Spot (up to 90% discount) vs Reserved Instances & Savings Plans.

### 3. 🔑 High Priority: Secrets & Environment Variables (`/api/v1/secrets`)
- **SSM Parameter Store**: Hierarchical paths (`/ataa/prod/db/url`), free tier parameters, and KMS `SecureString` decryption.
- **AWS Secrets Manager**: Automated password rotation via Lambda, KMS envelope encryption, and audit logs.
- **Decision Matrix**: Plain `.env` vs Docker environment variables (`--env-file`) vs SSM vs Secrets Manager.

### 4. 🪣 Medium Priority: Amazon S3 Storage (`/api/v1/s3`)
- **Bucket Security Baseline**: S3 Block Public Access, SSE-S3 AES-256 encryption, and Versioning.
- **Presigned URLs (Direct Client Upload)**:
  - Demonstrates generating secure, short-lived `PUT` URLs.
  - Allows browsers to upload medical records directly to S3 without piping large file bytes through FastAPI RAM!
- **Storage Classes & Lifecycle Rules**:
  - Compares Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier Flexible, and Glacier Deep Archive (cost vs retrieval speed).

### 5. 📊 Medium Priority: CloudWatch & Telemetry (`/api/v1/cloudwatch`)
- **CloudWatch Logs**: Structured JSON logging format enabling CloudWatch Logs Insights queries.
- **Custom Metrics**: Emitting multi-dimensional business metrics (`DonationPledgeAmount`, `Category=MedicalAid`).
- **Metric Alarms**: Threshold evaluations (e.g. 5xx Error Rate > 5% or CPU > 80%) and simulated Amazon SNS alert dispatches.

### 6. 🌐 Medium Priority: VPC & Cloud Networking (`/api/v1/vpc`)
- **CIDR & Subnet IP Calculator**:
  - Explains why AWS **always reserves 5 IP addresses** per subnet (`.0` network, `.1` router, `.2` DNS, `.3` future, `.255` broadcast).
  - Shows why a `/24` subnet has 251 usable IPs instead of 256.
- **Packet Journey Simulator**:
  - Traces traffic through Internet Gateway (IGW) and NAT Gateway.
  - Demonstrates **S3 VPC Gateway Endpoints** (100% free internal routing to S3 without touching the internet).

### 7. 🐳 Docker Fundamentals & Containers (`/api/v1/docker`)
- **Images vs Containers**: Read-only immutable blueprints vs running isolated runtime instances.
- **Port Mapping (`-p host:container`)**: Packet forwarding through Docker's network bridge and NAT table.
- **Production Dockerfile**: Multi-stage builds, layer caching optimization, and non-root security (`USER appuser`).
- **Dev vs Prod Consistency**: Eliminating the "it works on my machine" problem.

### 8. 🚀 Low Priority: Advanced Compute & Orchestration (`/api/v1/advanced`)
- **EC2 vs ECS on EC2 vs ECS Fargate vs EKS**: Decision matrix for choosing the right container runtime.
- **Production ECS Task Definition**: Generating task JSON with `networkMode: awsvpc` and native SSM secret injection.
- **Task Role vs Execution Role**: Critical distinction between infrastructure agent permissions and application runtime permissions.
- **Docker to Kubernetes Mapping**: Pods, Deployments, Services, and Ingress.

---

## 🚀 Quickstart: Running Locally

### Option 1: Run with Python & Uvicorn (Fastest)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yzes95/aws-cloud-training-lab.git
   cd aws-cloud-training-lab
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux / macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the API server**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Open Swagger UI**:
   Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) in your browser!

---

### Option 2: Run with Docker & Docker Compose

1. **Build and run the container**:
   ```bash
   docker-compose up -d --build
   ```

2. **Access the application**:
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Health Status: [http://localhost:8000/health](http://localhost:8000/health)

3. **View container logs**:
   ```bash
   docker-compose logs -f
   ```

4. **Stop the container**:
   ```bash
   docker-compose down
   ```

---

## 🧪 Running the Test Suite

All 24 unit tests validate business logic, security policies, and AWS service handlers:

```bash
pytest tests/ -v
```

Expected output:
```
tests/test_units.py::test_health PASSED
tests/test_units.py::test_iam_auth_vs_authz PASSED
tests/test_units.py::test_iam_evaluate_policy_allow PASSED
tests/test_units.py::test_iam_evaluate_policy_deny PASSED
tests/test_units.py::test_iam_assume_role PASSED
tests/test_units.py::test_iam_credential_auditor PASSED
tests/test_units.py::test_ec2_security_groups PASSED
tests/test_units.py::test_ec2_imds_v2 PASSED
tests/test_units.py::test_ec2_pricing_guide PASSED
tests/test_units.py::test_secrets_ssm PASSED
tests/test_units.py::test_secrets_manager PASSED
tests/test_units.py::test_secrets_comparison PASSED
tests/test_units.py::test_s3_bucket_and_upload PASSED
tests/test_units.py::test_s3_presigned_url PASSED
tests/test_units.py::test_s3_storage_classes PASSED
tests/test_units.py::test_cloudwatch_logging_and_metrics PASSED
tests/test_units.py::test_cloudwatch_alarm PASSED
tests/test_units.py::test_vpc_subnet_reserved_ips PASSED
tests/test_units.py::test_vpc_routing PASSED
tests/test_units.py::test_vpc_endpoints_guide PASSED
tests/test_units.py::test_docker_refresher PASSED
tests/test_units.py::test_docker_port_mapping PASSED
tests/test_units.py::test_dockerfile_guide PASSED
tests/test_units.py::test_advanced_compute PASSED

============================= 24 passed in 0.96s ==============================
```

---

## ⚙️ Configuration & Dual-Mode Toggle

Configure your environment in `.env`:

```env
APP_NAME="AWS Cloud Training Lab"
APP_ENV="development"
DEBUG=true

# Set to True to train offline for FREE with simulated AWS responses
# Set to False to call live AWS APIs or LocalStack
AWS_MOCK_MODE=true
AWS_REGION="us-east-1"

# Real AWS Credentials (ONLY needed if AWS_MOCK_MODE=false)
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_SESSION_TOKEN=""

# LocalStack endpoint (optional for local boto3 emulation)
LOCALSTACK_ENDPOINT_URL=""
```

---

## 📄 License

This training lab is open-source and licensed under the [MIT License](LICENSE).
