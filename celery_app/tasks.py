import time
from . import app

@app.task
def cpu_task(n):
    result = 0
    for i in range(n):
        result += i*i
    return result

@app.task
def io_task(seconds):
    time.sleep(seconds)
    return f"Slept for {seconds} seconds"
