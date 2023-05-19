import sys
import datetime
from PyQt5 import QtCore
import pandas as pd
import numpy as np
import csv
import folium
import io
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
    QFileDialog, QMessageBox, QComboBox, QCheckBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
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
    

class sessionTelemetryGraph(QWidget):
    def __init__(self, df, speed_activated, acc_activated, temp_activated):
        super().__init__()
        self.setWindowTitle("Session telemetry")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        if not acc_activated and (speed_activated or temp_activated):
            ax1 = self.figure.add_subplot(111)
        elif acc_activated and (speed_activated or temp_activated):
            ax1 = self.figure.add_subplot(211)
            ax2 = self.figure.add_subplot(212)
        elif acc_activated and not speed_activated and not temp_activated:
            ax2 = self.figure.add_subplot(111)
        
        if speed_activated:
            ax1.plot(df.index, df['speed'].values * 1.852, label="Speed (km/h)", color='#D016F5')
        
        if temp_activated:
            ax1.plot(df.index, df['temperature'], label="Temperature (ºC)", color='#F5680D')
        
        if speed_activated or temp_activated:
            ax1.legend()
            ax1.set_xticks([])
            ax1.set_xticklabels([])

        if speed_activated and temp_activated:
            # Adjust the Y-axis divisions and precision for temperature and speed plot
            ax1.yaxis.set_ticks(np.linspace(ax1.get_yticks()[0], ax1.get_yticks()[-1], 20))
            ax1.yaxis.set_major_formatter('{x:.1f}')
            

        # Plot the XYZ readings on the figure
        if acc_activated:
            ax2.plot(df.index, df['x'], label='X', color='#F80606')
            ax2.plot(df.index, df['y'], label='Y', color='#1017F1')
            ax2.plot(df.index, df['z'], label='Z', color='#6BF50C')
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


class sessionGPS_MapGraph(QWidget):
    def __init__(self, csv_file_name, individualLap=False, lapNumber=0):
        super().__init__()
        self.setWindowTitle('GPS Data')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        trail_coordinates = self.obtainGPScoordinates(csv_file_name, individualLap, lapNumber)

        coordinate = (trail_coordinates[0][0], trail_coordinates[0][1])
        m = folium.Map(
            tiles='OpenStreetMap',
            zoom_start=17,
            max_zoom=23,
            control_scale=True,
            location=coordinate
        )

        folium.PolyLine(trail_coordinates, tooltip="Coast").add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)
    
    
    def obtainGPScoordinates(self, csv_file_name, individualLap=False, lapNumber=0):
        df = pd.read_csv(csv_file_name, names=['CurrentTime', 'satellites', 'speed', 'latitude', 'longitude', 'x', 'y', 'z', 'temperature', 'altitude', 'currentLap'])
        if individualLap:
            df = df.loc[df['currentLap'] == lapNumber]
        
        coords = list(zip(df['latitude'], df['longitude']))
        return coords


