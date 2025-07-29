import os
from state_of_the_art.tables.base_table import BaseTable
from typing import Optional
import subprocess

class Changelog(BaseTable):
    table_name = "changelog"
    schema = {"message": {"type": str}, "by_user": {"type": Optional[str]}}

    def add_log(self, message: str, by_user: Optional[str] = None):
        if not by_user:
            by_user = get_host_machine_name()
        print(f"Adding changelog entry: {message} by {by_user}")
        self.add(message=message, by_user=by_user)



def get_host_machine_name() -> str:
    result = subprocess.check_output("uname -n", shell=True, text=True).strip()

    return result[0:30]
