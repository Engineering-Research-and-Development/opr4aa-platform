import json
import re
from airflow.providers.apache.hdfs.sensors.hdfs import HdfsRegexSensor

"""
    Poke a directory in HDFS and save path of files matching the regex in xcom variable "return_value".
    """
class ListHdfsRegexSensor(HdfsRegexSensor):
    def poke(self, context):
        sb_client = self.hook(self.hdfs_conn_id).get_conn()
        self.log.info(
            "Poking for %s to be a directory with files matching %s", self.filepath, self.regex.pattern
        )
        result = [
            f
            for f in sb_client.ls([self.filepath], include_toplevel=False)
            if f["file_type"] == "f" and self.regex.match(f["path"].replace(f"{self.filepath}/", ""))
        ]
        result = self.filter_for_ignored_ext(result, self.ignored_ext, self.ignore_copying)
        result = self.filter_for_filesize(result, self.file_size)
        context['ti'].xcom_push('return_value', json.dumps(result))
        return True

class HdfsFileSensor(HdfsRegexSensor):
    def __init__(self, parent_task_id, **kwargs) -> None:
        self.parent_task_id = parent_task_id
        super().__init__(**kwargs)

    def poke(self, context):
        file_path = context['ti'].xcom_pull(task_ids=self.parent_task_id)
        print('file_path:')
        print(file_path)
        sb_client = self.hook(self.hdfs_conn_id).get_conn()
        self.log.info(
            "Poking for %s to be a directory with files matching %s", self.filepath, file_path
        )
        result = [
            f
            for f in sb_client.ls([self.filepath], include_toplevel=False)
            if f["file_type"] == "f" and f["path"] == file_path
        ]
        result = self.filter_for_ignored_ext(result, self.ignored_ext, self.ignore_copying)
        result = self.filter_for_filesize(result, self.file_size)
        if len(result) > 0:
            context['ti'].xcom_push('return_value', json.dumps(result))
        return bool(result)