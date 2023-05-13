import sys
import pandas as pd
import csv
from datetime import datetime, timedelta
from fontTools.merge import first
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
    QFileDialog, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
from numpy import number


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(650, 800)
        self.csv_file_name = None
        self.selected_lap = 0

        # GUI
        self.setWindowTitle("UPV Eco-Marathon Telemetry App")

        # logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap('logo_equipo.png')
        pixmap = pixmap.scaled(650, 800, Qt.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        # open csv file
        self.open_csv_title = QLabel('Open CSV file')
        self.csv_file_name_label = QLabel('. . .')
        self.csv_button = QPushButton("Open...")
        self.csv_button.clicked.connect(self.open_csv_file)

        # csv file info
        self.info_label_title = QLabel('Session info')
        
        self.info_label_sessionTime = QLabel('Session time: ')
        self.info_label_sessionTime.setEnabled(False)
        
        self.info_label_gpsSats = QLabel('Avg GPS Satellites: ')
        self.info_label_gpsSats.setEnabled(False)
        
        self.info_label_laps = QLabel('Laps: ')
        self.info_label_laps.setEnabled(False)
        
        self.info_label_speed = QLabel('Speed: ')
        self.info_label_speed.setEnabled(False)
        
        self.info_label_temp = QLabel('Avg temp: ')
        self.info_label_temp.setEnabled(False)
        
        self.info_label_elevation = QLabel('Elevation change: ')
        self.info_label_elevation.setEnabled(False)
        
        self.cbLaps = QComboBox()
        self.cbLaps.addItems(["Lap 0"])
        self.cbLaps.currentIndexChanged.connect(self.update_lap_selected)
        self.cbLaps.setEnabled(False)

        # buttons
        self.buttons_title_label = QLabel('Graph Options')
        
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
        
        self.info_label_lapTime = QLabel("Laptime: ")
        self.info_label_lapTime.setEnabled(False)
        
        self.info_label_speed_per_lap = QLabel("Avg Speed: ")
        self.info_label_speed_per_lap.setEnabled(False)
        
        self.info_label_temp_per_lap = QLabel("Avg temp: ")
        self.info_label_temp_per_lap.setEnabled(False)

        # layouts
        main_v_layout = QVBoxLayout()
        logo_h_layout = QHBoxLayout()
        csvTitle_h_layout = QHBoxLayout()
        first_h_layout = QHBoxLayout()
        second_h_layout = QHBoxLayout()
        infoTitle_h_layout = QHBoxLayout()
        info_v_layout_left = QVBoxLayout()
        info_v_layout_right = QVBoxLayout()
        buttonTtile_h_layout = QHBoxLayout()
        button_h_layout_one = QHBoxLayout()
        button_h_layout_two = QHBoxLayout()
        button_h_layout_three = QHBoxLayout()

        main_v_layout.addLayout(logo_h_layout)
        main_v_layout.addLayout(csvTitle_h_layout)
        main_v_layout.addLayout(first_h_layout)
        main_v_layout.addLayout(infoTitle_h_layout)
        main_v_layout.addLayout(second_h_layout)
        main_v_layout.addLayout(buttonTtile_h_layout)
        main_v_layout.addLayout(button_h_layout_one)
        main_v_layout.addLayout(button_h_layout_two)
        main_v_layout.addLayout(button_h_layout_three)
        
        logo_h_layout.addWidget(self.logo_label)
        
        csvTitle_h_layout.addWidget(self.open_csv_title)
        csvTitle_h_layout.setContentsMargins(30, 30, 1, 1)

        first_h_layout.addWidget(self.csv_file_name_label)
        first_h_layout.addWidget(self.csv_button)
        first_h_layout.setContentsMargins(100, 10, 110, 50)
        
        infoTitle_h_layout.addWidget(self.info_label_title)
        infoTitle_h_layout.setContentsMargins(30, 1, 1, 1)
        
        second_h_layout.addLayout(info_v_layout_left)
        second_h_layout.addLayout(info_v_layout_right)
        second_h_layout.setContentsMargins(70, 10, 70, 50)
        
        info_v_layout_left.addWidget(self.info_label_sessionTime)
        info_v_layout_left.addWidget(self.info_label_gpsSats)
        info_v_layout_left.addWidget(self.info_label_laps)
        info_v_layout_left.addWidget(self.info_label_speed)
        info_v_layout_left.addWidget(self.info_label_temp)
        info_v_layout_left.addWidget(self.info_label_elevation)
        
        info_v_layout_right.addWidget(self.cbLaps)
        info_v_layout_right.addWidget(self.info_label_lapTime)
        info_v_layout_right.addWidget(self.info_label_speed_per_lap)
        info_v_layout_right.addWidget(self.info_label_temp_per_lap)
        info_v_layout_right.setContentsMargins(50, 0, 40, 0)

        buttonTtile_h_layout.addWidget(self.buttons_title_label)
        buttonTtile_h_layout.setContentsMargins(30, 1, 1, 1)
        
        button_h_layout_one.addWidget(self.racingLineMap_button)
        button_h_layout_one.addWidget(self.circuitElevation_button)
        button_h_layout_one.setContentsMargins(90, 15, 110, 5)

        button_h_layout_two.addWidget(self.speed_button)
        button_h_layout_two.addWidget(self.accelerometer_button)
        button_h_layout_two.setContentsMargins(90, 1, 110, 5)

        button_h_layout_three.addWidget(self.temperature_button)
        button_h_layout_three.setContentsMargins(90, 1, 110, 50)

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
                self.csv_file_name_label.setText(self.csv_file_name)
                self.csv_file_name_label.setFont(QFont('Arial', 7))
                
                # extract info from csv file
                self.csv_info = self.extract_csv_info(self.csv_file_name, 11)
                
                # update info section
                self.info_label_sessionTime.setText("Session time: "+self.csv_info["elapsed_time"])
                self.info_label_sessionTime.setEnabled(True)
                
                self.info_label_gpsSats.setText("Avg GPS Satellites: " + str(self.csv_info["avg_satellites"]))
                self.info_label_gpsSats.setEnabled(True)
                
                self.info_label_laps.setText("Laps: " + str(self.csv_info["num_laps"]))
                self.info_label_laps.setEnabled(True)
                
                self.info_label_speed.setText("Avg Speed: " + str(self.csv_info["avg_speed"]) + "km/h")
                self.info_label_speed.setEnabled(True)
                
                self.info_label_temp.setText("Avg Temp: " + str(self.csv_info["avg_temperature"]) + " ºC")
                self.info_label_temp.setEnabled(True)
                
                self.info_label_elevation.setText("Elevation change: " + str(self.csv_info["altitude_diff"]) + " meters")
                self.info_label_elevation.setEnabled(True)
                
                self.populate_CB_laps(self.csv_info["num_laps"])
                self.cbLaps.setEnabled(True)

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


    def update_lap_selected(self, index):
        selected_lap = index
        #ignore '-1'
        #update the right-part info depending on the lap selected
        print("-->"+str(selected_lap))
        
    def populate_CB_laps(self, total_laps):
        self.cbLaps.clear()
        
        for i in range(total_laps + 1):
            self.cbLaps.addItem('Lap {}'.format(i))
            

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
    app.setStyleSheet("QLabel{font-size: 11pt;} QPushButton{font-size: 10pt;} QComboBox{font-size: 10pt;}")
    #app.setStyleSheet("QPushButton{font-size: 10pt;}")

    w = MainWindow()
    w.show()
    app.exec()
