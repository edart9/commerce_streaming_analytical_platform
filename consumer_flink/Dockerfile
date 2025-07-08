FROM flink:1.20.1-java11

WORKDIR /consumer_flink

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv build-essential gcc g++ libatlas-base-dev && apt-get clean
RUN ln -s /usr/bin/python3 /usr/bin/python
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
