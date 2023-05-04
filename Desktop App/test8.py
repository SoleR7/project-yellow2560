import sys
import io
import folium  # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine
import csv

"""
Folium in PyQt5
"""


def read_csv_file(file_name):
    coords = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            latitude = float(row[3])
            longitude = float(row[4])
            coords.append((latitude, longitude))
    return coords

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        coordinate = (38.70430,-0.47878)
        m = folium.Map(
            #tiles='cartodbdark_matter',
            tiles='OpenStreetMap',
            zoom_start=15,
            max_zoom=23,
            control_scale=True,
            location=coordinate
        )

        trail_coordinates = read_csv_file('LOG.CSV')

        folium.PolyLine(trail_coordinates, tooltip="Coast").add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')