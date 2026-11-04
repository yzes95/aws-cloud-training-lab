# AWS Training Lab (2-Endpoint Backend)

I built this small backend project to train myself on connecting a Python/FastAPI application to PostgreSQL (AWS RDS) and AWS services, and practicing cloud infrastructure, Docker, and CI/CD around it.

Instead of building a large app or a frontend, I kept the codebase down to **2 endpoints** (`GET /health` and `POST/GET /items`) tested through FastAPI's Swagger UI (`/docs`). All the AWS and Docker connections are marked with `# TODO` so I can implement and test each piece myself.

## Project Layout

```text
aws-cloud-training-lab/
├── .github/workflows/
│   └── ci.yml           # TODO: GitHub Actions (pytest -> AWS OIDC STS -> ECR push)
├── main.py              # FastAPI app with /health and /items
├── db.py                # TODO: SQLAlchemy connection & Item model for PostgreSQL / AWS RDS
├── aws_services.py      # TODO: Boto3 integrations (STS identity, Secrets/SSM, S3, CloudWatch)
├── test_main.py         # Pytest suite (starts with /health test gate)
├── Dockerfile           # TODO: Multi-stage container build
├── docker-compose.yml   # TODO: Local FastAPI + local PostgreSQL container
├── LEARNING_PATH.md     # My step-by-step checklist for code & AWS console/CLI setup
└── requirements.txt
```

## How the 2 Endpoints Cover My AWS Topics

1. **`GET /health`**
   - Checks that the API is alive, tests the PostgreSQL/RDS connection (`SELECT 1`), and calls AWS STS `get_caller_identity()`.
   - **AWS topics applied:** Application Load Balancer (ALB) health checks, Fault Tolerance, IAM Roles & temporary STS credentials (no hardcoded AWS keys).

2. **`POST /items` & `GET /items`**
   - Saves an item (`name`, `description`) to **PostgreSQL / AWS RDS**, uploads an optional file to **Amazon S3** (with presigned URLs), fetches DB credentials from **Secrets Manager / SSM Parameter Store**, and sends structured logs + custom metrics to **Amazon CloudWatch**.
   - **AWS topics applied:** S3 object storage, RDS Multi-AZ, Secrets Manager/SSM, CloudWatch Logs & Metrics, VPC private subnets, chained Security Groups (`ALB -> EC2 -> RDS`), and Auto Scaling Groups (HA & Elasticity).

## How I Run It Locally

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

3. Open Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs).

4. Run tests:
   ```bash
   pytest test_main.py -v
   ```

## License
MIT
