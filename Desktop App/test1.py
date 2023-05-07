import pandas as pd
import matplotlib.pyplot as plt

# Read in the CSV file with column headers specified
df = pd.read_csv('LOG.CSV', names=['CurrentTime', 'satellites', 'speed', 'latitude', 'longitude', 'x', 'y', 'z', 'temperature', 'altitude', 'currentLap'])

# Convert the CurrentTime column to a datetime object
df['CurrentTime'] = pd.to_datetime(df['CurrentTime'], format='%H:%M:%S')

# Plot the temperature data over time
plt.plot(df['CurrentTime'].values, df['temperature'].values)
plt.title('Temperature over Time')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.show()

# Plot the x,y,z accelerometer data over time
plt.plot(df['CurrentTime'].values, df['x'].values, label='x')
plt.plot(df['CurrentTime'].values, df['y'].values, label='y')
plt.plot(df['CurrentTime'].values, df['z'].values, label='z')
plt.title('Accelerometer Readings over Time')
plt.xlabel('Time')
plt.ylabel('Acceleration (m/s^2)')
plt.legend()
plt.show()

# Plot the GPS data as a scatter plot
plt.scatter(df['longitude'].values, df['latitude'].values)
plt.title('GPS Data')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()