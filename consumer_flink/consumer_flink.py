from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment,EnvironmentSettings
import os
 
#/opt/flink/bin/flink run --jobmanager flinkjobmanager:8081 --python /consumer_flink/consumer_flink.py

env=StreamExecutionEnvironment.get_execution_environment()
settings=EnvironmentSettings.new_instance()\
                .in_streaming_mode()\
                .build()


table_env=StreamTableEnvironment.create(stream_execution_environment=env,
                                        environment_settings=settings)
lib_path = os.path.join(os.path.dirname(__file__), "lib")
jars = [f"file://{os.path.join(lib_path, jar)}" for jar in os.listdir(lib_path) if jar.endswith(".jar")]
table_env.get_config().get_configuration().set_string("pipeline.jars", ";".join(jars))
print(table_env)



table_env.execute_sql("""
        CREATE TABLE ecommerce(
            event_time TIMESTAMP(3),
            event_type varchar,
            product_id bigint,
            category_id bigint,
            category_code varchar,
            brand varchar,
            price double,
            user_id bigint,
            user_session varchar,
            ip varchar,
            proctime as PROCTIME()
        ) with (
            'connector'='kafka',
            'topic'='ecommerce_online_events',
            'properties.bootstrap.servers'='kafka:9092',
            'properties.group.id'='ecommerce',
            'scan.startup.mode' = 'earliest-offset',
            'format'='json'
        )
""")
table_env.execute_sql("""
CREATE TABLE postgres_sink (
    event_time TIMESTAMP(3),
    event_type STRING,
    product_id BIGINT,
    category_id BIGINT,
    category_code STRING,
    brand STRING,
    price DOUBLE,
    user_id BIGINT,
    user_session STRING,
    ip STRING,
    proctime TIMESTAMP(3)
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/ecommercedb',
    'table-name' = 'replica.t_ecommerce_events',
    'driver' = 'org.postgresql.Driver',
    'username' = 'aratae',
    'password' = 'Dexter121118,'
)
""")


table_env.execute_sql("""
INSERT INTO postgres_sink
SELECT * FROM ecommerce
""")