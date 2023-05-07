import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telemetry Data")

        # Load the image from file using QPixmap
        self.image_label = QLabel(self)
        pixmap = QPixmap('logo_equipo.png')
        pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        # Create buttons
        self.temp_button = QPushButton("Temperature")
        self.accel_button = QPushButton("Accelerometer Readings")
        self.gps_button = QPushButton("GPS Data")

        # Add buttons to layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
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
        temp_window = TemperatureWindow(self.df)
        temp_window.show()


    def show_accel(self):
        # Plot the x,y,z accelerometer data over time
        accel_window = AccelerometerWindow(self.df)
        accel_window.show()


    def show_gps(self):
        # Plot the GPS data as a scatter plot
        gps_window = GPSWindow(self.df)
        gps_window.show()


class TemperatureWindow(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.setWindowTitle("Temperature over Time")

        # Plot the temperature data over time
        plt.plot(self.df['CurrentTime'].values, self.df['temperature'].values)
        plt.xlabel('Time')
        plt.ylabel('Temperature')

        # Create a canvas widget and add the plot to it
        canvas = plt.gcf().canvas
        canvas.setParent(self)

        # Resize the canvas to fit the window
        canvas.setGeometry(0, 0, 800, 600)


class AccelerometerWindow(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.setWindowTitle("Accelerometer Readings over Time")

        # Plot the x,y,z accelerometer data over time
        plt.plot(self.df['CurrentTime'].values, self.df['x'].values, label='x')
        plt.plot(self.df['CurrentTime'].values, self.df['y'].values, label='y')
        plt.plot(self.df['CurrentTime'].values, self.df['z'].values, label='z')
        plt.xlabel('Time')
       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())