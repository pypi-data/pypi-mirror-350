

from typing import Iterator
from state_of_the_art.infrastructure.datadog_utils import send_metric
from state_of_the_art.infrastructure.shell import ShellRunner
from state_of_the_art.tables.open_tasks_table import TasksTable, TaskStatus


class TasksRunner:
    def __init__(self):
        self.tasks_table = TasksTable()

    def run_a_pending_task(self, yield_info: bool = False) -> Iterator[str]:
        print("Running a pending task, yield_info is", yield_info)
        yield "Starting to run a task"

        tasks_df = self.tasks_table.read(recent_first=True)
        filtered_tasks_df = tasks_df[tasks_df["status"] == TaskStatus.NOT_STARTED.value]

        if len(filtered_tasks_df) == 0:
            yield "No open tasks left to run"
            send_metric("sota.tasks_runner.no_tasks", 1)
            return
        
        task = filtered_tasks_df.iloc[0]
        yield f"Running {task['shell_cmd']} for task with uuid {task['tdw_uuid']} created at {task['tdw_timestamp']}"

        send_metric("sota.tasks_runner.task_started", 1)

        # create a log file
        log_file = f"/tmp/task_{task['tdw_uuid']}.log"
        print(f"Creating log file at {log_file}")
        self.tasks_table.update(by_key="tdw_uuid", by_value=task["tdw_uuid"], new_values={"status": TaskStatus.STARTED.value, "log_file": log_file})

        cmd = "nohup " + task["shell_cmd"] + " | tee " + log_file
        for line in ShellRunner().run_and_yield_intermediate_results(cmd):
                yield line
        self.tasks_table.update(by_key="tdw_uuid", by_value=task["tdw_uuid"], new_values={"status": TaskStatus.SUCCESS.value})
        send_metric("sota.tasks_runner.task_completed", 1)

if __name__ == "__main__":
    import fire
    fire.Fire(TasksRunner)
