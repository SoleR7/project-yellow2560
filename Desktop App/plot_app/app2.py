import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import pandas as pd


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.selected_option = None
        self.csv_file_name = None        
        
        #Window title
        self.setWindowTitle("ICZIA - Fermentation CSV Plotter")

        #Create a figure object
        self.fig = Figure()

        #Create an empty canvas that will show the graph
        self.canvas = FigureCanvas(self.fig)
        
        #Create label to hold the image logo of ICZIA
        label_logo = QLabel(self)
        pixmap_logo = QPixmap('logo_iczia.png')
        label_logo.setPixmap(pixmap_logo)

        #Create the text label widgets
        csvFile_label = QLabel('Select a valid .csv file:')
        caracteristic_labelText = QLabel('Property: ')
        self.csvFileSelected = QLabel('')
        
        #Create the button that allows the user to select the .csv file and connects the socket
        csv_button = QPushButton("Open...")
        csv_button.clicked.connect(self.choose_csv_file)
        
        #Creates the comboBox with the options available and connects the socket
        caracteristic_comboBox = QComboBox()
        caracteristic_comboBox.addItems(["Select an option...", "Temperature", "Humidity", "Conductivity", "Salinity", "pH", "TDS", "Alcohol"])
        caracteristic_comboBox.currentIndexChanged.connect(self.update_string_variable)

        #Create a button to show the plot and connects the socket
        showPlot_button = QPushButton('Show Plot')
        showPlot_button.clicked.connect(self.show_plot)
        
        #Create a horizontal box layout widget, this will be the main layout
        main_hLayout = QHBoxLayout()
        
        #Create a vertical box layout widget, for the right part of the window (show plot)
        showPlot_vLayout = QVBoxLayout()        
        
        #Create a vertical box layout widget for the left part of the window (conf)
        confPlot_vLayout = QVBoxLayout()                    
        
        #Create an Horizontal layout for the Select .CSV file part
        selectCSV_layout = QHBoxLayout()
        selectCSV_layout.addWidget(csvFile_label)
        selectCSV_layout.addWidget(csv_button)
        selectCSV_layout.setContentsMargins(20, 50, 20, 0)
        
        #Create an Horizontal layout for the Caracteristic ComboBox part
        caracteristicCB_layout = QHBoxLayout()
        caracteristicCB_layout.addWidget(caracteristic_labelText)
        caracteristicCB_layout.addWidget(caracteristic_comboBox)
        caracteristicCB_layout.setContentsMargins(20, 10, 20, 30)
        
        #Create a Vertical layout just for the csvFileSelected label
        selectedCSVfile_layout = QVBoxLayout()
        
        #Create a Vertical layout just for the showPlot_button label
        showPlotButton_layout = QVBoxLayout()

        #Add the vertical box layouts widgets to the main horizontal layout
        main_hLayout.addLayout(confPlot_vLayout)
        main_hLayout.addLayout(showPlot_vLayout)
        
        #Add the toolbar to the right vertical layout
        self.toolbar = NavigationToolbar(self.canvas, self)                
        showPlot_vLayout.addWidget(self.toolbar)
        showPlot_vLayout.addWidget(self.canvas)

        # set the layout of the main window
        self.setLayout(main_hLayout)

        #Add all the widgets for the left vertical layout
        confPlot_vLayout.addWidget(label_logo)
        
        confPlot_vLayout.addLayout(selectCSV_layout)
        
        selectedCSVfile_layout.addWidget(self.csvFileSelected)
        selectedCSVfile_layout.setContentsMargins(50, 0, 50, 0)
        confPlot_vLayout.addLayout(selectedCSVfile_layout)
        
        confPlot_vLayout.addLayout(caracteristicCB_layout)
        
        showPlotButton_layout.addWidget(showPlot_button)
        showPlotButton_layout.setContentsMargins(70, 0, 70, 0)
        confPlot_vLayout.addLayout(showPlotButton_layout)
        
        confPlot_vLayout.addStretch()

        # set the layout of the main window
        self.setLayout(main_hLayout)


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
            #self.csvFileSelected.setText(self.csv_file_name)     
    
    
    '''Method called from comboBox'''
    def update_string_variable(self, index):
        #Update the string variable based on the selected option in the comboBox
        options = ["Select an option...", "Temperature", "Humidity", "Conductivity", "Salinity", "pH", "TDS", "Alcohol"]
        self.selected_option = options[index]     


    '''Method called from showPlot_button'''
    def show_plot(self):        
        #Create and show the plot window only if the user has selected a .csv file and a valid option
        if self.selected_option == None or self.csv_file_name == None:
            dlg = QMessageBox.warning(self, "Error", "You must select a valid CSV file and option")
            
        else:
            if self.selected_option == "Select an option...":
                dlg = QMessageBox.warning(self, "Error", "You must select a valid option")
                 
            else:
                #Clear existing plots
                self.fig.clf()

                #Read data from CSV file
                data = pd.read_csv(self.csv_file_name, header=None)
                data.columns = ['time', 'temp1', 'temp2', 'hum1', 'hum2', 'cond', 'sal', 'ph', 'tds', 'mq3']
                
                #Plot data
                ax = self.fig.add_subplot(111)
                
                match self.selected_option:
                    case "Temperature":                                    
                        ax.plot(data['time'], data['temp1'], label='Soil Sensor')
                        ax.plot(data['time'], data['temp2'], label='AM2315C')
                        ax.set_xlabel('Time')
                        ax.set_ylabel('Temperature ºC')
                                            
                    case "Humidity":
                        ax.plot(data['time'], data['hum1'], label='Soil Sensor')
                        ax.plot(data['time'], data['hum2'], label='AM2315C')
                        ax.set_xlabel('Time')
                        ax.set_ylabel('Humidity %')
                    
                    case "Conductivity":
                        ax.plot(data['time'], data['cond'], label='Soil Sensor')
                        ax.set_xlabel('Time')
                        ax.set_ylabel('Conductivity 100% = 10%')
                                        
                    case "Salinity":
                        ax.plot(data['time'], data['sal'], label='Soil Sensor')
                        ax.set_xlabel('Time')
                        ax.set_ylabel('Salinity')
                    
                    case "pH":
                        ax.plot(data['time'], data['ph'], label='Soil Sensor')
                        ax.set_xlabel('Time')
                        ax.set_ylabel('pH Level')
                        
                    case "TDS":
                        ax.plot(data['time'], data['tds'], label='Soil Sensor')
                        ax.set_xlabel('Time')
                        ax.set_ylabel('TDS')                        
                    
                    case "Alcohol":
                        ax.plot(data['time'], data['mq3'], label='MQ-3')
                        ax.set_xlabel('Time')
                        ax.set_ylabel('Alcohol detected')                                                
                    case _:
                        pass
                
                ax.legend()
                        
                #Update toolbar to interact with the new generated plot canvas               
                self.toolbar.update()

                #Refresh the canvas to show the new plot
                self.canvas.draw()
                
                


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())