FROM python:3.9-slim

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    wget \
    gnupg2 \
    && apt-get clean

# Agregar repositorio oficial de AdoptOpenJDK (Java 11)
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor -o /etc/apt/keyrings/adoptium.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/adoptium.gpg] https://packages.adoptium.net/artifactory/deb bookworm main" > /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && \
    apt-get install -y temurin-11-jre

# Configurar JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/temurin-11-jre-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV PYFLINK_PYTHON=python

# Crear carpeta de trabajo
WORKDIR /app

# Copiar código
COPY . .

# Instalar PyFlink
RUN pip install apache-flink==1.17.1

# Comando por defecto
CMD ["python", "flink_kafka_testing.py"]
