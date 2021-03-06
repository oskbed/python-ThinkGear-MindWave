from PyQt5 import QtCore, QtGui
import pyqtgraph as pg
from LiveWave import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.LiveWave_widget = LiveWidget(self)
        self.LiveWave_widget.button.clicked.connect(self.plotter)
        self.LiveWave_widget.button2.clicked.connect(self.connector)
        self.LiveWave_widget.button3.clicked.connect(self.clear)
        self.LiveWave_widget.button4.clicked.connect(self.stop)
        self.central_widget.addWidget(self.LiveWave_widget)
        self.working = False
    def connector(self):
        self.mw = LiveWave()
    def plotter(self):
        self.LiveWave_widget.plot.clear()
        self.mw.start()
        self.data = [0]
        self.working = True
        while self.working:
            if len(self.data) >= 1024:
                self.data = self.data[1:]
                self.LiveWave_widget.plot.clear()
            self.curve = self.LiveWave_widget.plot.getPlotItem().plot()
            self.data.append(self.mw.rawValue)
            self.curve.setData(self.data)
            app.processEvents()

    def clear(self):
        if self.mw.sendingData:
            self.data = [0]
            self.LiveWave_widget.plot.clear()
        else:
            self.LiveWave_widget.plot.clear()
    def stop(self):
        self.mw.stop()
        self.working = False
        self.mw.sendingData = False
class LiveWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LiveWidget, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        layout1 = QtGui.QVBoxLayout()
        self.button2 = QtGui.QPushButton('Start MindWave')
        layout1.addWidget(self.button2)
        self.button = QtGui.QPushButton('Start Plotting')
        layout1.addWidget(self.button)
        self.button3 = QtGui.QPushButton('Clear Graph')
        layout1.addWidget(self.button3)
        self.button4 = QtGui.QPushButton('Stop Plotting')
        layout1.addWidget(self.button4)
        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)
        layout.addLayout(layout1)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.setWindowTitle("PyQt Live - MindWave Mobile")
    window.show()
    app.exec_()
