import pandas as pd
import folium

# Read in the CSV file with column headers specified
df = pd.read_csv('LOG.CSV', names=['CurrentTime', 'satellites', 'speed', 'latitude', 'longitude', 'x', 'y', 'z', 'temperature', 'altitude', 'currentLap'])

# Convert the latitude and longitude columns to floats
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

# Create a map centered on the mean latitude and longitude
map = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=13)

# Add markers to the map for each GPS coordinate
for index, row in df.iterrows():
    folium.Marker(location=[row['latitude'], row['longitude']]).add_to(map)

# Display the map
map
