FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip 

RUN pip install --no-cache-dir aiofiles==24.1.0 aiosqlite==0.21.0 python-dotenv==1.1.0 typing_extensions==4.13.1 websockets==15.0.1 loguru 

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "main.py"]
