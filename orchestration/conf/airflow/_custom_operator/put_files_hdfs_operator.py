from airflow.models.baseoperator import BaseOperator
import os
import json

"""
    Upload files to HDFS. Local files path must exist in xcom and it saves HDFS files path into xcom as output.
    """
class PutFilesHdfsOperator(BaseOperator):
    def __init__(self, parent_task_id, hdfs_folder_url, overwrite, **kwargs) -> None:
        self.parent_task_id = parent_task_id
        self.hdfs_folder_url = hdfs_folder_url
        self.overwrite = overwrite
        super().__init__(**kwargs)

    def execute(self, context):
        print(self.hdfs_folder_url)
        print('Put Files HDFS operator starting...')
        print('Getting files from xcom.')

        ti = context.get('ti')
        file_paths = json.loads(ti.xcom_pull(task_ids=self.parent_task_id))

        hdfs_file_list = []
        for file_path in file_paths:
            print('File path: {}'.format(file_path))

            file_name = os.path.basename(file_path)
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
            hdfs_file_list.append('{hdfs_folder_url}/{file_name}'.format(hdfs_folder_url=self.hdfs_folder_url, file_name=file_name))
        return hdfs_file_list
