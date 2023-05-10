import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QSplitter, QGraphicsScene, QGraphicsView

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create input fields
        self.x_label = QLabel("X values:")
        self.x_edit = QLineEdit()
        self.y_label = QLabel("Y values:")
        self.y_edit = QLineEdit()
        self.show_plot_button = QPushButton("Show Plot")
        self.show_plot_button.clicked.connect(self.show_plot)

        # Create layout for input fields
        input_layout = QFormLayout()
        input_layout.addRow(self.x_label, self.x_edit)
        input_layout.addRow(self.y_label, self.y_edit)
        input_layout.addRow(self.show_plot_button)

        # Create placeholder widget for plot
        self.plot_widget = QWidget()
        self.plot_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.plot_widget.setStyleSheet("background-color: white")

        # Create splitter to divide the window into two areas
        splitter = QSplitter()
        splitter.addWidget(QWidget())
        splitter.addWidget(self.plot_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)
        self.setWindowTitle("Plotting Tool")

    def show_plot(self):
        # Parse x and y values from input fields
        x_values = [float(x.strip()) for x in self.x_edit.text().split(",")]
        y_values = [float(y.strip()) for y in self.y_edit.text().split(",")]

        # Create QGraphicsScene and QGraphicsView to display the plot
        scene = QGraphicsScene()
        view = QGraphicsView(scene)
        view.setSceneRect(0, 0, 500, 500)

        # Add plot to scene
        for i in range(len(x_values)):
            scene.addEllipse(x_values[i]-5, y_values[i]-5, 10, 10)

        # Remove placeholder widget and add plot widget to splitter
        self.plot_widget.setParent(None)
        self.plot_widget = view
        self.plot_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.plot_widget.setStyleSheet("background-color: white")
        self.layout().addWidget(self.plot_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

