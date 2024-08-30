import multiprocessing
import time

# list of tasks with name and duration
tasks = [
    ('A', 5),
    ('B', 2),
    ('C', 1),
    ('D', 3),
]

# Simulate each task
def work_log(task):
    name, duration = task
    print(f"Process {name} waiting {duration} seconds")
    time.sleep(duration)
    print(f"Process {name} Finished.")

if __name__ == "__main__":
    # Pool with 2 workers
    with multiprocessing.Pool(2) as pool:
        # Map the work_log function to the list of tasks
        pool.map(work_log, tasks)
