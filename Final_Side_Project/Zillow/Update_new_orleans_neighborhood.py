import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Neighborhoods_in_New_Orleans"

# Send a GET request to fetch the HTML content
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the neighborhoods
table = soup.find("table", {"class": "wikitable"})

# Function to replace characters in the correct order
def format_neighborhood_name(name):
    name = name.replace('.   ', '-')
    name = name.replace('. ', '-')
    name = name.replace('.', '-')
    name = name.replace(' & ', '-')
    name = name.replace(' - ', '-')
    name = name.replace(' ', '-')
    return name.lower()

# Extract all the neighborhood names from the table
neighborhoods = []
for row in table.find_all("tr")[1:]:  # Skip the header row
    cell = row.find_all("td")[0]  # The first cell in each row contains the neighborhood name
    neighborhood = cell.text.strip()
    formatted_neighborhood = format_neighborhood_name(neighborhood)
    neighborhoods.append(formatted_neighborhood)

# Create a DataFrame and save to CSV
df = pd.DataFrame(neighborhoods, columns=["neighborhood"])
csv_path = "Update_new_orleans_neighborhoods_Result.csv"
df.to_csv(csv_path, index=False)

print(f"CSV file saved as {csv_path}")
