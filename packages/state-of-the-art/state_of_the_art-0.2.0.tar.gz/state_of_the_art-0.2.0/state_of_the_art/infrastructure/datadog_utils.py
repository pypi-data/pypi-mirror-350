import os
import time
from typing import List, Optional
import datadog


def setup_datadog(disable_exception: bool = False):
    if os.environ.get("SOTA_TEST"):
        print("Skipping datadog setup in test mode")
        return

    if not os.getenv("DATADOG_API_KEY"):
        if not disable_exception:
            raise ValueError("DATADOG_API_KEY is not set")
        else:
            print("DATADOG_API_KEY is not set")
    if not os.getenv("DATADOG_APP_KEY"):
        if not disable_exception:
            raise ValueError("DATADOG_APP_KEY is not set")
        else:
            print("DATADOG_APP_KEY is not set")

    datadog.initialize(return_raw_response=True, host_name='https://api.datadoghq.eu')

    print("Datadog initialized successfully" ) 
    print(" Datadog API key: '" + os.getenv("DATADOG_API_KEY", "not set") + "' and app key: '" + os.getenv("DATADOG_APP_KEY", "not set") + "'")


def test(value: int= 123):
    setup_datadog()
    send_metric(metric="my.test2", value=value)

def send_metric(metric: str, value: int, metric_type: str = "gauge", tags: Optional[List[str]]=None):
    #  get now as timestamp
    now = int(time.time())
    points = [(now, value)]
    if os.environ.get("SOTA_TEST"):
        print(f"Skipping datadog send_metric in test mode {metric}={points}")
        return

    result = datadog.api.Metric.send(metric=metric, points=points, type=metric_type, tags=tags)
    print(f"Datadog call {metric}={points} result: {result}")

    
    if len(result) < 2 or result[0]['status'] != 'ok':
        raise ValueError(f"Failed to send metric {metric} with value {value}")

    return result


if __name__ == "__main__":
    import fire
    fire.Fire()
