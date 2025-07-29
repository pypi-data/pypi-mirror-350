

from enum import Enum
from typing import Any
from state_of_the_art.tables.base_table import BaseTable


class TaskStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"

class TasksTable(BaseTable):
    table_name = "tasks"
    schema = {
        "task_name": {"type": str},
        "shell_cmd": {"type": str},
        "status": {"type": str},
        "logs": {"type": list},
        "log_file": {"type": str},
    }

    def create_task(self, task_name: str, shell_cmd: str) -> None:
        status = TaskStatus.NOT_STARTED.value

        self.add(task_name=task_name, shell_cmd=shell_cmd, status=status, logs="", log_file="")
    

    def print(self):
        df = self.read(recent_first=True)
        for index, row in df.iterrows():
            print(f"{row['task_name']} {row['status']} created at {row['tdw_timestamp']} uuid: {row['tdw_uuid']} c")


class TaskEntity:
    def __init__(self, task_name: str, shell_cmd: str, status: str):
        self.task_name = task_name
        self.shell_cmd = shell_cmd
        self.status = status
