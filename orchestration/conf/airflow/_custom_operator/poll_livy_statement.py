from airflow.models.baseoperator import BaseOperator
import requests
import json
import time 

# Poll livy statement until completed. It saves alrgorithm result into xcom.
class PollLivyStatement(BaseOperator):
    def __init__(self, livy_url, session_task_id, statement_task_id, **kwargs):
        self.livy_url = livy_url
        self.session_task_id = session_task_id
        self.statement_task_id = statement_task_id
        super().__init__(**kwargs)

    def execute(self, context):
        livy_session = context.get('ti').xcom_pull(task_ids=self.session_task_id)
        session_id = livy_session['session_id']
        livy_statement = context.get('ti').xcom_pull(task_ids=self.statement_task_id)
        statement_id = livy_statement['statement_id']

        response = self.get_statement_state(session_id, statement_id)
        if response.status_code == 200:            
            json_response = response.json()            
            print(json_response)            
            counter = 0            
            while json_response['state'] != 'available':
                if counter > 600:
                    raise Exception("Timeout expired waiting for idle statement with id {}".format(statement_id))
                time.sleep(1)                
                response = self.get_statement_state(session_id, statement_id)
                json_response = response.json()                
                counter += 1
            print(json_response)
            obj = json_response['output']['data']['text/plain']
            context['ti'].xcom_push('return_value', obj)
            return obj        
        elif response.status_code == 404:            
            json_response = response.json()            
            print(json_response)            
            raise Exception("Statement not found with id {}".format(statement_id))
        else:            
            raise Exception("Something went wrong: {}".format(response))

    def get_statement_state(self, session_id, statement_id):
        url = '{}/sessions/{}/statements/{}'.format(self.livy_url, session_id, statement_id)
        print('Sending request to Livy: ')        
        print(url)        
        response = requests.get(url)        
        print('status_code: {}'.format(response.status_code))        
        return response