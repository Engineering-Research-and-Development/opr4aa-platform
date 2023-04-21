from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.models.xcom_arg import XComArg

def source(**kwargs):
    #kwargs['ti'].xcom_push(key='return_value', value=[1,2,3])
    return [{"x":1},{"x":2},{"x":3}]

def add_one(x):
    print(x)
    return x + 1

def sum_it(values):
    print(values)
    total = sum(values)
    print(f"Total was {total}")


with DAG(dag_id="example_dynamic_task_mapping_reduce", start_date=datetime(2022, 3, 4), schedule_interval=None):
    source = PythonOperator(
        task_id="source",
        python_callable=source,
        provide_context=True
    )
    add_one_task = PythonOperator.partial(
        task_id="add_one",
        python_callable=add_one
    ).expand(
        op_kwargs=XComArg(source, key='return_value')
    )
    sum_it_task = PythonOperator(
        task_id="sum_it",
        python_callable=sum_it,
        op_kwargs={"values": add_one_task.output},
    )