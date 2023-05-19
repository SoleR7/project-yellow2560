import sys
import datetime
from PyQt5 import QtCore
import pandas as pd
import numpy as np
import csv
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
    QFileDialog, QMessageBox, QComboBox
from PyQt5.QtCore import Qt


class drawCircuitWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        app = Tk()
        app.title("Circuit draw")
        app.geometry("850x500")
        app.resizable(False, False)


        def get_x_and_y(event):
            global lasx, lasy
            lasx, lasy = event.x, event.y

        def draw_smth(event):
            global lasx, lasy
            canvas.create_line((lasx, lasy, event.x, event.y), fill='red', width=3)
            lasx, lasy = event.x, event.y
            

        canvas = Canvas(app, bg='black')
        canvas.pack(anchor='nw', fill='both', expand=1)

        canvas.bind("<Button-1>", get_x_and_y)
        canvas.bind("<B1-Motion>", draw_smth)


        image = Image.open("nogaro_layout.png")
        image = image.resize((850,500), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        canvas.create_image(0,0, image=image, anchor='nw')
        
        app.mainloop()
    
    

class accelerometerGraph(QWidget):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Accelerometer Graph")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Plot the temperature data on the figure
        ax = self.figure.add_subplot(111)
        ax.plot(df['CurrentTime'].values, df['x'].values, label='X')
        ax.plot(df['CurrentTime'].values, df['y'].values, label='Y')
        ax.plot(df['CurrentTime'].values, df['z'].values, label='Z')
        ax.set_title('Accelerometer Readings over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Acceleration (m/s^2)')
        ax.legend()


        # Create a navigation toolbar and add it to the layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class combinedPlot3(QWidget):
    def __init__(self, dfA):
        super().__init__()
        self.setWindowTitle("Combined Temperature, Speed, and Accelerometer Graph")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Plot the temperature and speed data on the figure
        ax1 = self.figure.add_subplot(211)
        ax1.plot(dfA.index, dfA['temperature'], label="A temperature", color='#F5680D')
        ax1.plot(dfA.index, dfA['speed'].values * 1.852, label="A speed", color='#D016F5')
        ax1.set_title('Temperature and Speed')
        ax1.set_ylabel('Value')
        ax1.legend()
        ax1.set_xticks([])
        ax1.set_xticklabels([])

        # Adjust the Y-axis divisions and precision for temperature and speed plot
        ax1.yaxis.set_ticks(np.linspace(ax1.get_yticks()[0], ax1.get_yticks()[-1], 20))
        ax1.yaxis.set_major_formatter('{x:.1f}')

        # Plot the XYZ readings on the figure
        ax2 = self.figure.add_subplot(212)
        ax2.plot(dfA.index, dfA['x'], label='A X', color='#F80606')
        ax2.plot(dfA.index, dfA['y'], label='A Y', color='#1017F1')
        ax2.plot(dfA.index, dfA['z'], label='A Z', color='#6BF50C')
        ax2.set_title('Accelerometer Readings')
        ax2.set_ylabel('Acceleration (m/s^2)')
        ax2.legend()
        ax2.set_xticks([])
        ax2.set_xticklabels([])

        # Create a navigation toolbar and add it to the layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)




class combinedPlot2(QWidget):
    def __init__(self, dfA, dfB):
        super().__init__()
        self.setWindowTitle("Combined Temperature, Speed, and Accelerometer Graph")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Combine the temperature and speed data from both dataframes
        temperatures = pd.concat([dfA['temperature'], dfB['temperature']], axis=0)
        speeds = pd.concat([dfA['speed'], dfB['speed']], axis=0)

        # Create a common x-axis range based on the length of the longest dataframe
        max_length = max(len(dfA), len(dfB))
        x_temps_speeds = np.arange(max_length)
        x_xyz = np.arange(max_length)

        # Plot the temperature and speed data on the figure
        ax1 = self.figure.add_subplot(211)
        ax1.plot(x_temps_speeds[:len(dfA)], dfA['temperature'], label="A temperature", color='#F5680D')
        ax1.plot(x_temps_speeds[:len(dfB)], dfB['temperature'], label="B temperature", color='#F3BD99')
        ax1.plot(x_temps_speeds[:len(dfA)], dfA['speed'].values * 1.852, label="A speed", color='#D016F5')
        ax1.plot(x_temps_speeds[:len(dfB)], dfB['speed'].values * 1.852, label="B speed", color='#EAB0F5')
        ax1.set_title('Temperature and Speed')
        ax1.set_ylabel('Value')
        ax1.legend()

        ax1.set_xticks([])
        ax1.set_xticklabels([])

        # Adjust the Y-axis divisions and precision for temperature and speed plot
        ax1.yaxis.set_ticks(np.linspace(ax1.get_yticks()[0], ax1.get_yticks()[-1], 20))
        ax1.yaxis.set_major_formatter('{x:.1f}')
        

        # Plot the XYZ readings on the figure
        ax2 = self.figure.add_subplot(212)
        ax2.plot(x_xyz[:len(dfA)], dfA['x'], label='A X', color='#F80606')
        ax2.plot(x_xyz[:len(dfA)], dfA['y'], label='A Y', color='#1017F1')
        ax2.plot(x_xyz[:len(dfA)], dfA['z'], label='A Z', color='#6BF50C')
        ax2.plot(x_xyz[:len(dfB)], dfB['x'], label='B X', color='#FB9090')
        ax2.plot(x_xyz[:len(dfB)], dfB['y'], label='B Y', color='#9598F3')
        ax2.plot(x_xyz[:len(dfB)], dfB['z'], label='B Z', color='#C1F39E')
        ax2.set_title('Accelerometer Readings')
        ax2.set_ylabel('Acceleration (m/s^2)')
        ax2.legend()
        
        ax2.set_xticks([])
        ax2.set_xticklabels([])

        # Create a navigation toolbar and add it to the layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    

    


class combinedPlot(QWidget):
    def __init__(self, dfA, dfB):
        super().__init__()
        self.setWindowTitle("Temperature and Speed Graph A vs B")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Combine the temperature and speed data from both dataframes
        temperatures = pd.concat([dfA['temperature'], dfB['temperature']], axis=0)

        # Create a common x-axis range based on the length of the longest dataframe
        x = np.arange(len(temperatures))

        # Plot the temperature and speed data on the figure
        ax = self.figure.add_subplot(111)
        ax.plot(x[:len(dfA)], dfA['temperature'], label="A temperature")
        ax.plot(x[:len(dfB)], dfB['temperature'], label="B temperature")
        ax.plot(x[:len(dfA)], dfA['speed'].values * 1.852, label="A speed")
        ax.plot(x[:len(dfB)], dfB['speed'].values * 1.852, label="B speed")
        ax.set_title('Temperature and Speed over Time')
        #ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.legend()

        # Adjust the Y-axis divisions and precision
        ax.yaxis.set_ticks(np.linspace(ax.get_yticks()[0], ax.get_yticks()[-1], 20))
        ax.yaxis.set_major_formatter('{x:.1f}')
        
        ax.set_xticks([])
        ax.set_xticklabels([])

        # Create a navigation toolbar and add it to the layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class temperatureGraph2(QWidget):
    def __init__(self, dfA, dfB):
        super().__init__()
        self.setWindowTitle("Temperature Graph A vs B")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Combine the temperature data from both dataframes
        temperatures = pd.concat([dfA['temperature'], dfB['temperature']], axis=0)

        # Create a common x-axis range based on the length of the longest dataframe
        x = np.arange(len(temperatures))

        # Plot the temperature data on the figure
        ax = self.figure.add_subplot(111)
        ax.plot(x[:len(dfA)], dfA['temperature'], label="A temp")
        ax.plot(x[:len(dfB)], dfB['temperature'], label="B temp")
        ax.set_title('Temperature over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature (ºC)')
        ax.legend()
        
        ax.set_xticks([])
        ax.set_xticklabels([])

        # Create a navigation toolbar and add it to the layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class temperatureGraph(QWidget):
    def __init__(self, dfA, dfB):
        super().__init__()
        self.setWindowTitle("Temperature Graph A vs B")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Plot the temperature data on the figure
        ax = self.figure.add_subplot(111)
        ax.plot(dfA['CurrentTime'].values, dfA['temperature'].values, label="A")
        ax.plot(dfB['CurrentTime'].values, dfB['temperature'].values, label="B")
        ax.set_title('Temperature over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature ºC')

        # Create a navigation toolbar and add it to the layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class speedGraph2(QWidget):
    def __init__(self, dfA, dfB):
        super().__init__()
        self.setWindowTitle("Speed Graph A vs B")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Combine the temperature data from both dataframes
        speeds = pd.concat([dfA['speed'], dfB['speed']], axis=0)

        # Create a common x-axis range based on the length of the longest dataframe
        x = np.arange(len(speeds))

        # Plot the temperature data on the figure
        ax = self.figure.add_subplot(111)
        ax.plot(x[:len(dfA)], dfA['speed'].values * 1.852, label="A speed")
        ax.plot(x[:len(dfB)], dfB['speed'].values * 1.852, label="B speed")
        ax.set_title('Speed over Time')
        #ax.set_xlabel('Time')
        ax.set_ylabel('Speed (km/h)')
        ax.legend()
        
        
        ax.set_xticks([])
        ax.set_xticklabels([])

        # Create a navigation toolbar and add it to the layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class speedGraph(QWidget):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Speed Graph")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Plot the temperature data on the figure
        ax = self.figure.add_subplot(111)
        ax.plot(df['CurrentTime'].values, df['speed'].values * 1.852)
        ax.set_title('Speed over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Speed km/h')

        # Create a navigation toolbar and add it to the layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        

class circuitElevationGraph(QWidget):
    def __init__(self, df):
        super().__init__()

        self.setWindowTitle("Elevation Analysis")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Plot the latitude and longitude data on a scatter plot
        ax = self.figure.add_subplot(111)
        scatter = ax.scatter(df['longitude'].values, df['latitude'].values, c=df['altitude'].values, cmap='viridis')
        cbar = self.figure.colorbar(scatter)
        cbar.set_label('Altitude (meters)')

        # Connect each point by its next one with a line plot
        ax.plot(df['longitude'].values, df['latitude'].values, color='gray')

        # Remove X and Y axis ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Create a navigation toolbar and add it to the layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(650, 850)
        self.csv_file_name = None
        self.selected_lap = 0

        # GUI
        self.setWindowTitle("UPV Eco-Marathon Telemetry App")

        # logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap('logo_equipo.png')
        pixmap = pixmap.scaled(650, 850, Qt.KeepAspectRatio)
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
        
        self.info_label_lapTime = QLabel("Laptime: ")
        self.info_label_lapTime.setEnabled(False)
        
        self.info_label_speed_per_lap = QLabel("Avg Speed: ")
        self.info_label_speed_per_lap.setEnabled(False)
        
        self.info_label_temp_per_lap = QLabel("Avg temp: ")
        self.info_label_temp_per_lap.setEnabled(False)
        
        # buttons
        self.buttons_title_label = QLabel('Graphs\t\t (Whole session \ per lap)')
        
        #  whole session
        self.speed_button = QPushButton("Speed")
        self.speed_button.clicked.connect(self.speed_plot)
        self.speed_button.setEnabled(False)
        
        self.temperature_button = QPushButton("Temperature")
        self.temperature_button.clicked.connect(self.temperature_plot)
        self.temperature_button.setEnabled(False)
        
        self.accelerometer_button = QPushButton("Accelerometer")
        self.accelerometer_button.clicked.connect(self.accelerometer_plot)
        self.accelerometer_button.setEnabled(False)
        
        # per lap
        self.racingLineMap_button = QPushButton("Racing line")
        self.racingLineMap_button.clicked.connect(self.racingLineMap_plot)
        self.racingLineMap_button.setEnabled(False)

        self.circuitElevation_button = QPushButton("Elevation Analysis")
        self.circuitElevation_button.clicked.connect(self.circuitElevation_plot)
        self.circuitElevation_button.setEnabled(False)
        
        self.speed_perLap_button = QPushButton("Speed")
        self.speed_perLap_button.clicked.connect(self.speed_perLap_plot)
        self.speed_perLap_button.setEnabled(False)
        
        self.temp_perLap_button = QPushButton("Temperature")
        self.temp_perLap_button.clicked.connect(self.temp_perLap_plot)
        self.temp_perLap_button.setEnabled(False)
        
        self.accelerometer_perLap_button = QPushButton("Accelerometer")
        self.accelerometer_perLap_button.clicked.connect(self.accelerometer_perLap_plot)
        self.accelerometer_perLap_button.setEnabled(False)
        

        # layouts
        #(right, top, left, bottom)
        main_v_layout = QVBoxLayout()
        logo_h_layout = QHBoxLayout()
        csvTitle_h_layout = QHBoxLayout()
        first_h_layout = QHBoxLayout()
        second_h_layout = QHBoxLayout()
        infoTitle_h_layout = QHBoxLayout()
        info_v_layout_left = QVBoxLayout()
        info_v_layout_right = QVBoxLayout()
        buttonTtile_h_layout = QHBoxLayout()
        button_h_main_layout = QHBoxLayout()
        button_v_layout_left = QVBoxLayout()
        button_v_layout_right = QVBoxLayout()

        main_v_layout.addLayout(logo_h_layout)
        main_v_layout.addLayout(csvTitle_h_layout)
        main_v_layout.addLayout(first_h_layout)
        main_v_layout.addLayout(infoTitle_h_layout)
        main_v_layout.addLayout(second_h_layout)
        main_v_layout.addLayout(buttonTtile_h_layout)
        main_v_layout.addLayout(button_h_main_layout)
        
        logo_h_layout.addWidget(self.logo_label)
        
        csvTitle_h_layout.addWidget(self.open_csv_title)
        csvTitle_h_layout.setContentsMargins(30, 10, 1, 1)

        first_h_layout.addWidget(self.csv_file_name_label)
        first_h_layout.addWidget(self.csv_button)
        first_h_layout.setContentsMargins(100, 1, 110, 1)
        
        infoTitle_h_layout.addWidget(self.info_label_title)
        infoTitle_h_layout.setContentsMargins(30, 1, 1, 1)
        
        second_h_layout.addLayout(info_v_layout_left)
        second_h_layout.addLayout(info_v_layout_right)
        second_h_layout.setContentsMargins(70, 10, 70, 20)
        
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
        info_v_layout_right.setContentsMargins(50, 0, 0, 0)

        buttonTtile_h_layout.addWidget(self.buttons_title_label)
        buttonTtile_h_layout.setContentsMargins(30, 1, 1, 1)
        
        button_h_main_layout.addLayout(button_v_layout_left)
        button_h_main_layout.addLayout(button_v_layout_right)
        button_h_main_layout.setContentsMargins(70, 15, 70, 5)
        
        button_v_layout_left.addWidget(self.speed_button)
        button_v_layout_left.addWidget(self.accelerometer_button)
        button_v_layout_left.addWidget(self.temperature_button)
        button_v_layout_left.setAlignment(Qt.AlignTop)
        
        button_v_layout_right.addWidget(self.racingLineMap_button)
        button_v_layout_right.addWidget(self.circuitElevation_button)
        button_v_layout_right.addWidget(self.speed_perLap_button)
        button_v_layout_right.addWidget(self.accelerometer_perLap_button)
        button_v_layout_right.addWidget(self.temp_perLap_button)
        button_v_layout_right.setAlignment(Qt.AlignTop)

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

            # check if the file is valid
            if self.is_valid_csv_file(self.csv_file_name, 11):
                self.csv_file_name_label.setText(self.csv_file_name)
                self.csv_file_name_label.setFont(QFont('Arial', 7))
                
                # extract info from csv file
                self.csv_info = self.extract_csv_info(self.csv_file_name, 11)
                
                # Read the CSV file and create a pandas DataFrame.
                self.df = pd.read_csv(self.csv_file_name,
                                      names=['CurrentTime', 'satellites', 'speed', 'latitude', 'longitude', 'x', 'y',
                                             'z', 'temperature', 'altitude', 'currentLap'])
                
                # Convert the CurrentTime column to a datetime object
                self.df['CurrentTime'] = pd.to_datetime(self.df['CurrentTime'], format='%H:%M:%S')
                
                # update info section
                self.info_label_sessionTime.setText("Session time: "+self.csv_info["elapsed_time"])
                self.info_label_sessionTime.setEnabled(True)
                
                self.info_label_gpsSats.setText("Avg GPS Satellites: " + str(self.csv_info["avg_satellites"]))
                self.info_label_gpsSats.setEnabled(True)
                
                self.info_label_laps.setText("Laps: " + str(self.csv_info["num_laps"]))
                self.info_label_laps.setEnabled(True)
                
                self.info_label_speed.setText("Avg Speed: " + str(self.csv_info["avg_speed"]) + " km/h")
                self.info_label_speed.setEnabled(True)
                
                self.info_label_temp.setText("Avg Temp: " + str(self.csv_info["avg_temperature"]) + " ºC")
                self.info_label_temp.setEnabled(True)
                
                self.info_label_elevation.setText("Elevation change: " + str(self.csv_info["altitude_diff"]) + " meters")
                self.info_label_elevation.setEnabled(True)
                
                self.populate_CB_laps(self.csv_info["num_laps"])
                self.cbLaps.setEnabled(True)
                
                # extract info from lap 0
                self.extract_csv_info_perLap(self.selected_lap, self.df)
 
                #activate buttons
                self.speed_button.setEnabled(True)
                self.temperature_button.setEnabled(True)
                self.accelerometer_button.setEnabled(True)
                self.racingLineMap_button.setEnabled(True)
                self.circuitElevation_button.setEnabled(True)
                self.speed_perLap_button.setEnabled(True)
                self.accelerometer_perLap_button.setEnabled(True)
                self.temp_perLap_button.setEnabled(True)
                
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


    def populate_CB_laps(self, total_laps):
        self.cbLaps.clear()
        
        for i in range(total_laps + 1):
            self.cbLaps.addItem('Lap {}'.format(i))


    def update_lap_selected(self, index):
        self.selected_lap = index
        
        if self.selected_lap >= 0:
            #print("->"+str(self.selected_lap))
            currentLap_df = self.extract_csv_info_perLap(self.selected_lap, self.df)
            
            currentLap_avg_speed = round(currentLap_df['speed'].mean() * 1.852, 2)
            currentLap_avg_temp= round(currentLap_df['temperature'].mean(), 2)
            
            lap_time = currentLap_df.iloc[-1]['CurrentTime'] - currentLap_df.iloc[0]['CurrentTime']
            lap_time_seconds = lap_time.total_seconds()
            lap_time_str = '{:02d}:{:02d}:{:02d}'.format(int(lap_time_seconds // 3600), int(lap_time_seconds % 3600 // 60), int(lap_time_seconds % 60))

            self.info_label_lapTime.setText("LapTime: " + lap_time_str)
            self.info_label_lapTime.setEnabled(True)
            self.info_label_speed_per_lap.setText("Avg Speed: " + str(currentLap_avg_speed) + " km/h")
            self.info_label_speed_per_lap.setEnabled(True)
            self.info_label_temp_per_lap.setText("Avg Temp: " + str(currentLap_avg_temp) + " ºC")
            self.info_label_temp_per_lap.setEnabled(True)
        
            
    def extract_csv_info_perLap(self, lap_selected, dataFrame):
        df_currentLap = dataFrame.loc[dataFrame['currentLap'] == lap_selected]
        return df_currentLap
    

    def speed_plot(self):
        #self.speed_GraphWindow = speedGraph2(self.extract_csv_info_perLap(2, self.df), self.extract_csv_info_perLap(4, self.df))
        #self.speed_GraphWindow.show()
        self.combined_GraphWindow = combinedPlot2(self.extract_csv_info_perLap(2, self.df), self.extract_csv_info_perLap(4, self.df))
        self.combined_GraphWindow.show()
        #self.combined_GraphWindow = combinedPlot3(self.df)
        #self.combined_GraphWindow.show()
        

    def accelerometer_plot(self):
        self.accelerometer_GraphWindow = accelerometerGraph(self.df)
        self.accelerometer_GraphWindow.show()


    def temperature_plot(self):
        self.temperature_GraphWindow = temperatureGraph2(self.extract_csv_info_perLap(1, self.df), self.extract_csv_info_perLap(2, self.df))
        self.temperature_GraphWindow.show()

    def racingLineMap_plot(self):
        #open image?
        self.drawOnCircuitWindow = drawCircuitWindow()

    def circuitElevation_plot(self):
        self.circuitElevation_GraphWindow = circuitElevationGraph(self.extract_csv_info_perLap(self.selected_lap, self.df))
        self.circuitElevation_GraphWindow.show()
    
    def speed_perLap_plot(self):
        self.speedPerLap_GraphWindow = speedGraph(self.extract_csv_info_perLap(self.selected_lap, self.df))
        self.speedPerLap_GraphWindow.show()

    def accelerometer_perLap_plot(self):
        self.accelerometerPerLap_GraphWindow = accelerometerGraph(self.extract_csv_info_perLap(self.selected_lap, self.df))
        self.accelerometerPerLap_GraphWindow.show()
    
    def temp_perLap_plot(self):
        self.temperaturePerLap_GraphWindow = temperatureGraph(self.extract_csv_info_perLap(self.selected_lap, self.df))
        self.temperaturePerLap_GraphWindow.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet("QLabel{font-size: 11pt;} QPushButton{font-size: 10pt;} QComboBox{font-size: 10pt;}")
    app.setStyleSheet("QLabel{font-size: 9pt;} QPushButton{font-size: 9pt;} QComboBox{font-size: 9pt;}")
    w = MainWindow()
    w.show()
    app.exec()
