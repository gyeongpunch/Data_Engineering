import multiprocessing
import time

def worker(tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
        except multiprocessing.queues.Empty:
            break
        else:
            # Simulate task execution
            print(f"Task no {task[0]}")
            time.sleep(0.5)
            tasks_that_are_done.put((task[0], task[1]))
            tasks_to_accomplish.task_done()

if __name__ == '__main__':
    num_tasks = 10
    num_processes = 4

    # Create queues
    tasks_to_accomplish = multiprocessing.JoinableQueue()
    tasks_that_are_done = multiprocessing.Queue()

    # Add tasks to the queue, assigning each to a specific process
    for i in range(num_tasks):
        tasks_to_accomplish.put((i, (i % num_processes) + 1))

    # Create processes
    processes = []
    for i in range(num_processes):
        process = multiprocessing.Process(target=worker, args=(tasks_to_accomplish, tasks_that_are_done))
        processes.append(process)
        process.start()

    # 모든 작업이 완료되었음을 보장
    tasks_to_accomplish.join()

    # Ensure all processes have finished
    for process in processes:
        process.join()

    # Collect all results
    results = []
    while not tasks_that_are_done.empty():
        results.append(tasks_that_are_done.get())

    # Sort results to ensure order by task number
    results.sort(key=lambda x: x[0])

    # Print out the completion messages in order
    for task, process_number in results:
        print(f"Task no {task} is done by Process-{process_number}")
