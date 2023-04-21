from airflow.sensors.filesystem import FileSensor
from airflow.hooks.filesystem import FSHook
from airflow.utils.context import Context
import os
import datetime
from glob import glob
import json

class XcomFileSensor(FileSensor):
    def poke(self, context: Context):
        hook = FSHook(self.fs_conn_id)
        basepath = hook.get_path()
        full_path = os.path.join(basepath, self.filepath)
        self.log.info("Poking for file %s", full_path)

        for path in glob(full_path, recursive=self.recursive):
            if os.path.isfile(path):
                mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y%m%d%H%M%S")
                self.log.info("Found File %s last modified: %s", str(path), mod_time)
                return True

            for _, _, files in os.walk(path):
                if len(files) > 0:
                    complete_files = []
                    for file in files:
                        complete_files.append("{}/{}".format(full_path, file))
                    context['ti'].xcom_push('return_value', json.dumps(complete_files))
                    return True
        return False