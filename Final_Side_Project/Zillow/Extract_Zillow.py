import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Load neighborhoods and their URLs from CSV file
input_csv_path = "Update_new_orleans_neighborhoods_Result.csv"
neighborhoods_df = pd.read_csv(input_csv_path)

# Function to fetch property addresses and detail URLs from Zillow URL
def fetch_property_addresses(url):
    addresses = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract JSON-LD script tags
        script_tags = soup.find_all("script", type="application/ld+json")
        for script in script_tags:
            try:
                json_data = json.loads(script.string)
                if json_data.get("@type") == "SingleFamilyResidence":
                    address = json_data.get("name")
                    detail_url = json_data.get("url")
                    addresses.append({'address': address, 'detail_url': detail_url})
            except json.JSONDecodeError:
                continue
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
    
    return addresses

# Create a new DataFrame to store neighborhood, address, and detail URL pairs
addresses_list = []

# Iterate over each neighborhood and its URL
for index, row in neighborhoods_df.iterrows():
    neighborhood = row['neighborhood']
    url = row['url']
    properties = fetch_property_addresses(url)
    for property in properties:
        property['neighborhood'] = neighborhood
        addresses_list.append(property)

# Convert the list of dictionaries to a DataFrame
addresses_df = pd.DataFrame(addresses_list)

# Save the addresses DataFrame to a new CSV file
output_csv_path = "Extract_Zillow_Result.csv"
addresses_df.to_csv(output_csv_path, index=False)

print(f"CSV file saved as {output_csv_path}")
