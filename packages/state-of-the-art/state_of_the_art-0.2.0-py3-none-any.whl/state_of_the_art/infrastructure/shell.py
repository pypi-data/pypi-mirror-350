


import subprocess
from typing import Iterator
from unittest import result

class ShellRunner:
    def run_waiting(self, command: str, exception_on_error: bool = True) -> str:
        print("Shell Runner command: ", command)
        p = subprocess.Popen(
            command,
            shell=True,
            text=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        out, error = p.communicate()
        result = out if out else ""
        result += error if error else ""
        if exception_on_error and p.returncode != 0:
            raise Exception(f"Failed to run command: {command}\n{result}")
        return result
    
    def run_in_background(self, command: str) -> None:
        # run in background does not wait for the command to finish 
        subprocess.Popen(command, shell=True, text=True)


    def run_and_yield_intermediate_results(self, command: str, exception_on_error: bool = True) -> Iterator[str]:
        p = subprocess.Popen(
            command,
            shell=True,
            text=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        # also yield the error
        while p.poll() is None:
            yield p.stdout.readline()
            yield p.stderr.readline()

        # get stderr complete
        error = p.stderr.read()
        if exception_on_error and p.returncode != 0:
            raise Exception(f"Failed to run command: {command}\n{error}")
