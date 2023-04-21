from airflow.models.baseoperator import BaseOperator
import os
import json
import time

"""
    Upload a file to HDFS. Local file path must exist in xcom and it saves HDFS file path into xcom as output.
    If deserialize=True it convert xcom json in a regular json file in file system and then upload it to HDFS.
    """
class PutHdfsOperator(BaseOperator):
    def __init__(self, parent_task_id, hdfs_folder_url, overwrite, deserialize=False, tmp_folder="/opt/airflow/tmp", **kwargs) -> None:
        self.parent_task_id = parent_task_id
        self.hdfs_folder_url = hdfs_folder_url
        self.overwrite = overwrite
        self.deserialize = deserialize
        self.tmp_folder = tmp_folder
        super().__init__(**kwargs)

    def execute(self, context):
        print(self.hdfs_folder_url)
        print('Put HDFS operator starting...')
        print('Getting file from xcom.')

        ti = context.get('ti')
        file_path = ""
        file_name = ""

        if self.deserialize is True :
            json_obj = ti.xcom_pull(task_ids=self.parent_task_id)
            print(json_obj)
            file_path = "{}/{}.json".format(self.tmp_folder, int(time.time()))
            file_name = "{}.json".format(int(time.time()))
            with open(file_path, "w") as outfile:
                outfile.write(json_obj)
        else:
            file_path = ti.xcom_pull(task_ids=self.parent_task_id)
            print('File path: {}'.format(file_path))
            file_name = os.path.basename(file_path)

        print('Getting file {}'.format(file_name))
        print('Saving file to {}/{}'.format(self.hdfs_folder_url, file_name))

        b_overwrite = 'false'
        if self.overwrite:
            b_overwrite = 'true'

        print('Executing:')
        command = "curl -i -T {file_path} '{hdfs_folder_url}/{file_name}?op=CREATE&overwrite={b_overwrite}' -L"\
            .format(hdfs_folder_url=self.hdfs_folder_url, file_path=file_path, file_name=file_name,
                    b_overwrite=b_overwrite)
        print(command)

        os.system(command)
        return '{hdfs_folder_url}/{file_name}'.format(hdfs_folder_url=self.hdfs_folder_url, file_name=file_name)
