from airflow.hooks.filesystem import FSHook
from airflow.models.baseoperator import BaseOperator
import os
import json
import time

class XcomPythonFileSensor(BaseOperator):
    def __init__(self, filepath, fs_conn_id="fs_default", fetch_one=False, **kwargs):
        self.fetch_one = fetch_one
        self.filepath = filepath
        self.fs_conn_id = fs_conn_id
        super().__init__(**kwargs)

    def execute(self, context):
        hook = FSHook(self.fs_conn_id)
        basepath = hook.get_path()
        full_path = os.path.join(basepath, self.filepath)
        print("Poking for file {}".format(full_path))

        counter = 0
        while len(os.listdir(full_path)) == 0:
            if counter > 600:
                raise Exception("Timeout expired.")
            time.sleep(1)

        print("Files found at {}".format(full_path))

        for _, _, files in os.walk(full_path):
            if len(files) > 0:
                complete_files = []
                for file in files:
                    print("{}/{}".format(full_path, file))
                    complete_files.append("{}/{}".format(full_path, file))
                    if self.fetch_one:
                        context['ti'].xcom_push('return_value', json.dumps(complete_files))
                        return json.dumps(complete_files)
                context['ti'].xcom_push('return_value', json.dumps(complete_files))
                return json.dumps(complete_files)
        return []
