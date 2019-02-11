from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator 
from airflow.contrib.sensors.mongo_sensor import MongoSensor
# from airflow.operators.email_operator import EmailOperator

default_args={
	'owner': 'rreamy',
}

def print_promotions(promotions):
    return 'promotions'

myDag = DAG('simple_workflow', description='Simple tutorial DAG', schedule_interval='0 12 * * *', start_date=datetime(2017, 3, 20), catchup=False)

task1 = MongoSensor(collection="packages", query={"promote": "true"}, mongo_conn_id="dataLake", task_id="task1", poke_interval=30, dag=myDag)

task2 = BashOperator(task_id='say_hi', bash_command='echo I am processing data now', dag=myDag)

# Commented this out because I need to do additional work to set up mailing...but this is an option
# task3 = EmailOperator(task_id="email_user", to="rlreamy@umich.edu", subject="You've got work", html_content="Check it...you got work to do")

task3 = MongoSensor(collection="packages", query={"qa": "pass"}, mongo_conn_id="dataLake", task_id="QApassed", poke_interval=30, dag=myDag)


# I couldn't find a prebuilt operator for moving files, but you could envision this being done by using PythonOperator and creating a python script to move data around

task1 >> task2 >> task3

# additional operators that I think would be intersting/useful:
# ExternalTaskSensor - used to wait for a task to complete in a different DAG
# SlackAPIPostOperator - can be used to post information to slack, useful if a process fails
# SimpleHttpOperator - calls an endpoint to execute an action
# PythonOperator - used to call a python script
