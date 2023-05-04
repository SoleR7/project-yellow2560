import pandas as pd
import matplotlib.pyplot as plt

# Read in the CSV file with column headers specified
df = pd.read_csv('LOG.CSV', names=['CurrentTime', 'satellites', 'speed', 'latitude', 'longitude', 'x', 'y', 'z', 'temperature', 'altitude', 'currentLap'])

# Print the column names
print(df.columns)

# Print the first few rows of the DataFrame
print(df.head())

# Convert the CurrentTime column to a datetime object
df['CurrentTime'] = pd.to_datetime(df['CurrentTime'])

# Plot the temperature data over time
plt.plot(df['CurrentTime'], df['temperature'])
plt.title('Temperature over Time')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.show()

# Plot the x,y,z accelerometer data over time
plt.plot(df['CurrentTime'], df['x'], label='x')
plt.plot(df['CurrentTime'], df['y'], label='y')
plt.plot(df['CurrentTime'], df['z'], label='z')
plt.title('Accelerometer Readings over Time')
plt.xlabel('Time')
plt.ylabel('Acceleration (m/s^2)')
plt.legend()
plt.show()

# Plot the GPS data as a scatter plot
plt.scatter(df['longitude'], df['latitude'])
plt.title('GPS Data')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()