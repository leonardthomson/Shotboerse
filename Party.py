from PySide2.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QLabel, QVBoxLayout
from PySide2 import QtWidgets
from PySide2.QtCore import QTimer
from PySide2.QtCore import Qt

import pyqtgraph as pg
import sys
from random import randint
import time


import keyboard

# TODO: Schreibe aktuelle Preise ans Ende des Graphs
# TODO: GIB DIE KOSTEN-Berechnung aus
# TODO: Öffne die Nachfrage schön! InputWidget anpassen!
# TODO: Evtl Fehlerbehandlung

shot_names = ["Mexikaner", "Eierlikör", "Joster", "GimLet"]
str_shot_names = ""
for shot_name in shot_names[:-1]:
    str_shot_names += shot_name + ", "
str_shot_names += shot_names[-1]
val_priceIncrease = 2
avg = 100
minPrice = 30
n_xValues = 30

pen_colors = [(250, 0, 0), (0,255,0), (0,0,255), (255, 255, 255)]
assert len(pen_colors) == len(shot_names), "We need as much pen colors as shot-names!"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()



        self.InputWidget = QInputDialog()

        # INITIALIZE THE PLOTWIDGET
        self.graphWidget = pg.PlotWidget()
        #self.graphWidget.showGrid(x=True, y=True)
        # self.setCentralWidget(self.graphWidget)

        # label
        # self.priceLabel = QLabel()
        # self.priceLabel.setText("Hello World")
        # self.setCentralWidget(self.graphWidget)

        # self.vbox = QVBoxLayout(self)
        # self.vbox.addWidget(self.priceLabel, alignment=Qt.AlignCenter)
        # self.vbox.addWidget(self.graphWidget, alignment=Qt.AlignCenter)
        # self.setLayout(self.vbox)


        #self.graphWidget.setBackground('w')

        self.graphWidget.addLegend(offset=(200, 200), )

        styles = {'color': 'r', 'font-size': '50px'}
        self.graphWidget.setLabel('left', "Preis in Cent", **styles)
        self.setWindowTitle("STONKS!")

        # INITIALIZE THE GRAPHS
        self.n_Shots = len(shot_names)
        pens = [pg.mkPen(width=3, color=pen_color) for pen_color in pen_colors]
        self.x = list(range(n_xValues))  # 100 time points
        self.y = [randint(0,2*avg) for _ in range(n_xValues)] # 100 data points
        self.y_data = [[100 for _ in range(n_xValues)] for _ in shot_names]
        self.data_lines = [self.graphWidget.plot(self.x, y_data, pen=pen, name=shot_name, symbol='x', symbolSize=20) for y_data, pen, shot_name in zip(self.y_data, pens, shot_names)]

        self.update_price = [100 for _ in shot_names]
        self.shots_bought = [0 for _ in shot_names]

        # DO THE UPDATE-FUNCTION
        self.shotsBoughtString = " "
        # self.timer = QTimer()
        # self.timer.setInterval(300)
        #
        # self.timer.timeout.connect(self.do_nothing())
        # self.timer.start()

    def do_nothing(self):
        self.repeat_currentData()

    def print_price(self):
        val = sum([nShot*price for nShot, price in zip(self.shots_bought, [y_data[-1] for y_data in self.y_data])])
        string = "Gekauft: "
        for nShot, shot_name in zip(self.shots_bought, shot_names):
            if nShot == 0:
                pass
            elif nShot >= 1:
                string += str(nShot) + " " + shot_name + ", "

        val = round(val/10)/10
        string += "\nPreis: " + str(val) + "0€."

        print(string)
        return val*100

    def keyPressEvent(self, event):
        # Space to Enter Number of Shots Bought
        # F10 to do a random walk

        if event.key() == Qt.Key_Space:
            self.update_shotsBought()
            self.print_price()
            self.update_priceVector()
            self.update_plot_data()

        if event.key() == Qt.Key_F2:
            self.restart()
            self.update_plot_data()
        if event.key() == Qt.Key_F10:
            self.random_walk()

    def update_plot_data(self):
        self.x = self.x[1:] + [self.x[-1]+1]
        for idx, data_line in enumerate(self.data_lines):
            self.y_data[idx][:] = self.y_data[idx][1:] + [self.update_price[idx]]  # Add a new random value.
            data_line.setData(self.x, self.y_data[idx][:])  # Update the data.

    def update_shotsBought(self):
        length = 0
        while length != self.n_Shots:
            try:
                self.shotsBoughtString, ok = self.InputWidget.getText(self, "Shots", "How many shots bought?\n" + str_shot_names, QLineEdit.Normal, "0"*self.n_Shots)
                self.shotsBoughtString = self.shotsBoughtString.replace(" ", "")
                length = len(self.shotsBoughtString)

            except KeyboardInterrupt:
                break
        self.shots_bought = [int(val) for val in self.shotsBoughtString]

    def update_priceVector(self):
        val1 = sum(self.shots_bought)/(self.n_Shots-1)
        val2 = (1+1/(self.n_Shots-1))
        self.update_price = [max(lastPrice + val_priceIncrease*(val2 * nShotsBought - val1), minPrice) for lastPrice, nShotsBought in zip([y_data[-1] for y_data in self.y_data], self.shots_bought)]

    def restart(self):
        self.shots_bought = [0 for _ in range(self.n_Shots)]
        self.update_price = [100 for _ in range(self.n_Shots)]
        self.update_plot_data()

    def random_walk(self, nWalks = 5, nShots=5):
        for i in range(nWalks):
            self.shots_bought = [randint(0, nShots) for _ in range(self.n_Shots)]
            self.update_priceVector()
            self.update_plot_data()

    def repeat_currentData(self):
        self.shots_bought = [0 for _ in range(self.n_Shots)]
        self.update_priceVector()
        self.update_plot_data




            #[y_data[-1] for y_data in self.y_data] + val_priceIncrease*(1+1/self.nShots) * self.shots_bought - 1/(self.nShots-1)*sum(self.shots_bought)


app = QApplication(sys.argv)
app.setStyleSheet("QLabel{font-size: 24pt;}")
main = MainWindow()
main.showMaximized()
app.exec_()
