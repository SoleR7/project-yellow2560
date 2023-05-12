import sys
import pandas as pd
import csv
from datetime import datetime, timedelta
from fontTools.merge import first
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
    QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from numpy import number


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.csv_file_name = None

        # GUI
        self.setWindowTitle("UPV Eco-Marathon Telemetry App")

        # logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap('logo_equipo.png')
        pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        # open csv file
        self.csv_button = QPushButton("open csv file...")
        self.csv_button.clicked.connect(self.open_csv_file)

        # csv file info
        self.info_label_sessionTime = QLabel('Session time: ')
        self.info_label_gpsSats = QLabel('Avg GPS Satellites: ')
        self.info_label_laps= QLabel('Laps: ')
        self.info_label_temp = QLabel('Avg temp: ')
        #self.info_label_temp.setVisible(False)
        self.info_label_elevation = QLabel('Elevation change: ')
        self.info_label_elevation.setEnabled(False)
        

        # buttons
        self.racingLineMap_button = QPushButton("Racing line")
        self.racingLineMap_button.clicked.connect(self.racingLineMap_plot)
        self.racingLineMap_button.setEnabled(False)

        self.circuitElevation_button = QPushButton("Circuit Elevation")
        self.circuitElevation_button.clicked.connect(self.circuitElevation_plot)
        self.circuitElevation_button.setEnabled(False)

        self.speed_button = QPushButton("Speed")
        self.speed_button.clicked.connect(self.speed_plot)
        self.speed_button.setEnabled(False)

        self.accelerometer_button = QPushButton("Accelerometer")
        self.accelerometer_button.clicked.connect(self.accelerometer_plot)
        self.accelerometer_button.setEnabled(False)

        self.temperature_button = QPushButton("Temperature")
        self.temperature_button.clicked.connect(self.temperature_plot)
        self.temperature_button.setEnabled(False)

        # layouts
        main_v_layout = QVBoxLayout()
        first_h_layout = QHBoxLayout()
        second_h_layout = QHBoxLayout()
        info_v_layout_left = QVBoxLayout()
        info_v_layout_right = QVBoxLayout()
        button_h_layout_one = QHBoxLayout()
        button_h_layout_two = QHBoxLayout()
        button_h_layout_three = QHBoxLayout()

        main_v_layout.addWidget(self.logo_label)
        main_v_layout.addLayout(first_h_layout)
        main_v_layout.addLayout(second_h_layout)
        main_v_layout.addLayout(button_h_layout_one)
        main_v_layout.addLayout(button_h_layout_two)
        main_v_layout.addLayout(button_h_layout_three)

        first_h_layout.addWidget(self.csv_button)
        first_h_layout.setContentsMargins(150, 10, 150, 30)
        
        second_h_layout.addLayout(info_v_layout_left)
        second_h_layout.addLayout(info_v_layout_right)
        second_h_layout.setContentsMargins(70, 10, 70, 5)
        
        info_v_layout_left.addWidget(self.info_label_sessionTime)
        info_v_layout_left.addWidget(self.info_label_gpsSats)
        info_v_layout_left.addWidget(self.info_label_laps)
        info_v_layout_left.addWidget(self.info_label_temp)
        info_v_layout_left.addWidget(self.info_label_elevation)

        button_h_layout_one.addWidget(self.racingLineMap_button)
        button_h_layout_one.addWidget(self.circuitElevation_button)
        button_h_layout_one.setContentsMargins(90, 10, 90, 5)

        button_h_layout_two.addWidget(self.speed_button)
        button_h_layout_two.addWidget(self.accelerometer_button)
        button_h_layout_two.setContentsMargins(90, 0, 90, 5)

        button_h_layout_three.addWidget(self.temperature_button)
        button_h_layout_three.setContentsMargins(90, 0, 90, 20)

        # placeholder widget to hold the main layout.
        widget = QWidget()
        widget.setLayout(main_v_layout)
        self.setCentralWidget(widget)

    def open_csv_file(self):
        # Open a file dialog to choose a CSV file
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setDefaultSuffix("csv")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            # Get the name of the selected file and store it in self.csv_file_name
            self.csv_file_name = file_dialog.selectedFiles()[0]
            print(self.csv_file_name)

            # check if the file is valid
            if self.is_valid_csv_file(self.csv_file_name, 11):
                print("csv is valid!")
                
                # extract info from csv file
                self.csv_info = self.extract_csv_info(self.csv_file_name, 11)
                
                # update info section
                self.info_label_sessionTime.setText("Session time: "+self.csv_info["elapsed_time"])
                self.info_label_gpsSats.setText("Avg GPS Satellites: " + str(self.csv_info["avg_satellites"]))
                self.info_label_laps.setText("Laps: " + str(self.csv_info["num_laps"]))
                self.info_label_temp.setText("Avg Temp: " + str(self.csv_info["avg_temperature"]) + "ºC")
                self.info_label_elevation.setText("Elevation change: " + str(self.csv_info["altitude_diff"]) + "m")


                # Read the CSV file and create a pandas DataFrame.
                self.df = pd.read_csv('LOG.CSV',
                                      names=['CurrentTime', 'satellites', 'speed', 'latitude', 'longitude', 'x', 'y',
                                             'z', 'temperature', 'altitude', 'currentLap'])
                # Convert the CurrentTime column to a datetime object
                self.df['CurrentTime'] = pd.to_datetime(self.df['CurrentTime'], format='%H:%M:%S')

                
            else:
                dlg = QMessageBox.warning(self, "Error", "Selected csv file is not valid!")

    def is_valid_csv_file(self, filename, num_columns):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != num_columns:
                    return False
            return True

    def extract_csv_info(self, filename, num_columns):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            rows = [row for row in reader if len(row) == num_columns]
            if not rows:
                return None

            start_time = datetime.strptime(rows[0][0], '%H:%M:%S').strftime('%H:%M:%S')
            stop_time = datetime.strptime(rows[-1][0], '%H:%M:%S').strftime('%H:%M:%S')
            elapse_time = datetime.strptime(stop_time, '%H:%M:%S') - datetime.strptime(start_time, '%H:%M:%S')
            elapse_time_str = str(elapse_time).split('.')[0]

            laps = [int(row[-1]) for row in rows]
            num_laps = laps[-1]

            satellites = [int(row[1]) for row in rows]
            avg_satellites = round(sum(satellites) / len(satellites), 2)

            speeds = [float(row[2]) * 1.852 for row in rows]  # Convert knots to km/h
            avg_speed = round(sum(speeds) / len(speeds), 2)

            temperatures = [float(row[8]) for row in rows]
            avg_temperature = round(sum(temperatures) / len(temperatures), 2)

            altitudes = [float(row[9]) for row in rows]
            max_altitude = max(altitudes)
            min_altitude = min(altitudes)
            altitude_diff = round(max_altitude - min_altitude, 2)

            return {
                'start_time': start_time,
                'stop_time': stop_time,
                'elapsed_time': elapse_time_str,
                'num_laps': num_laps,
                'avg_satellites': avg_satellites,
                'avg_speed': avg_speed,
                'avg_temperature': avg_temperature,
                'max_altitude': max_altitude,
                'min_altitude': min_altitude,
                'altitude_diff': altitude_diff
            }


    def racingLineMap_plot(self):
        pass

    def circuitElevation_plot(self):
        self.racingLineMap_button.setEnabled(True)

    def speed_plot(self):
        pass

    def accelerometer_plot(self):
        pass

    def temperature_plot(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
