import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QComboBox, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import pandas as pd


'''Graph canvas class'''
class MplCanvas(FigureCanvasQTAgg):
    '''Class constructor'''
    def __init__(self, parent=None, width=6, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


'''Class that generates the plot window'''
class PlotWindow(QMainWindow):
    '''Class constructor'''
    def __init__(self, csv_file_name: str, selected_option: str, parent=None,):
        super().__init__(parent)
        
        #Window title
        self.setWindowTitle("Tapa de fermentación")

        self.csv_file_name = csv_file_name
        self.selected_option = selected_option
        
        #Read the CSV file and create a pandas DataFrame.
        data = pd.read_csv(self.csv_file_name, header=None)
        data.columns = ['time', 'temp1', 'temp2', 'hum1', 'hum2', 'cond', 'sal', 'ph', 'tds', 'mq3']

        #Create the maptlotlib FigureCanvas object
        sc = MplCanvas(self, width=10, height=5, dpi=100)

        #Axes, lines, labels and legends configuration depending on the option selected by the user
        match self.selected_option:
            case "Temperature":
                sc.axes.plot(data['time'], data['temp1'], label='Soil Sensor')  #line 1
                sc.axes.plot(data['time'], data['temp2'], label='AM2315C')      #line 2
                
                sc.axes.set_xlabel('Time')
                sc.axes.set_ylabel('Temperature ºC')
                #sc.axes.set_title('Temperature vs. Time')
                sc.axes.legend()
                
            case "Humidity":
                sc.axes.plot(data['time'], data['hum1'], label='Soil Sensor')
                sc.axes.plot(data['time'], data['hum2'], label='AM2315C')
                
                sc.axes.set_xlabel('Time')
                sc.axes.set_ylabel('Humidity %')
                sc.axes.legend()
                
            case "Conductivity":
                sc.axes.plot(data['time'], data['cond'], label='Soil Sensor')
                
                sc.axes.set_xlabel('Time')
                sc.axes.set_ylabel('Conductivity 100% = 10%')
                sc.axes.legend()
                
            case "Salinity":
                sc.axes.plot(data['time'], data['sal'], label='Soil Sensor')
                
                sc.axes.set_xlabel('Time')
                sc.axes.set_ylabel('Salinity')
                sc.axes.legend()
                
            case "pH":
                sc.axes.plot(data['time'], data['ph'], label='Soil Sensor')
                
                sc.axes.set_xlabel('Time')
                sc.axes.set_ylabel('pH Level')
                sc.axes.legend()
            case "TDS":
                sc.axes.plot(data['time'], data['tds'], label='Soil Sensor')
                
                sc.axes.set_xlabel('Time')
                sc.axes.set_ylabel('TDS')
                sc.axes.legend()
                
            case "Alcohol":
                sc.axes.plot(data['time'], data['mq3'], label='MQ-3')
                
                sc.axes.set_xlabel('Time')
                sc.axes.set_ylabel('Alcohol detected')
                sc.axes.legend()
            case _:
                pass

        #Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        #The toolbar gives the user different tools to better visualize the plot
        toolbar = NavigationToolbar(sc, self)

        #We create a vertical layout to add first the toolbar and then the plot
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold the layout
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


'''Class tasked with the MainWindow creation'''
class MainWindow(QMainWindow):
    '''Class constructor'''
    def __init__(self):
        super().__init__()

        self.selected_option = None
        self.csv_file_name = None
        
        #Create text label, button (and its socked)
        self.label = QLabel("")
        showPlot_button = QPushButton("Show Plot")
        showPlot_button.clicked.connect(self.show_plot)
        
        #Create label to hold the image logo of ICZIA
        label_logo = QLabel(self)
        pixmap_logo = QPixmap('logo_iczia.png')
        label_logo.setPixmap(pixmap_logo)

        #Create the button that allows the user to select the .csv file and connects the socket
        csv_button = QPushButton("Choose csv file ...")
        csv_button.clicked.connect(self.choose_csv_file)

        #Creates the comboBox with the options available and connects the socket
        combo_box = QComboBox()
        combo_box.addItems(["Select an option...", "Temperature", "Humidity", "Conductivity", "Salinity", "pH", "TDS", "Alcohol"])
        combo_box.currentIndexChanged.connect(self.update_string_variable)

        #Create a vertical layer in which we add all the widgets
        layout = QVBoxLayout()
        layout.addWidget(label_logo)
        layout.addWidget(self.label)
        layout.addWidget(csv_button)
        layout.addWidget(combo_box)
        layout.addWidget(showPlot_button)

        # Create a placeholder widget to hold our layout.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setWindowTitle("ICZIA - Tapa Fermentación CSV plotter") #MainWindow title


    '''Method called from csv_button'''
    def choose_csv_file(self):
        # Open a file dialog to choose a CSV file
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setDefaultSuffix("csv")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        
        if file_dialog.exec():
            # Get the name of the selected file and store it in self.csv_file_name
            self.csv_file_name = file_dialog.selectedFiles()[0]
            self.label.setText(self.csv_file_name)          
            
    '''Method called from comboBox'''
    def update_string_variable(self, index):
        # Update the string variable based on the selected option in the comboBox
        options = ["Select an option...", "Temperature", "Humidity", "Conductivity", "Salinity", "pH", "TDS", "Alcohol"]
        self.selected_option = options[index]
        
    '''Method called from showPlot_button'''
    def show_plot(self):
        # Create and show the plot window only if the user has selected a .csv file and a valid option
        if self.selected_option == None or self.csv_file_name == None:
            dlg = QMessageBox.warning(self, "Error", "You must select a valid CSV file and option")
        else:
            if self.selected_option == "Select an option...":
                dlg = QMessageBox.warning(self, "Error", "You must select a valid option") 
            else:
                plot_window = PlotWindow(self.csv_file_name, self.selected_option, self)
                plot_window.show()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())