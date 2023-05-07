import sys
import random
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the main window
        self.setWindowTitle("Main Window")

        # Create the buttons
        self.button1 = QPushButton("Graph 1", self)
        self.button2 = QPushButton("Graph 2", self)
        self.button3 = QPushButton("Graph 3", self)

        # Connect the buttons to their respective functions
        self.button1.clicked.connect(self.show_graph1)
        self.button2.clicked.connect(self.show_graph2)
        self.button3.clicked.connect(self.show_graph3)

        # Add the buttons to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        # Create the central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_graph1(self):
        print("1")
        graph_window = GraphWindow()
        graph_window.show_graph(random.sample(range(10), 5))
        graph_window.show()

    def show_graph2(self):
        graph_window = GraphWindow()
        graph_window.show_graph(random.sample(range(10), 10))
        graph_window.show()

    def show_graph3(self):
        graph_window = GraphWindow()
        graph_window.show_graph(random.sample(range(10), 10))
        graph_window.show()


class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the graph window
        self.setWindowTitle("Graph Window")

    def show_graph(self, data):
        # Create the plot
        fig, ax = plt.subplots()
        ax.plot(data)

        # Add the plot to the layout
        layout = QVBoxLayout()
        layout.addWidget(fig.canvas)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
