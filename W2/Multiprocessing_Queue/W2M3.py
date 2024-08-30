import multiprocessing
import time

def push_items(queue, items):
    print("pushing items to queue:")
    for i, item in enumerate(items):
        queue.put(item)
        print(f"item no: {i+1} {item}")
        time.sleep(0.5)  # simulate some delay

def pop_items(queue):
    print("\npopping items from queue:")
    i = 0
    while not queue.empty():
        item = queue.get()
        print(f"item no: {i+1} {item}")
        i += 1
        time.sleep(0.5)  # simulate some delay

if __name__ == "__main__":
    # Define the list of items to be pushed to the queue
    items = ["red", "green", "blue", "black"]

    # multiprocessing queue
    queue = multiprocessing.Queue()

    # Process for pushing items to the queue
    push_process = multiprocessing.Process(target=push_items, args=(queue, items))
    # Process for popping items from the queue
    pop_process = multiprocessing.Process(target=pop_items, args=(queue,))

    # Start the push process
    push_process.start()
    # Wait for the push process to finish
    push_process.join()

    # Start the pop process
    pop_process.start()
    # Wait for the pop process to finish
    pop_process.join()
