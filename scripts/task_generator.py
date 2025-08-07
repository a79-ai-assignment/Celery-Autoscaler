from celery_app import cpu_task, io_task
import random
import time

def generate_tasks(pattern="gradual"):
    for i in range(50):
        if pattern == "gradual":
            cpu_task.delay(1000000 + i * 10000)
            io_task.delay(random.randint(1, 3))
            time.sleep(2)
        elif pattern == "burst":
            for _ in range(10):
                cpu_task.delay(1000000)
                io_task.delay(2)
            time.sleep(10)
        elif pattern == "oscillating":
            delay = 2 if i % 2 == 0 else 0.2
            cpu_task.delay(1000000)
            io_task.delay(2)
            time.sleep(delay)

if __name__ == "__main__":
    import sys
    pattern = sys.argv[1] if len(sys.argv) > 1 else "gradual"
    generate_tasks(pattern)
