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
table_env.execute_sql(source)
table=table_env.from_path('ecommerce')
print ('\nSource Schema')
table.print_schema()
table_env.execute_sql("SELECT * FROM ecommerce").print()

# #Calculation
# sql="""
#     select 
# """
