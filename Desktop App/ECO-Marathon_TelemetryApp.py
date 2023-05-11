import sys
import pandas as pd
from fontTools.merge import first
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.csv_file_name = None

        #GUI
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
        #...

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
        button_h_layout_one = QHBoxLayout()
        button_h_layout_two = QHBoxLayout()
        button_h_layout_three = QHBoxLayout()

        main_v_layout.addWidget(self.logo_label)
        main_v_layout.addLayout(first_h_layout)
        main_v_layout.addLayout(button_h_layout_one)
        main_v_layout.addLayout(button_h_layout_two)
        main_v_layout.addLayout(button_h_layout_three)

        first_h_layout.addWidget(self.csv_button)
        first_h_layout.setContentsMargins(150, 10, 150, 30)

        button_h_layout_one.addWidget(self.racingLineMap_button)
        button_h_layout_one.addWidget(self.circuitElevation_button)
        button_h_layout_one.setContentsMargins(110, 10, 110, 5)

        button_h_layout_two.addWidget(self.speed_button)
        button_h_layout_two.addWidget(self.accelerometer_button)
        button_h_layout_two.setContentsMargins(110, 0, 110, 5)

        button_h_layout_three.addWidget(self.temperature_button)
        button_h_layout_three.setContentsMargins(110, 0, 110, 20)

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
        
            #check if the file is valid
            #...
            #extract info from csv file
            #...
            #update info section
            #...

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
