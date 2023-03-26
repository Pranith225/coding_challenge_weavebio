from airflow.models import BaseOperator
from neo4j_loader import Neo4jLoader


class Neo4jLoadOperator(BaseOperator):
    def __init__(self, input_data, uri, user, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_data = input_data
        self.uri = uri
        self.user = user
        self.password = password

    def execute(self, context):
        entries = context['task_instance'].xcom_pull(key=self.input_data)
        loader = Neo4jLoader(self.uri, self.user, self.password)

        for entry in entries:
            loader.load_data(entry)

        loader.close()