class lapComparationTelemetryGraph(QWidget):
        def __init__(self, dfA, speed_activated, acc_activated, temp_activated, dfB=None):
            super().__init__()
            if dfB is None:
                self.setWindowTitle("Lap A telemetry")
                # Create a figure and a canvas to draw the plot on
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)

                if not acc_activated and (speed_activated or temp_activated):
                    ax1 = self.figure.add_subplot(111)
                elif acc_activated and (speed_activated or temp_activated):
                    ax1 = self.figure.add_subplot(211)
                    ax2 = self.figure.add_subplot(212)
                elif acc_activated and not speed_activated and not temp_activated:
                    ax2 = self.figure.add_subplot(111)
                    
                
                if speed_activated:
                    ax1.plot(dfA.index, dfA['speed'].values * 1.852, label="Speed (km/h)", color='#D016F5')
                
                if temp_activated:
                    ax1.plot(dfA.index, dfA['temperature'], label="Temperature (ºC)", color='#F5680D')
                
                if speed_activated or temp_activated:
                    ax1.legend()
                    ax1.set_xticks([])
                    ax1.set_xticklabels([])

                if speed_activated and temp_activated:
                    # Adjust the Y-axis divisions and precision for temperature and speed plot
                    ax1.yaxis.set_ticks(np.linspace(ax1.get_yticks()[0], ax1.get_yticks()[-1], 20))
                    ax1.yaxis.set_major_formatter('{x:.1f}')
                
                
               # Plot the XYZ readings on the figure
                if acc_activated:
                    ax2.plot(dfA.index, dfA['x'], label='X', color='#F80606')
                    ax2.plot(dfA.index, dfA['y'], label='Y', color='#1017F1')
                    ax2.plot(dfA.index, dfA['z'], label='Z', color='#6BF50C')
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

                
            else:
                self.setWindowTitle("Lap A vs B telemetry analysis")

                # Create a figure and a canvas to draw the plot on
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)

                
                if not acc_activated and (speed_activated or temp_activated):
                    ax1 = self.figure.add_subplot(111)
                elif acc_activated and (speed_activated or temp_activated):
                    ax1 = self.figure.add_subplot(211)
                    ax2 = self.figure.add_subplot(212)
                elif acc_activated and not speed_activated and not temp_activated:
                    ax2 = self.figure.add_subplot(111)
                
                if speed_activated and temp_activated:
                    # Combine the temperature and speed data from both dataframes
                    temperatures = pd.concat([dfA['temperature'], dfB['temperature']], axis=0)
                    speeds = pd.concat([dfA['speed'], dfB['speed']], axis=0)

                if speed_activated or temp_activated:
                    # Create a common x-axis range based on the length of the longest dataframe
                    max_length = max(len(dfA), len(dfB))
                    x_temps_speeds = np.arange(max_length)
                    
                if acc_activated:
                    max_length = max(len(dfA), len(dfB))
                    x_xyz = np.arange(max_length)

                if temp_activated:
                    ax1.plot(x_temps_speeds[:len(dfA)], dfA['temperature'], label="A Air temperature", color='#F5680D')
                    ax1.plot(x_temps_speeds[:len(dfB)], dfB['temperature'], label="B Air temperature", color='#F3BD99')
                
                if speed_activated:
                    ax1.plot(x_temps_speeds[:len(dfA)], dfA['speed'].values * 1.852, label="A speed", color='#D016F5')
                    ax1.plot(x_temps_speeds[:len(dfB)], dfB['speed'].values * 1.852, label="B speed", color='#EAB0F5')

                if temp_activated or speed_activated:
                    ax1.set_ylabel('Value')
                    ax1.legend()
                    ax1.set_xticks([])
                    ax1.set_xticklabels([])

                    # Adjust the Y-axis divisions and precision for temperature and speed plot
                    ax1.yaxis.set_ticks(np.linspace(ax1.get_yticks()[0], ax1.get_yticks()[-1], 20))
                    ax1.yaxis.set_major_formatter('{x:.1f}')
                
                if acc_activated:
                    ax2.plot(x_xyz[:len(dfA)], dfA['x'], label='A X', color='#F80606')
                    ax2.plot(x_xyz[:len(dfA)], dfA['y'], label='A Y', color='#1017F1')
                    ax2.plot(x_xyz[:len(dfA)], dfA['z'], label='A Z', color='#6BF50C')
                    ax2.plot(x_xyz[:len(dfB)], dfB['x'], label='B X', color='#FB9090')
                    ax2.plot(x_xyz[:len(dfB)], dfB['y'], label='B Y', color='#9598F3')
                    ax2.plot(x_xyz[:len(dfB)], dfB['z'], label='B Z', color='#C1F39E')
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


