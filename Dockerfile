FROM --platform=linux/amd64 python:3.9.6-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install -r requirements.txt \
    && addgroup --gid 3000 --system nonroot \
    && adduser --uid 2000 --system --ingroup nonroot wiliotuser

USER 2000:3000
COPY app/*.py .

ENTRYPOINT ["python", "app.py"]
