"""Minimal 2-Endpoint FastAPI App for AWS Training.

Endpoints:
1. GET  /health -> Used by ALB Health Checks; verifies API, RDS Database, and AWS IAM Role identity.
2. POST /items  -> Saves an item to PostgreSQL (RDS), uploads a file to S3, and logs a metric to CloudWatch.
3. GET  /items  -> Lists saved items from PostgreSQL (RDS).
"""
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, File, Form, Request, UploadFile, status
from fastapi.responses import JSONResponse

# Structured logger (Docker / EC2 CloudWatch agent picks up stdout logs automatically)
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger("aws_training_app")

app = FastAPI(
    title="AWS Training App (2-Endpoint Lab)",
    description="Minimal FastAPI backend to practice connecting Python + Docker to RDS, S3, Secrets Manager, IAM Roles, and CloudWatch.",
    version="1.0.0",
)


@app.exception_handler(NotImplementedError)
def not_implemented_handler(request: Request, exc: NotImplementedError):
    return JSONResponse(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        content={"status": "TODO", "detail": str(exc)},
    )


# =====================================================================
# ENDPOINT 1: Health & Connectivity Check (ALB / RDS / IAM Role)
# =====================================================================
@app.get("/health", tags=["1. Health & IAM Check"])
def health_check() -> Dict[str, Any]:
    """Health check endpoint probed by the AWS Application Load Balancer (ALB).
    
    Once you implement `db.check_db_connection()` and `aws_services.get_aws_identity()`,
    uncomment them below to verify your RDS connection and EC2 IAM Role in Swagger UI.
    """
    # TODO: Uncomment as you implement db.py and aws_services.py:
    # from db import check_db_connection
    # from aws_services import get_aws_identity
    # db_ok = check_db_connection()
    # aws_identity = get_aws_identity()

    return {
        "status": "healthy",
        "database": "TODO: call check_db_connection() in db.py",
        "aws_iam_identity": "TODO: call get_aws_identity() in aws_services.py",
    }


# =====================================================================
# ENDPOINT 2: Items CRUD + S3 Upload + CloudWatch Telemetry
# =====================================================================
@app.post("/items", tags=["2. Items (RDS + S3 + CloudWatch)"])
def create_item(
    name: str = Form(..., description="Item name to save in RDS PostgreSQL"),
    description: Optional[str] = Form(None, description="Optional item description"),
    file: Optional[UploadFile] = File(None, description="Optional file to upload to Amazon S3"),
) -> Dict[str, Any]:
    """Single end-to-end cloud workflow:
    1. If a file is attached, upload it to Amazon S3 (`aws_services.upload_to_s3`).
    2. Save the item record (`name`, `description`, `s3_file_url`) in PostgreSQL / AWS RDS (`db.py`).
    3. Emit a structured log and increment the `ItemsCreated` metric in CloudWatch (`aws_services.record_cloudwatch_metric`).
    """
    logger.info(f"Received request to create item: {name}")

    # TODO 1: If `file` is provided, read `file.file.read()` and upload to S3 via `upload_to_s3()`
    # TODO 2: Insert the new Item into PostgreSQL / RDS using your SQLAlchemy session from `db.py`
    # TODO 3: Call `record_cloudwatch_metric("ItemsCreated", 1.0)`
    # TODO 4: Return the created item with its database ID and S3 URL
    raise NotImplementedError(
        "TODO: Connect create_item() to S3 (aws_services.py), PostgreSQL/RDS (db.py), and CloudWatch."
    )


@app.get("/items", tags=["2. Items (RDS + S3 + CloudWatch)"])
def list_items() -> List[Dict[str, Any]]:
    """Fetches all saved items from PostgreSQL / AWS RDS."""
    # TODO: Query all items from the `Item` table in `db.py` and return them
    raise NotImplementedError("TODO: Query and return items from PostgreSQL / RDS in db.py.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
