FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir cneura-ai==0.1.112


COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8800"]

