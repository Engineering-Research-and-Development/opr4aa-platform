from airflow.models.baseoperator import BaseOperator
import os
import json

"""
    Upload a file to HDFS. Local file path must exist on xcom variable "file_path" and it saves HDFS uploaded file path
    into xcom variable hdfs_file_path.
    """
class GetHdfsOperator(BaseOperator):
    def __init__(self, parent_task_id, webhdfs_folder_url, save_folder, **kwargs) -> None:
        self.parent_task_id = parent_task_id
        self.webhdfs_folder_url = webhdfs_folder_url
        self.save_folder = save_folder
        super().__init__(**kwargs)

    def execute(self, context):
        print('Get HDFS operator starting...')
        print('Getting file path from xcom.')
        ti = context.get('ti')
        files = json.loads(ti.xcom_pull(task_ids=self.parent_task_id))
        saved_files = []
        for file in files:
            print('File path: {}'.format(file["path"]))
            file_name = os.path.basename(file["path"])
            print('Executing:')
            command = 'curl -L -s "{webhdfs_folder_url}/{file_path}?op=OPEN" > {save_folder}/{file_name}'\
                .format(webhdfs_folder_url=self.webhdfs_folder_url, file_path=file['path'],
                        save_folder=self.save_folder, file_name=file_name)
            print(command)
            os.system(command)
            saved_files.append('{save_folder}/{file_name}'.format(save_folder=self.save_folder, file_name=file_name))

        return json.dumps(saved_files)