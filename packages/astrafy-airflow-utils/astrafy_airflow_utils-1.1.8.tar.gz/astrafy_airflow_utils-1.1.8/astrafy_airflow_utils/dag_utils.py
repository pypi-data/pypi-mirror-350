from datetime import datetime, timedelta
from airflow.models.param import Param

def default_dag(data_product, ENV, schedule= '0 10 * * *',start_date=datetime(2022, 10, 10, 1, 0),**kwargs):
    dag = {
        "dag_id": f'{data_product}-k8s-dag-{ENV}',
        "schedule_interval": schedule,
        "description": f'Dag for the {data_product} data product - {ENV}',
        "max_active_tasks": 10,
        "catchup": False,
        "is_paused_upon_creation": True,
        "tags": ['k8s', data_product],
        "max_active_runs": 1,
        "dagrun_timeout": timedelta(seconds=36000),
        "default_view": 'grid',
        "orientation": 'LR',
        "sla_miss_callback": None,
        "params": {"is_full_refresh": Param(False, type="boolean")},
        "start_date": start_date,
        "doc_md": __doc__,
    }
    
    dag.update(kwargs)
    
    return dag