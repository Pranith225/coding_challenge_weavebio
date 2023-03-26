from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from operators.uniprot_xml_parse_operator import UniProtXmlParseOperator
from operators.neo4j_load_operator import Neo4jLoadOperator

dag = DAG(
    'uniprot_neo4j_dag',
    default_args={
        'owner': 'airflow',
        'retries': 0,
        'retry_delay': timedelta(minutes=5),
        'start_date': datetime(2022, 1, 1),
    },
    description='Load UniProt data into Neo4j graph database',
    schedule_interval=timedelta(days=1),
    catchup=False,
    max_active_runs=1,
)

start = DummyOperator(task_id='start', dag=dag)

parse_uniprot_xml = UniProtXmlParseOperator(
    task_id='parse_uniprot_xml',
    input_file='data/Q9Y261.xml',
    output_data='uniprot_entries',
    dag=dag,
)

load_data_to_neo4j = Neo4jLoadOperator(
    task_id='load_data_to_neo4j',
    input_data='uniprot_entries',
    uri='bolt://localhost:7687',
    user='neo4j',
    password='neo4j_password',
    dag=dag,
)

end = DummyOperator(task_id='end', dag=dag)

start >> parse_uniprot_xml >> load_data_to_neo4j >> end
