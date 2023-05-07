import sys
from random import randint

import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class MatGraph(QWidget):
    def __init__(self, df):
        super().__init__()

        self.setWindowTitle("Graph 1")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Plot the temperature data on the figure
        ax = self.figure.add_subplot(111)
        ax.plot(df['CurrentTime'].values, df['temperature'].values)
        ax.set_title('Temperature over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature')

        # Create a navigation toolbar and add it to the layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


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

        # Add elements to the layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.temp_button)
        layout.addWidget(self.accel_button)
        layout.addWidget(self.gps_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect buttons to their respective functions
        self.temp_button.clicked.connect(self.toggle_window1)
        self.accel_button.clicked.connect(self.toggle_window2)
        self.gps_button.clicked.connect(self.toggle_window1)

        # Read in the CSV file with column headers specified
        self.df = pd.read_csv('LOG.CSV', names=['CurrentTime', 'satellites', 'speed', 'latitude', 'longitude', 'x', 'y', 'z', 'temperature', 'altitude', 'currentLap'])

        # Convert the CurrentTime column to a datetime object
        self.df['CurrentTime'] = pd.to_datetime(self.df['CurrentTime'], format='%H:%M:%S')

        self.window1 = MatGraph(self.df)
        self.window2 = MatGraph(self.df)

    def toggle_window1(self, checked):
        if self.window1.isVisible():
            self.window1.hide()
        else:
            self.window1.show()

    def toggle_window2(self, checked):
        if self.window2.isVisible():
            self.window2.hide()
        else:
            self.window2.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
