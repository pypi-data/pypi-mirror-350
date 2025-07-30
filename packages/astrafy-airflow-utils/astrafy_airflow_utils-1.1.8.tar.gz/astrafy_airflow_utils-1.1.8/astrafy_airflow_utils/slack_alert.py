from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.configuration import conf


SLACK_CONN_ID = "slack_airflow"

DAG_OWNER_MAPPING = {
    "management": "U02TS6TVBP1", #Charles
    "finops": "U06CCADAA21", #Victor
    "billing": "U06CCADAA21", #Victor
    "monitoring": "U08B0Q00T9U", #Cris
    "security": "U02TS6TVBP1", #Charles
    "chatops": "U04PS4C43EC", #Nawfel
    "gitops": "U085HU06BQ9", #Virginia
    "sales_marketing": "U02UKEM1XFB", #Andrea
    "web_analytics": "U06U5P7SV7G", #Greta
    "internal_doc": "U04JMG5CU0K" #Alex
}

def task_fail_slack_alert(context):
    webserver_url = conf.get('webserver', 'base_url')
    dag_id = context.get("task_instance").dag_id
    task_id = context.get("task_instance").task_id
    run_id = context.get("task_instance").run_id
    execution_date = context.get("execution_date")
    dag_url = f"{webserver_url}/dags/{dag_id}/grid?execution_date={execution_date.isoformat()}&tab=graph&dag_run_id={run_id}"

    owner_tag = ""
    for prefix, user_id in DAG_OWNER_MAPPING.items():
        if dag_id.startswith(prefix):
            owner_tag = f"<@{user_id}>"
            break

    slack_msg = """
:red_circle: Task Failed.
*Task*: {task}  
*Dag*: {dag} 
*Execution Time*: {exec_date}
*Dag URL*: <{url}|View in Airflow>
*Owner*: {owner}
""".format(
        task=task_id,
        dag=dag_id,
        exec_date=execution_date,
        url=dag_url,
        owner=owner_tag
    )
    failed_alert = SlackWebhookOperator(
        task_id="slack_fail_alert", 
        slack_webhook_conn_id=SLACK_CONN_ID,
        message=slack_msg,
    )
    return failed_alert.execute(context=context)