class temperatureGraph(QWidget):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Temperature Graph")

        # Create a figure and a canvas to draw the plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Plot the temperature data on the figure
        ax = self.figure.add_subplot(111)
        ax.plot(df['CurrentTime'].values, df['temperature'].values)
        ax.set_title('Temperature over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature ºC')

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
        self.setFixedSize(850, 1020)
        self.csv_file_name = None
        self.selected_lapA = 0
        self.selected_lapB = 0
        self.lapB_selected = False
        self.sessionGraph_speed_selected = False
        self.sessionGraph_acc_selected = False
        self.sessionGraph_temp_selected = False
        self.lapComparationGraph_speed_selected = False
        self.lapComparationGraph_acc_selected = False
        self.lapComparationGraph_temp_selected = False
        
        
        
        font_bold = QFont()
        font_bold.setBold(True)
        

        # GUI
        self.setWindowTitle("UPV Eco-Marathon Telemetry App")

        # logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap('logo_equipo.png')
        pixmap = pixmap.scaled(850, 1020, Qt.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        # open csv file
        self.open_csv_title = QLabel('Open CSV file')
        self.open_csv_title.setFont(font_bold)
        self.csv_file_name_label = QLabel('. . .')
        self.csv_button = QPushButton("Open...")
        self.csv_button.clicked.connect(self.open_csv_file)

        # csv file info
        self.session_info_labelTitle = QLabel('Session info')
        self.session_info_labelTitle.setFont(font_bold)
        self.info_label_sessionTime = QLabel('Session time: ')
        self.info_label_sessionTime.setEnabled(False)
        self.info_label_gpsSats = QLabel('Avg GPS Satellites: ')
        self.info_label_gpsSats.setEnabled(False)
        self.info_label_laps = QLabel('Laps: ')
        self.info_label_laps.setEnabled(False)
        self.info_label_speed = QLabel('Speed: ')
        self.info_label_speed.setEnabled(False)
        self.info_label_temp = QLabel('Avg Air Temp: ')
        self.info_label_temp.setEnabled(False)
        self.info_label_elevation = QLabel('Elevation change: ')
        self.info_label_elevation.setEnabled(False)
        
        self.drawCircuitButton = QPushButton("Circuit strategy sketch")
        self.drawCircuitButton.clicked.connect(self.show_CircuitSketch)
        
        
        # Session graphs
        self.session_graphs_labelTitle = QLabel('Session Graphs')
        self.session_graphs_labelTitle.setFont(font_bold)
        self.checkBox_SessionGraphs_speed = QCheckBox(text="Speed", parent=self)
        self.checkBox_SessionGraphs_speed.stateChanged.connect(self.checkBox_sessionGraph_speed_changed)
        self.checkBox_SessionGraphs_speed.setEnabled(False)
        self.checkBox_SessionGraphs_accelerometer = QCheckBox(text="Accelerometer", parent=self)
        self.checkBox_SessionGraphs_accelerometer.stateChanged.connect(self.checkBox_sessionGraph_accelerometer_changed)
        self.checkBox_SessionGraphs_accelerometer.setEnabled(False)
        self.checkBox_SessionGraphs_temp = QCheckBox(text="Temperature", parent=self)
        self.checkBox_SessionGraphs_temp.stateChanged.connect(self.checkBox_sessionGraph_temp_changed)
        self.checkBox_SessionGraphs_temp.setEnabled(False)
        self.plot_sesssionGraph_telemetry_button = QPushButton("Telemetry")
        self.plot_sesssionGraph_telemetry_button.clicked.connect(self.sessionGraph_telemetry_ShowPlot)
        self.plot_sesssionGraph_telemetry_button.setEnabled(False)
        self.plot_sesssionGraph_gpsData_button = QPushButton("GPS Data")
        self.plot_sesssionGraph_gpsData_button.clicked.connect(self.sessionGrap_gpsData_ShowPlot)
        self.plot_sesssionGraph_gpsData_button.setEnabled(False)
        
        # Lap comparation Graphs
        self.lap_comparation_graphs_labelTitle = QLabel('Lap Comparation Graphs')
        self.lap_comparation_graphs_labelTitle.setFont(font_bold)
        self.a_label = QLabel('A:')
        self.a_label.setEnabled(False)
        self.comboBox_A = QComboBox()
        self.comboBox_A.addItems(["Lap 0"])
        self.comboBox_A.currentIndexChanged.connect(self.update_lapSelected_A)
        self.comboBox_A.setEnabled(False)
        self.checkBox_LapComparation_speed =  QCheckBox(text="Speed", parent=self)
        self.checkBox_LapComparation_speed.stateChanged.connect(self.checkBox_lapComparation_speed_changed)
        self.checkBox_LapComparation_speed.setEnabled(False)
        self.checkBox_LapComparation_accelerometer =  QCheckBox(text="Acceleromter", parent=self)
        self.checkBox_LapComparation_accelerometer.stateChanged.connect(self.checkBox_lapComparation_accelerometer_changed)
        self.checkBox_LapComparation_accelerometer.setEnabled(False)
        self.checkBox_LapComparation_temp =  QCheckBox(text="Air Temp", parent=self)
        self.checkBox_LapComparation_temp.stateChanged.connect(self.checkBox_lapComparation_temp_changed)
        self.checkBox_LapComparation_temp.setEnabled(False)

        
        self.checkBox_B_lap = QCheckBox(parent=self)
        self.checkBox_B_lap.stateChanged.connect(self.checkBox_bLap_changed)
        self.checkBox_B_lap.setEnabled(False)
        self.b_label = QLabel('B: ')
        self.b_label.setEnabled(False)
        self.comboBox_B = QComboBox()
        self.comboBox_B.addItems(["Lap 0"])
        self.comboBox_B.currentIndexChanged.connect(self.update_lapSelected_B)
        self.comboBox_B.setEnabled(False)
        
        self.plot_lapComparation_telemetry_button = QPushButton('Telemetry')
        self.plot_lapComparation_telemetry_button.setEnabled(False)
        self.plot_lapComparation_telemetry_button.clicked.connect(self.lapComparation_telemetry_ShowPlot)
        self.plot_lapComparation_gpsData_button = QPushButton('GPS Data')
        self.plot_lapComparation_gpsData_button.setEnabled(False)
        self.plot_lapComparation_gpsData_button.clicked.connect(self.lapComparation_gpsData_ShowPlot)
        self.plot_lapComparation_elevationMap_button = QPushButton('Elevation Map')
        self.plot_lapComparation_elevationMap_button.setEnabled(False)
        self.plot_lapComparation_elevationMap_button.clicked.connect(self.lapComparation_elevationMap_ShowPlot)
        
        self.lapComparationA_labelTitle = QLabel('Lap A   ')
        self.lapComparationA_labelTitle.setFont(font_bold)
        self.lapComparationA_labelTitle.setEnabled(False)
        self.lapComparationB_labelTitle = QLabel('Lap B   ')
        self.lapComparationB_labelTitle.setFont(font_bold)
        self.lapComparationB_labelTitle.setEnabled(False)
        self.lapComparationA_lapTime_labelTitle = QLabel('Laptime: ')
        self.lapComparationA_lapTime_labelTitle.setEnabled(False)
        self.lapComparationB_lapTime_labelTitle = QLabel('Laptime: ')
        self.lapComparationB_lapTime_labelTitle.setEnabled(False)
        
        self.lapComparationA_avgSpeed_labelTitle = QLabel('Avg Speed: ')
        self.lapComparationA_avgSpeed_labelTitle.setEnabled(False)
        self.lapComparationB_avgSpeed_labelTitle = QLabel('Avg Speed: ')
        self.lapComparationB_avgSpeed_labelTitle.setEnabled(False)       
        self.lapComparationA_avgTemp_labelTitle = QLabel('Avg Air Temp: ')
        self.lapComparationA_avgTemp_labelTitle.setEnabled(False)
        self.lapComparationB_avgTemp_labelTitle = QLabel('Avg Air Temp: ')
        self.lapComparationB_avgTemp_labelTitle.setEnabled(False)
        

        # layouts
        #(right, top, left, bottom)
        main_v_layout = QVBoxLayout()
        logo_h_layout = QHBoxLayout()
        csvTitle_h_layout = QHBoxLayout()
        first_h_layout = QHBoxLayout()
        sessionInfoTitle_h_layout = QHBoxLayout()
        sessionInfoData_h_layout = QHBoxLayout()
        sessionInfoDataLeft_v_layout = QVBoxLayout()
        sessionInfoDataRight_v_layout = QVBoxLayout()
        sessionGraphsTitle_h_layout = QHBoxLayout()
        sessionGraphs_main_h_layout = QHBoxLayout()
        sessionGraphsLeft_v_layout = QVBoxLayout()
        sessionGraphsRight_v_layout = QVBoxLayout()
        lapComparationGraphTitle_h_layout = QHBoxLayout()
        lapComparationGraph_v_main_layout = QVBoxLayout()
        lapComparationData_h_row1_layout = QHBoxLayout()
        lapComparationData_h_row2_layout = QHBoxLayout()
        lapComparationData_h_row3_layout = QHBoxLayout()
        lapComparationData_h_row4_layout = QHBoxLayout()
        
        main_v_layout.setAlignment(Qt.AlignTop)
        

        main_v_layout.addLayout(logo_h_layout)
        main_v_layout.addLayout(csvTitle_h_layout)
        main_v_layout.addLayout(first_h_layout)
        main_v_layout.addLayout(sessionInfoTitle_h_layout)
        main_v_layout.addLayout(sessionInfoData_h_layout)
        main_v_layout.addLayout(sessionGraphsTitle_h_layout)
        main_v_layout.addLayout(sessionGraphs_main_h_layout)
        main_v_layout.addLayout(lapComparationGraphTitle_h_layout)
        main_v_layout.addLayout(lapComparationGraph_v_main_layout)
        
        sessionInfoData_h_layout.addLayout(sessionInfoDataLeft_v_layout)
        sessionInfoData_h_layout.addLayout(sessionInfoDataRight_v_layout)
        
        sessionGraphs_main_h_layout.addLayout(sessionGraphsLeft_v_layout)
        sessionGraphs_main_h_layout.addLayout(sessionGraphsRight_v_layout)
        
        lapComparationGraph_v_main_layout.addLayout(lapComparationData_h_row1_layout)
        lapComparationGraph_v_main_layout.addLayout(lapComparationData_h_row2_layout)
        lapComparationGraph_v_main_layout.addLayout(lapComparationData_h_row3_layout)
        lapComparationGraph_v_main_layout.addLayout(lapComparationData_h_row4_layout)
        
        # Widgets to layouts
        logo_h_layout.addWidget(self.logo_label)
        
        csvTitle_h_layout.addWidget(self.open_csv_title)
        csvTitle_h_layout.setContentsMargins(50, 10, 70, 1)

        first_h_layout.addWidget(self.csv_file_name_label)
        first_h_layout.addWidget(self.csv_button)
        first_h_layout.setContentsMargins(90, 1, 90, 1)
        
        sessionInfoTitle_h_layout.addWidget(self.session_info_labelTitle)
        sessionInfoTitle_h_layout.setContentsMargins(50, 1, 50, 1)
        
        sessionInfoDataLeft_v_layout.addWidget(self.info_label_sessionTime)
        sessionInfoDataLeft_v_layout.addWidget(self.info_label_gpsSats)
        sessionInfoDataLeft_v_layout.addWidget(self.info_label_laps)
        sessionInfoDataLeft_v_layout.addWidget(self.info_label_speed)
        sessionInfoDataLeft_v_layout.addWidget(self.info_label_temp)
        sessionInfoDataLeft_v_layout.addWidget(self.info_label_elevation)
        
        sessionInfoDataRight_v_layout.addWidget(self.drawCircuitButton)
        sessionInfoDataRight_v_layout.setContentsMargins(30, 10, 30, 1)
        sessionInfoData_h_layout.setContentsMargins(100, 10, 110, 20)
        
        sessionGraphsTitle_h_layout.addWidget(self.session_graphs_labelTitle)
        sessionGraphsTitle_h_layout.setContentsMargins(50, 1, 70, 1)
        
        sessionGraphsLeft_v_layout.addWidget(self.checkBox_SessionGraphs_speed)
        sessionGraphsLeft_v_layout.addWidget(self.checkBox_SessionGraphs_accelerometer)
        sessionGraphsLeft_v_layout.addWidget(self.checkBox_SessionGraphs_temp)
        
        sessionGraphsRight_v_layout.addWidget(self.plot_sesssionGraph_telemetry_button)
        sessionGraphsRight_v_layout.addWidget(self.plot_sesssionGraph_gpsData_button)
        sessionGraphsRight_v_layout.setContentsMargins(1, 1, 70, 1)
        sessionGraphs_main_h_layout.setContentsMargins(180, 1, 150, 5)
        
        lapComparationGraphTitle_h_layout.addWidget(self.lap_comparation_graphs_labelTitle)
        lapComparationGraphTitle_h_layout.setContentsMargins(50, 1, 50, 1)
        
        lapComparationData_h_row1_layout.addWidget(self.a_label)
        lapComparationData_h_row1_layout.addWidget(self.comboBox_A)
        lapComparationData_h_row1_layout.addWidget(self.checkBox_LapComparation_speed)
        lapComparationData_h_row1_layout.addWidget(self.checkBox_LapComparation_accelerometer)
        lapComparationData_h_row1_layout.addWidget(self.checkBox_LapComparation_temp)
        #lapComparationData_h_row1_layout.setContentsMargins(40, 1, 1, 1)
        
        lapComparationData_h_row2_layout.addWidget(self.checkBox_B_lap)
        lapComparationData_h_row2_layout.addWidget(self.b_label)
        lapComparationData_h_row2_layout.addWidget(self.comboBox_B)
        lapComparationData_h_row2_layout.addWidget(self.plot_lapComparation_telemetry_button)
        lapComparationData_h_row2_layout.addWidget(self.plot_lapComparation_gpsData_button)
        lapComparationData_h_row2_layout.addWidget(self.plot_lapComparation_elevationMap_button)
        
        lapComparationData_h_row3_layout.addWidget(self.lapComparationA_labelTitle, stretch=0, alignment=Qt.AlignLeft)
        lapComparationData_h_row3_layout.addWidget(self.lapComparationA_lapTime_labelTitle, stretch=1, alignment=Qt.AlignLeft)
        lapComparationData_h_row3_layout.addWidget(self.lapComparationA_avgSpeed_labelTitle, stretch=1, alignment=Qt.AlignLeft)
        lapComparationData_h_row3_layout.addWidget(self.lapComparationA_avgTemp_labelTitle, stretch=1, alignment=Qt.AlignLeft)
        
        lapComparationData_h_row4_layout.addWidget(self.lapComparationB_labelTitle, stretch=0, alignment=Qt.AlignLeft)
        lapComparationData_h_row4_layout.addWidget(self.lapComparationB_lapTime_labelTitle, stretch=1, alignment=Qt.AlignLeft)
        lapComparationData_h_row4_layout.addWidget(self.lapComparationB_avgSpeed_labelTitle, stretch=1, alignment=Qt.AlignLeft)
        lapComparationData_h_row4_layout.addWidget(self.lapComparationB_avgTemp_labelTitle, stretch=1, alignment=Qt.AlignLeft)
        
        lapComparationGraph_v_main_layout.setContentsMargins(80, 1, 20, 10)
        

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
                
                self.info_label_temp.setText("Avg Air Temp: " + str(self.csv_info["avg_temperature"]) + " ºC")
                self.info_label_temp.setEnabled(True)
                
                self.info_label_elevation.setText("Elevation change: " + str(self.csv_info["altitude_diff"]) + " meters")
                self.info_label_elevation.setEnabled(True)
                
                # enable widgets
                self.checkBox_SessionGraphs_speed.setEnabled(True)
                self.checkBox_SessionGraphs_accelerometer.setEnabled(True)
                self.checkBox_SessionGraphs_temp.setEnabled(True)
                self.plot_sesssionGraph_telemetry_button.setEnabled(True)
                self.plot_sesssionGraph_gpsData_button.setEnabled(True)
                
                self.a_label.setEnabled(True)
                self.comboBox_A.setEnabled(True)
                self.checkBox_LapComparation_speed.setEnabled(True)
                self.checkBox_LapComparation_accelerometer.setEnabled(True)
                self.checkBox_LapComparation_temp.setEnabled(True)
                
                self.checkBox_B_lap.setEnabled(True)
                self.plot_lapComparation_telemetry_button.setEnabled(True)
                self.plot_lapComparation_gpsData_button.setEnabled(True)
                self.plot_lapComparation_elevationMap_button.setEnabled(True)
                
                self.lapComparationA_labelTitle.setEnabled(True)
                self.lapComparationA_lapTime_labelTitle.setEnabled(True)
                self.lapComparationA_avgSpeed_labelTitle.setEnabled(True)
                self.lapComparationA_avgTemp_labelTitle.setEnabled(True)
                
                # populate both comboBoxes
                self.populate_CB_laps(self.csv_info["num_laps"])
                
                
            else:
                QMessageBox.warning(self, "Error", "Selected csv file is not valid!")


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
        self.comboBox_A.clear()
        self.comboBox_B.clear()
        
        for i in range(total_laps + 1):
            self.comboBox_A.addItem('Lap {}'.format(i))
            self.comboBox_B.addItem('Lap {}'.format(i))


    def update_lapSelected_A(self, index):
        self.selected_lapA = index
        
        if self.selected_lapA >= 0:
            currentLap_df = self.extract_csv_info_perLap(self.selected_lapA, self.df)
            
            currentLap_avg_speed = round(currentLap_df['speed'].mean() * 1.852, 2)
            currentLap_avg_temp= round(currentLap_df['temperature'].mean(), 2)
            
            lap_time = currentLap_df.iloc[-1]['CurrentTime'] - currentLap_df.iloc[0]['CurrentTime']
            lap_time_seconds = lap_time.total_seconds()
            lap_time_str = '{:02d}:{:02d}:{:02d}'.format(int(lap_time_seconds // 3600), int(lap_time_seconds % 3600 // 60), int(lap_time_seconds % 60))

            self.lapComparationA_lapTime_labelTitle.setText("LapTime: " + lap_time_str)
            self.lapComparationA_avgSpeed_labelTitle.setText("Avg Speed: " + str(currentLap_avg_speed) + " km/h")
            self.lapComparationA_avgTemp_labelTitle.setText("Avg Air Temp: " + str(currentLap_avg_temp) + " ºC")
        
    
    def update_lapSelected_B(self, index):
        self.selected_lapB = index
        
        if self.selected_lapB >= 0:
            currentLap_df = self.extract_csv_info_perLap(self.selected_lapB, self.df)
            
            currentLap_avg_speed = round(currentLap_df['speed'].mean() * 1.852, 2)
            currentLap_avg_temp= round(currentLap_df['temperature'].mean(), 2)
            
            lap_time = currentLap_df.iloc[-1]['CurrentTime'] - currentLap_df.iloc[0]['CurrentTime']
            lap_time_seconds = lap_time.total_seconds()
            lap_time_str = '{:02d}:{:02d}:{:02d}'.format(int(lap_time_seconds // 3600), int(lap_time_seconds % 3600 // 60), int(lap_time_seconds % 60))

            self.lapComparationB_lapTime_labelTitle.setText("LapTime: " + lap_time_str)
            self.lapComparationB_avgSpeed_labelTitle.setText("Avg Speed: " + str(currentLap_avg_speed) + " km/h")
            self.lapComparationB_avgTemp_labelTitle.setText("Avg Air Temp: " + str(currentLap_avg_temp) + " ºC")
    
             
    def extract_csv_info_perLap(self, lap_selected, dataFrame):
        df_currentLap = dataFrame.loc[dataFrame['currentLap'] == lap_selected]
        return df_currentLap
    
    
    
    # GUI listeners methods
    def checkBox_sessionGraph_speed_changed(self):
        if self.checkBox_SessionGraphs_speed.isChecked():
            self.sessionGraph_speed_selected = True
        else:
            self.sessionGraph_speed_selected = False
    
    def checkBox_sessionGraph_accelerometer_changed(self):
        if self.checkBox_SessionGraphs_accelerometer.isChecked():
            self.sessionGraph_acc_selected = True
        else:
            self.sessionGraph_acc_selected = False
            
    def checkBox_sessionGraph_temp_changed(self):
        if self.checkBox_SessionGraphs_temp.isChecked():
            self.sessionGraph_temp_selected = True
        else:
            self.sessionGraph_temp_selected = False   
    
    def sessionGraph_telemetry_ShowPlot(self):
        if not self.sessionGraph_speed_selected and not self.sessionGraph_acc_selected and not self.sessionGraph_temp_selected:
            QMessageBox.warning(self, "Error", "Please, select at least one option.")
        else:    
            self.telemetry_GraphWindow = sessionTelemetryGraph(self.df, self.sessionGraph_speed_selected, self.sessionGraph_acc_selected, self.sessionGraph_temp_selected)
            self.telemetry_GraphWindow.show()
            
    
    def sessionGrap_gpsData_ShowPlot(self):
        self.sessionGPSdata_GraphWindow = sessionGPS_MapGraph(self.csv_file_name)
        self.sessionGPSdata_GraphWindow.show()
        
    
    def checkBox_lapComparation_speed_changed(self):
        if self.checkBox_LapComparation_speed.isChecked():
            self.lapComparationGraph_speed_selected = True
        else:
            self.lapComparationGraph_speed_selected = False
    
    def checkBox_lapComparation_accelerometer_changed(self):
        if self.checkBox_LapComparation_accelerometer.isChecked():
            self.lapComparationGraph_acc_selected = True
        else:
            self.lapComparationGraph_acc_selected = False
            
    def checkBox_lapComparation_temp_changed(self):
        if self.checkBox_LapComparation_temp.isChecked():
            self.lapComparationGraph_temp_selected = True
        else:
            self.lapComparationGraph_temp_selected = False  
    
    
    def lapComparation_telemetry_ShowPlot(self):
        if not self.lapComparationGraph_speed_selected and not self.lapComparationGraph_acc_selected and not self.lapComparationGraph_temp_selected:
            QMessageBox.warning(self, "Error", "Please, select at least one option.")
        else:
            dfA = self.extract_csv_info_perLap(self.selected_lapA, self.df)
            
            if self.lapB_selected:
                dfB = self.extract_csv_info_perLap(self.selected_lapB, self.df)
                self.lapComparationTelemetry_GraphWindow = lapComparationTelemetryGraph(dfA, self.lapComparationGraph_speed_selected, self.lapComparationGraph_acc_selected, self.lapComparationGraph_temp_selected, dfB)                
            else:
                self.lapComparationTelemetry_GraphWindow = lapComparationTelemetryGraph(dfA, self.lapComparationGraph_speed_selected, self.lapComparationGraph_acc_selected, self.lapComparationGraph_temp_selected)
            
            self.lapComparationTelemetry_GraphWindow.show()
    
    
    def lapComparation_gpsData_ShowPlot(self):
        self.lapComparationGPSdata_GraphWindow = sessionGPS_MapGraph(self.csv_file_name, True, self.selected_lapA)
        self.lapComparationGPSdata_GraphWindow.show()
    
    def lapComparation_elevationMap_ShowPlot(self):
        self.elevationMap_GraphWindow = circuitElevationGraph(self.extract_csv_info_perLap(self.selected_lapA, self.df))
        self.elevationMap_GraphWindow.show()
        
    def checkBox_bLap_changed(self):
        if self.checkBox_B_lap.isChecked():
            self.lapB_selected = True
            self.comboBox_B.setEnabled(True)
            self.b_label.setEnabled(True)
            self.lapComparationB_labelTitle.setEnabled(True)
            self.lapComparationB_lapTime_labelTitle.setEnabled(True)
            self.lapComparationB_avgSpeed_labelTitle.setEnabled(True)
            self.lapComparationB_avgTemp_labelTitle.setEnabled(True)
        else:
            self.lapB_selected = False
            self.comboBox_B.setEnabled(False)
            self.b_label.setEnabled(False)
            self.lapComparationB_labelTitle.setEnabled(False)
            self.lapComparationB_lapTime_labelTitle.setEnabled(False)
            self.lapComparationB_avgSpeed_labelTitle.setEnabled(False)
            self.lapComparationB_avgTemp_labelTitle.setEnabled(False)
    
    
    def show_CircuitSketch(self):
        self.circuitSketchWindow = drawCircuitWindow()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet("QLabel{font-size: 11pt;} QPushButton{font-size: 10pt;} QComboBox{font-size: 10pt;}")
    app.setStyleSheet("QLabel{font-size: 9pt;} QPushButton{font-size: 9pt;} QComboBox{font-size: 9pt;}")
    w = MainWindow()
    w.show()
    app.exec()
