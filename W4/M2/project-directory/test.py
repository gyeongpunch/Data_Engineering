import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import matplotlib.pyplot as plt
import seaborn as sns

# URL of the webpage containing the weather data
base_url = "https://world-weather.info"
main_url = "https://world-weather.info/forecast/usa/new_york/january-2024/"

# Define headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send a GET request to the main webpage
response = requests.get(main_url, headers=headers)
response.raise_for_status()  # Check if the request was successful

# Parse the main webpage content
soup = BeautifulSoup(response.content, "html.parser")

# Initialize lists to store the data
dates = []
night_temps = []
morning_temps = []
day_temps = []
evening_temps = []

# Find all the relevant forecast data in the webpage
forecast_items = soup.select("ul.ww-month li.foreacast-archive a")

# Function to extract temperature from a span text
def extract_temperature(span_text):
    return int(span_text.replace("°", "").replace("+", "").replace("−", "-"))

# Iterate through each forecast item and extract the required data
for item in forecast_items:
    # Get the date from the div text
    date = item.find("div").get_text()
    dates.append(date)
    
    # Get the URL for the detailed forecast
    detail_url = urljoin(base_url, item['href'])
    
    # Send a GET request to the detailed forecast webpage
    detail_response = requests.get(detail_url, headers=headers)
    detail_response.raise_for_status()
    
    # Parse the detailed forecast webpage content
    detail_soup = BeautifulSoup(detail_response.content, "html.parser")
    
    # Extract temperatures for night, morning, day, evening
    night_temp = extract_temperature(detail_soup.select_one("tr.night td.weather-temperature span").get_text())
    morning_temp = extract_temperature(detail_soup.select_one("tr.morning td.weather-temperature span").get_text())
    day_temp = extract_temperature(detail_soup.select_one("tr.day td.weather-temperature span").get_text())
    evening_temp = extract_temperature(detail_soup.select_one("tr.evening td.weather-temperature span").get_text())
    
    night_temps.append(night_temp)
    morning_temps.append(morning_temp)
    day_temps.append(day_temp)
    evening_temps.append(evening_temp)

# Create a DataFrame
data = {
    "Date": dates,
    "Night Temperature (°F)": night_temps,
    "Morning Temperature (°F)": morning_temps,
    "Day Temperature (°F)": day_temps,
    "Evening Temperature (°F)": evening_temps
}

df = pd.DataFrame(data)

# Convert temperatures from Fahrenheit to Celsius
df["Night Temperature (°C)"] = (df["Night Temperature (°F)"] - 32) * 5.0 / 9.0
df["Morning Temperature (°C)"] = (df["Morning Temperature (°F)"] - 32) * 5.0 / 9.0
df["Day Temperature (°C)"] = (df["Day Temperature (°F)"] - 32) * 5.0 / 9.0
df["Evening Temperature (°C)"] = (df["Evening Temperature (°F)"] - 32) * 5.0 / 9.0

# Load the trip count data
trip_counts = pd.read_csv('/Users/admin/Desktop/Data_Engineering/W4/M2/project-directory/results/hourly_trips.csv')

# Define the representative hours for each period
periods = {
    'Night': list(range(0, 6)),
    'Morning': list(range(6, 12)),
    'Day': list(range(12, 18)),
    'Evening': list(range(18, 24))
}

# Add a period column to the trip_counts DataFrame
trip_counts['period'] = trip_counts['hour'].apply(lambda x: 'Night' if x in periods['Night'] else ('Morning' if x in periods['Morning'] else ('Day' if x in periods['Day'] else 'Evening')))

# Add columns for trip counts in the df DataFrame
df['Night_trip_count'] = 0
df['Morning_trip_count'] = 0
df['Day_trip_count'] = 0
df['Evening_trip_count'] = 0

# Populate trip count columns for each date
for i, date in enumerate(df['Date']):
    # Filter the trip counts for the specific date
    daily_trip_counts = trip_counts[(trip_counts['hour'] // 24) == i]

    # Sum trip counts for each period
    df.at[i, 'Night_trip_count'] = daily_trip_counts[daily_trip_counts['period'] == 'Night']['trip_count'].sum()
    df.at[i, 'Morning_trip_count'] = daily_trip_counts[daily_trip_counts['period'] == 'Morning']['trip_count'].sum()
    df.at[i, 'Day_trip_count'] = daily_trip_counts[daily_trip_counts['period'] == 'Day']['trip_count'].sum()
    df.at[i, 'Evening_trip_count'] = daily_trip_counts[daily_trip_counts['period'] == 'Evening']['trip_count'].sum()

# Calculate the correlation matrix
correlation_matrix = df[[
    'Night Temperature (°C)', 'Morning Temperature (°C)', 
    'Day Temperature (°C)', 'Evening Temperature (°C)', 
    'Night_trip_count', 'Morning_trip_count', 
    'Day_trip_count', 'Evening_trip_count'
]].corr()

# Plot the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix between Temperatures and Taxi Trip Counts')
plt.show()
