FROM --platform=linux/amd64 python:3.9.6-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install -r requirements.txt

COPY app/*.py .

ENTRYPOINT ["python", "app.py"]