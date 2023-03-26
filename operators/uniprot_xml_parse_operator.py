from airflow.models import BaseOperator
from uniprot_xml_parser import parse_uniprot_xml_file


class UniProtXmlParseOperator(BaseOperator):
    def __init__(self, input_file, output_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_file = input_file
        self.output_data = output_data

    def execute(self, context):
        entries = parse_uniprot_xml_file(self.input_file)
        context['task_instance'].xcom_push(key=self.output_data, value=entries)
