FROM python:3.12-slim

WORKDIR /ecommerce_simulator

COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libc-dev librdkafka-dev && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run_simulator.py"]