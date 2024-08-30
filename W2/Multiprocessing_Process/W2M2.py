import multiprocessing

# function that prints the continent name
def print_continent(name="Asia"):
    print(f"The name of continent is : {name}")

if __name__ == "__main__":
    # Create a list of continent
    continents = ["Asia", "North America", "Europe", "Africa", "Oceania", "South America"]

    # Llist to hold the process objects
    processes = []

    # Process for each continent in the list
    for continent in continents:
        process = multiprocessing.Process(target=print_continent, args=(continent,))
        processes.append(process)
        process.start()

    # print('!!!!!!!!')

    # Wait for all processes to complete
    for process in processes:
        process.join()
