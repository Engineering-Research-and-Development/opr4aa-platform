from airflow.models.baseoperator import BaseOperator
import os
import glob

class EmptyDirectoryOperator(BaseOperator):
    def __init__(self, path, **kwargs):
        self.path = path
        super().__init__(**kwargs)

    def execute(self, context):
        print('Remove Files Operator starting...')
        files = glob.glob('{}/*'.format(self.path))
        for file in files:
            os.remove(file)
