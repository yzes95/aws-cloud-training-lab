from pydantic import BaseModel, Field


class ECSTaskDefRequest(BaseModel):
    family_name: str = Field(default="my-backend-task")
    container_name: str = Field(default="fastapi-app")
    image_uri: str = Field(default="123456789012.dkr.ecr.us-east-1.amazonaws.com/my-backend:latest")
    cpu: str = Field(default="256")
    memory: str = Field(default="512")
    container_port: int = Field(default=8000)
