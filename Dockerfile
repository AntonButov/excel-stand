FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-calc \
    poppler-utils \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY excel_stand ./excel_stand
RUN pip install --no-cache-dir .

EXPOSE 8080
CMD ["uvicorn", "excel_stand.api:app", "--host", "0.0.0.0", "--port", "8080"]
