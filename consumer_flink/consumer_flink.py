from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment,EnvironmentSettings
import os


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



source="""
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
"""

try:
    table_env.execute_sql(source)
    print("✅ Source table created")
except Exception as e:
    print("❌ Table creation failed:", e)


query = """
SELECT *
FROM ecommerce
"""


print("✅ Executing query:")
table_env.execute_sql(query).print()