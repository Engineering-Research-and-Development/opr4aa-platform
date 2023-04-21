from airflow.models.baseoperator import BaseOperator
import os

"""
    Create directory in HDFS
    """
class MkdirHdfsOperator(BaseOperator):
    def __init__(self, webhdfs_base_url, folder, **kwargs) -> None:
        self.webhdfs_base_url = webhdfs_base_url
        self.folder = folder
        super().__init__(**kwargs)

    def execute(self, context):
        print(self.webhdfs_base_url)
        print('Mkdir HDFS operator starting...')

        print('Directory name: {}'.format(self.folder))

        print('Executing:')
        command = "curl -i -X PUT '{}/{}?op=MKDIRS'".format(self.webhdfs_base_url, self.folder)
        print(command)
        os.system(command)
        return True
