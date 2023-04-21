from airflow.models.baseoperator import BaseOperator
import requests
import json
import time

# Wait for livy session to be in state "idle". Retrieve session id to poke from parent_task_id xcom return_value.
# It saves session_id and session_name into xcom.
class WaitForIdleLivySession(BaseOperator):
    def __init__(self, livy_url, parent_task_id, **kwargs):
        self.parent_task_id = parent_task_id
        self.livy_url = livy_url
        super().__init__(**kwargs)

    def execute(self, context):
        livy_session = context.get('ti').xcom_pull(task_ids=self.parent_task_id)
        session_id = livy_session['session_id']
        response = self.get_session(session_id)
        if response.status_code == 200:
            json_response = response.json()
            print(json_response)
            counter = 0
            while json_response['state'] != 'idle':
                if counter > 120:
                    raise Exception("Timeout expired waiting for idle session with id {}".format(session_id))
                time.sleep(1)
                response = self.get_session(session_id)
                json_response = response.json()
                counter += 1
            obj = {'session_id': json_response['id'], 'session_name': json_response['name']}
            context['ti'].xcom_push('return_value', json.dumps(obj))
            return obj
        elif response.status_code == 404:
            json_response = response.json()
            print(json_response)
            raise Exception("Session not found with id {}".format(session_id))
        else:
            raise Exception("Something went wrong: {}".format(response))

    def get_session(self, session_id):
        url = '{}/sessions/{}'.format(self.livy_url, session_id)
        print('Sending request to Livy: ')
        print(url)
        response = requests.get(url)
        print('status_code: {}'.format(response.status_code))
        return response
