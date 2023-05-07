import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant

class TelemetryTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._data[0])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return QVariant()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                headers = ['Current Time', 'Satellites', 'Speed', 'Latitude', 'Longitude', 'X', 'Y', 'Z', 'Temperature', 'Altitude', 'Current Lap']
                return headers[section]
            return str(section + 1)
        return QVariant()

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        table_model = TelemetryTableModel(data)
        table_view = QTableView()
        table_view.setModel(table_model)
        self.setCentralWidget(table_view)

        self.setWindowTitle('Telemetry Data Viewer')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load data from CSV file
    with open('LOG.CSV', 'r') as f:
        reader = csv.reader(f)
        data = [row for row in reader]

    window = MainWindow(data)
    window.show()

    sys.exit(app.exec_())
