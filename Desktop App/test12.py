import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telemetry Data")

        # Create buttons
        self.temp_button = QPushButton("Temperature")
        self.accel_button = QPushButton("Accelerometer Readings")
        self.gps_button = QPushButton("GPS Data")

        # Add buttons to layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.temp_button)
        layout.addWidget(self.accel_button)
        layout.addWidget(self.gps_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect buttons to their respective functions
        self.temp_button.clicked.connect(self.show_temp)
        self.accel_button.clicked.connect(self.show_accel)
        self.gps_button.clicked.connect(self.show_gps)

        # Read in the CSV file with column headers specified
        self.df = pd.read_csv('LOG.CSV', names=['CurrentTime', 'satellites', 'speed', 'latitude', 'longitude', 'x', 'y', 'z', 'temperature', 'altitude', 'currentLap'])

        # Convert the CurrentTime column to a datetime object
        self.df['CurrentTime'] = pd.to_datetime(self.df['CurrentTime'], format='%H:%M:%S')

    def show_temp(self):
        # Plot the temperature data over time
        plt.plot(self.df['CurrentTime'].values, self.df['temperature'].values)
        plt.title('Temperature over Time')
        plt.xlabel('Time')
        plt.ylabel('Temperature')
        plt.show()

    def show_accel(self):
        # Plot the x,y,z accelerometer data over time
        plt.plot(self.df['CurrentTime'].values, self.df['x'].values, label='x')
        plt.plot(self.df['CurrentTime'].values, self.df['y'].values, label='y')
        plt.plot(self.df['CurrentTime'].values, self.df['z'].values, label='z')
        plt.title('Accelerometer Readings over Time')
        plt.xlabel('Time')
        plt.ylabel('Acceleration (m/s^2)')
        plt.legend()
        plt.show()

    def show_gps(self):
        # Plot the GPS data as a scatter plot
        plt.scatter(self.df['longitude'].values, self.df['latitude'].values)
        plt.title('GPS Data')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
