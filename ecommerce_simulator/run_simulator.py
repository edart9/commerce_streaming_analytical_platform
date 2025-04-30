import os
import time
import random
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from loguru import logger

# Cargar variables de entorno
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path)

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_GROUP = os.getenv("KAFKA_GROUP")
KAFKA_OFFSET = os.getenv("KAFKA_OFFSET")

logger.info(f"KAFKA_BOOTSTRAP: {KAFKA_BOOTSTRAP}")
logger.info(f"KAFKA_GROUP: {KAFKA_GROUP}")
logger.info(f"KAFKA_OFFSET: {KAFKA_OFFSET}")
logger.info(f"KAFKA_TOPIC: {KAFKA_TOPIC}")

kafka_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP
}

# ✅ Crear el topic si no existe
def ensure_topic_exists():
    topic_name = KAFKA_TOPIC
    admin_client = AdminClient(kafka_config)
    for i in range (5):
        try:
            metadata = admin_client.list_topics(timeout=5)
            if topic_name not in metadata.topics:
                logger.info(f"Creando topic: {topic_name}")
                topic = NewTopic(topic=topic_name, num_partitions=1, replication_factor=1)
                admin_client.create_topics([topic])
                logger.info(f'topic creado {topic}')
                return
        except Exception as e:
            logger.error(f"Error creando topic: {e}")
            time.sleep(5)
    raise RuntimeError("❌ No se pudo conectar con Kafka luego de varios intentos.")

# ✅ Callback para logs de envío
def log_callback(err, msg):
    if err:
        logger.error(f"❌ Error al enviar evento: {err}")
    else:
        logger.success(f"✅ Evento enviado: {msg.value()}")

# ✅ Enviar eventos
def run_simulator():
    producer = Producer(kafka_config)
    path_csv = os.path.join(os.path.dirname(__file__), "data", "events.csv")

    if not os.path.exists(path_csv):
        logger.error(f"Archivo CSV no encontrado: {path_csv}")
        return

    try:
        df = pd.read_csv(path_csv, encoding="utf-8")  # Ajustá encoding si da error
        logger.info(f"📄 Cargando {len(df)} eventos desde CSV.")
    except Exception as e:
        logger.error(f"Error leyendo el CSV: {e}")
        return

    try:
        while True:
            i = random.randint(0, len(df) - 1)
            evento = df.iloc[i]
            evento["event_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            day_key = datetime.now().strftime("%Y-%m-%d")
            producer.produce(
                topic=KAFKA_TOPIC,
                value=evento.to_json(),
                key=day_key,
                callback=log_callback
            )
            time.sleep(2)
            producer.poll(0)
    except KeyboardInterrupt:
        logger.warning("Simulación detenida por teclado.")
    finally:
        producer.flush()
        logger.info("Mensajes pendientes enviados.")

if __name__ == "__main__":
    ensure_topic_exists()
    run_simulator()
