from airflow.models.baseoperator import BaseOperator
import requests
import json

# Execute livy statement if not exists. It saves statement_id into xcom.
class ExecuteLivyStatement(BaseOperator):
    def __init__(self, livy_url, session_task_id, hdfs_task_id, algorithm_name, **kwargs):
        self.livy_url = livy_url
        self.session_task_id = session_task_id
        self.hdfs_task_id = hdfs_task_id
        self.algorithm_name = algorithm_name
        super().__init__(**kwargs)

    def execute(self, context):
        livy_session = context.get('ti').xcom_pull(task_ids=self.session_task_id)
        session_id = livy_session['session_id']
        hdfs_file_path_array = context.get('ti').xcom_pull(task_ids=self.hdfs_task_id)
        for hdfs_file_path in hdfs_file_path_array:
            url = '{}/sessions/{}/statements'.format(self.livy_url, session_id)
            jsonbody = {'code': 'import {}\n{}.run("{}?op=OPEN")'.format(self.algorithm_name, self.algorithm_name, hdfs_file_path)}
            print('Sending statement to Livy:')
            print(url)
            print(jsonbody)
            response = requests.post(url, json=jsonbody)
            print('status_code: {}'.format(response.status_code))
            if response.status_code == 201:
                jsonbody = response.json()
                print(jsonbody)
                obj = {'statement_id': jsonbody['id']}
                context['ti'].xcom_push('return_value', json.dumps(obj))
                return obj
            elif response.status_code == 400:
                jsonbody = response.json()
                print(json)
                raise Exception("Something went wrong: {}".format(jsonbody['msg']))
            else:
                raise Exception("Something went wrong: {}".format(response))
