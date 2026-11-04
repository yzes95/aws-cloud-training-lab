"""Database connection and models (PostgreSQL / AWS RDS).

How this connects to AWS:
1. Locally: Connects to a local Postgres container via DATABASE_URL environment variable.
2. On AWS: Connects to an Amazon RDS (PostgreSQL) instance in a private subnet.
3. Secrets: Instead of hardcoding the RDS password in .env, you can fetch it at startup
   from AWS Secrets Manager or SSM Parameter Store using `get_secret()` in `aws_services.py`.
"""
import os
from typing import Any, Generator

# Default local database URL (override in .env or fetch from AWS Secrets Manager)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/training_db"
)

# TODO 1: Create the SQLAlchemy engine and SessionLocal
# Example:
# from sqlalchemy import create_engine, Column, Integer, String, text
# from sqlalchemy.orm import declarative_base, sessionmaker
#
# engine = create_engine(DATABASE_URL, pool_pre_ping=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# TODO 2: Define a simple `Item` table model
# Columns needed:
# - id (Integer, primary_key=True)
# - name (String, nullable=False)
# - description (String)
# - s3_file_url (String, nullable=True)  <-- stores the S3 key or URL of the uploaded file


def get_db() -> Generator[Any, None, None]:
    """FastAPI dependency that provides a database session per request."""
    # TODO 3: Yield a database session and close it in a `finally:` block
    raise NotImplementedError("TODO: Implement get_db() session dependency in db.py")


def check_db_connection() -> bool:
    """Used by GET /health to verify that PostgreSQL / RDS is reachable."""
    # TODO 4: Run a simple `SELECT 1` query against the database and return True/False
    # Hint: During an RDS Multi-AZ failover, existing connections drop; `pool_pre_ping=True`
    # on your SQLAlchemy engine helps automatically reconnect!
    raise NotImplementedError("TODO: Implement check_db_connection() in db.py")
