from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment,EnvironmentSettings
import os

#create streaming enviroment
env=StreamExecutionEnvironment.get_execution_environment()
settings=EnvironmentSettings.new_instance()\
                .in_streaming_mode()\
                .build()

#create table enviroment
table_env=StreamTableEnvironment.create(stream_execution_environment=env,
                                        environment_settings=settings)
lib_path = os.path.join(os.path.dirname(__file__), "lib")
jars = [f"file://{os.path.join(lib_path, jar)}" for jar in os.listdir(lib_path) if jar.endswith(".jar")]
table_env.get_config().get_configuration().set_string("pipeline.jars", ";".join(jars))
print(table_env)


#Creating kafka source table
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
# Execute and confirm
try:
    table_env.execute_sql(source)
    print("✅ Source table created")
except Exception as e:
    print("❌ Table creation failed:", e)

# Skip from_path() unless you need Table API access
query = """
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY window_start ORDER BY total_revenue DESC) AS rownum
    FROM (
        SELECT
            TUMBLE_START(proctime, INTERVAL '1' MINUTE) AS window_start,
            brand,
            product_id,
            SUM(price) AS total_revenue
        FROM ecommerce
        WHERE event_type = 'purchase'
        GROUP BY TUMBLE(proctime, INTERVAL '1' MINUTE), brand, product_id
    )
)
WHERE rownum <= 5
"""

# Execute SQL query
print("✅ Executing query:")
table_env.execute_sql(query).print()