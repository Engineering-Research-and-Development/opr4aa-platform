from airflow.models.baseoperator import BaseOperator
import requests
import json

# Create livy session if not exists. It saves session_id and session_name into xcom.
class CreateLivySession(BaseOperator):
    def __init__(self, livy_url, kind, session_name, py_files, **kwargs):
        self.kind = kind
        self.livy_url = livy_url
        self.session_name = session_name
        self.py_files = py_files
        super().__init__(**kwargs)

    def execute(self, context):
        response = self.create_session()
        if response.status_code == 201:
            jsonbody = response.json()
            print(jsonbody)
            obj = {'session_id': jsonbody['id'], 'session_name': jsonbody['name']}
            context['ti'].xcom_push('return_value', json.dumps(obj))
            return obj
        elif response.status_code == 400:
            jsonbody = response.json()
            print(jsonbody)
            if "Duplicate session name" in jsonbody['msg']:
                print("Duplicate session name")
                session = self.find_session(self.session_name)
                session_id = session['id']

                if session['state'] == 'error' or session['state'] == 'dead' or session['state'] == 'killed':
                    self.delete_session(session_id)
                    jsonbody = self.create_session().json()
                    session_id = jsonbody['session_id']

                obj = {'session_id': session_id, 'session_name': self.session_name}
                context.get('ti').xcom_push(key="return_value", value=json.dumps(obj))
                return obj
            else:
                raise Exception("Something went wrong: {}".format(jsonbody['msg']))
        else:
            raise Exception("Something went wrong: {}".format(response))

    def create_session(self):
        url = '{}/sessions'.format(self.livy_url)
        jsonbody = {'name': self.session_name, 'kind': self.kind, 'pyFiles': self.py_files}
        print('Sending request to Livy:')
        print(url)
        print(jsonbody)
        response = requests.post(url, json=jsonbody)
        print('status_code: {}'.format(response.status_code))
        return response

    def find_session(self, session_name):
        url = '{}/sessions'.format(self.livy_url)
        print('Sending request to Livy: ')
        print(url)
        response = requests.get(url)
        jsonbody = response.json()
        for session in jsonbody['sessions']:
            if session['name'] == session_name:
                print('Found session for session_name {} and id {}'.format(session_name, session['id']))
                return session
        return -1

    def delete_session(self, session_id):
        url = '{}/sessions/{}'.format(self.livy_url, session_id)
        print('Sending request to Livy: ')
        print(url)
        response = requests.delete(url)
        if response.status_code != 200:
            raise Exception("Cannot delete session.")
        return session_id
