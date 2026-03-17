FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY filesystem-mcp/main.py .

ENV PYTHONBUFFERED=1

CMD ["python", "main.py"]