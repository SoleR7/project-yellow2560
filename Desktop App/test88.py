import sys
import io
import folium  # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pandas as pd

"""
Folium in PyQt5
"""


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        coordinate = (38.70430, -0.47878)
        m = folium.Map(
            # tiles='cartodbdark_matter',
            tiles='OpenStreetMap',
            zoom_start=15,
            max_zoom=23,
            control_scale=True,
            location=coordinate
        )

        trail_coordinates = self.read_csv_file('LOG.CSV')

        folium.PolyLine(trail_coordinates, tooltip="Coast").add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

    def read_csv_file(self, file_name):
        df = pd.read_csv(file_name, names=['CurrentTime', 'satellites', 'speed', 'latitude', 'longitude', 'x', 'y', 'z', 'temperature', 'altitude', 'currentLap'])
        coords = list(zip(df['latitude'], df['longitude']))
        return coords


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