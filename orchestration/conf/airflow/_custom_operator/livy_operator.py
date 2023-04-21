from airflow.models.baseoperator import BaseOperator

import os
import json

"""
    [TODO]
    """
class LivyOperator(BaseOperator):
    def __init__(self, algorithm_path, hdfs_output_folder, output_extension, livy_batch_endpoint, parent_task_id, **kwargs) -> None:
        self.algorithm_path = algorithm_path
        self.output_extension = output_extension
        self.livy_batch_endpoint = livy_batch_endpoint
        self.hdfs_output_folder = hdfs_output_folder
        self.parent_task_id = parent_task_id
        super().__init__(**kwargs)

    def execute(self, context):
        ti = context.get('ti')
        print('Livy Operator starting...')
        hdfs_file_path = ti.xcom_pull(task_ids=self.parent_task_id)
        print(hdfs_file_path)

        if hdfs_file_path is None:
            hdfs_file_path = ""

        if type(hdfs_file_path) == list:
            hdfs_file_path = hdfs_file_path[0]

        file_name = ""
        if hdfs_file_path is not None and hdfs_file_path != "":
            file_name = hdfs_file_path.rsplit("/")[-1]

        output_file_path = "{hdfs_output_folder}/{file_name}.{output_extension}"\
            .format(hdfs_output_folder=self.hdfs_output_folder, file_name=file_name, output_extension=self.output_extension)
        json_object = {
            "file": self.algorithm_path,
            "args": ["{hdfs_file_path}?op=OPEN".format(hdfs_file_path=hdfs_file_path), output_file_path]
        }
        json_body = json.dumps(json_object)

        curl_body = "curl -X POST -d '{}' -H 'Content-Type: application/json' {}"\
            .format(json_body, self.livy_batch_endpoint)
        print('Executing:')
        print(curl_body)
        os.system(curl_body)
        return output_file_path