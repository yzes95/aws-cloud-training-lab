# ==========================================
# TODO: Write your Dockerfile here
# ==========================================
# Hints for multi-stage build:
# 1. Stage 1 (Builder):
#    - FROM python:3.13-slim AS builder
#    - WORKDIR /app
#    - COPY requirements.txt .
#    - RUN pip install --no-cache-dir --user -r requirements.txt
#
# 2. Stage 2 (Runner):
#    - FROM python:3.13-slim AS runner
#    - Create a non-root user (e.g., useradd -u 1001 appuser)
#    - COPY --from=builder /root/.local /home/appuser/.local
#    - COPY . .
#    - USER appuser
#    - EXPOSE 8000
#    - CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
