from airflow.models.baseoperator import BaseOperator
import os
import json

class RemoveFilesOperator(BaseOperator):
    def __init__(self, parent_task_id, **kwargs):
        self.parent_task_id = parent_task_id
        super().__init__(**kwargs)

    def execute(self, context):
        ti = context.get('ti')
        print('Remove Files Operator starting...')
        files = json.loads(ti.xcom_pull(task_ids=self.parent_task_id))
        for file in files:
            os.remove(file)
