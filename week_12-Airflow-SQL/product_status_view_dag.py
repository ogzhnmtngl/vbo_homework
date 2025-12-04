from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import logging

POSTGRES_CONN_ID = "postgresql_conn"

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 5, 20),
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}

with DAG(
    dag_id="v_product_status_track_view_dag",
    default_args=default_args,
    schedule_interval="@hourly",   # Ödev gereği saatlik
    catchup=False,
    description="Create/refresh serving.v_product_status_track and log sample rows",
) as dag:

 
    create_serving_schema = SQLExecuteQueryOperator(
        task_id="create_serving_schema",
        conn_id=POSTGRES_CONN_ID,
        sql="""
        CREATE SCHEMA IF NOT EXISTS serving;
        """,
    )


    create_product_status_view = SQLExecuteQueryOperator(
        task_id="create_v_product_status_track",
        conn_id=POSTGRES_CONN_ID,
        sql="""
        CREATE OR REPLACE VIEW serving.v_product_status_track AS
        SELECT
            o.order_id,
            o.order_date,
            o.order_status,
            oi.order_item_id,
            oi.order_item_order_id,
            oi.order_item_product_id AS product_id,
            p.product_name,
            oi.order_item_quantity,
            oi.order_item_subtotal,
            oi.order_item_product_price,

            -- Ürün bazında teslim edildi mi?
            CASE 
                WHEN o.order_status IN ('COMPLETE', 'CLOSED') THEN TRUE
                ELSE FALSE
            END AS is_delivered,

            -- Ödeme tamam mı? (pending / canceled / fraud dışı durumları "paid" sayıyoruz)
            CASE 
                WHEN o.order_status NOT IN ('PENDING_PAYMENT', 'CANCELED', 'SUSPECTED_FRAUD') THEN TRUE
                ELSE FALSE
            END AS is_paid,

            -- Sipariş iptal mi?
            CASE 
                WHEN o.order_status = 'CANCELED' THEN TRUE
                ELSE FALSE
            END AS is_cancelled
        FROM staging.orders o
        JOIN staging.order_items oi
          ON o.order_id = oi.order_item_order_id
        JOIN staging.products p
          ON oi.order_item_product_id = p.product_id;
        """,
    )

   
    def log_view_sample_rows():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        records = hook.get_records("""
            SELECT *
            FROM serving.v_product_status_track
            ORDER BY order_id, product_id
            LIMIT 20;
        """)

        logging.info("Query output from serving.v_product_status_track (first 20 rows):")
        for row in records:
 
            logging.info(row)

    preview_view = PythonOperator(
        task_id="preview_v_product_status_track",
        python_callable=log_view_sample_rows,
    )

    create_serving_schema >> create_product_status_view >> preview_view
