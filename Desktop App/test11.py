import sys
import csv
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class TelemetryData():
    def __init__(self, filename):
        self.filename = filename
        self.current_time = []
        self.satellites = []
        self.speed = []
        self.latitude = []
        self.longitude = []
        self.x = []
        self.y = []
        self.z = []
        self.temperature = []
        self.altitude = []
        self.current_lap = []
        
        self.load_data()

    def load_data(self):
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            for row in reader:
                self.current_time.append(row[0])
                self.satellites.append(float(row[1]))
                self.speed.append(float(row[2]))
                self.latitude.append(float(row[3]))
                self.longitude.append(float(row[4]))
                self.x.append(float(row[5]))
                self.y.append(float(row[6]))
                self.z.append(float(row[7]))
                self.temperature.append(float(row[8]))
                self.altitude.append(float(row[9]))
                self.current_lap.append(float(row[10]))

class MainWindow(QMainWindow):
    def __init__(self, telemetry_data):
        super().__init__()

        self.telemetry_data = telemetry_data

        # Create plot widgets
        self.speed_plot = PlotWidget('Speed (km/h)', 'Time (s)', self.telemetry_data.current_time, self.telemetry_data.speed)
        self.temperature_plot = PlotWidget('Temperature (C)', 'Time (s)', self.telemetry_data.current_time, self.telemetry_data.temperature)
        self.altitude_plot = PlotWidget('Altitude (m)', 'Time (s)', self.telemetry_data.current_time, self.telemetry_data.altitude)

        # Create main layout
        layout = QHBoxLayout()
        layout.addWidget(self.speed_plot)
        layout.addWidget(self.temperature_plot)
        layout.addWidget(self.altitude_plot)

        # Create main widget and set layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set maximum size of main window
        self.setMaximumSize(400, 600)

        self.setWindowTitle('Telemetry Data Viewer')

class PlotWidget(QWidget):
    def __init__(self, title, x_label, x_data, y_data):
        super().__init__()

        # Create a figure and axes for the plot
        self.figure, self.ax = plt.subplots()
        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.plot(x_data, y_data)

        # Create a canvas for the plot
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(600, 400)

        # Create a layout and add the canvas
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load telemetry data from CSV file
    telemetry_data = TelemetryData('LOG.CSV')

    # Create main window and show it
    window = MainWindow(telemetry_data)
    window.show()

    sys.exit(app.exec_())
