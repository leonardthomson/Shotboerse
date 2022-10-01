from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QLabel, QVBoxLayout
from PySide6 import QtWidgets
from PySide6 import *
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt

import pyqtgraph as pg
import sys
from random import randint
import time

import pyttsx3


from myWidget import Ui_MainWindow

# TODO: Schreibe aktuelle Preise ans Ende des Graphs
# TODO: GIB DIE KOSTEN-Berechnung aus
# TODO: Öffne die Nachfrage schön! InputWidget anpassen!
# TODO: Evtl Fehlerbehandlung

# Constant 
ALL_SHOTS = ["Mexikaner", "Gimlet", "Blueshot",
             "BlowJob", "Fishshot", "Tequila",
             "Vodka", "Berentzen", "Joster", "Pfeffi"]
ALL_COLORS = [(103, 19, 16), (108, 103, 97), (60, 182, 204),
              (167, 136, 91), (212, 67, 49), (225, 185, 68),
              (250, 250, 250), (161, 189, 68), (106, 54, 58), (0, 250, 5)]# BJ 100, 57, 28
ALL_DIC = dict(zip(ALL_SHOTS, ALL_COLORS))

# Current Shot selection
shot_names = ALL_SHOTS#["Fishshot", "Tequila", "Vodka", "Berentzen", "Joster", "Pfeffi"]#["Mexikaner", "Gimlet", 'Berentzen']#, "Joster", "Pfeffi", "Tequila"]
assert all(names in ALL_SHOTS for names in shot_names), f"Unrecognized Shot! Allowed shots are:\n{ALL_SHOTS}"
shot_dic = {names:ALL_DIC[names] for names in shot_names}
pen_colors = shot_dic.values()
assert len(pen_colors) == len(shot_names), "We need as much pen colors as shot-names!"

# Inits
val_priceIncrease = 4
avg = 100
minPrice = 30
is_cheap_value = 60
is_already_cheap = [0 for i in range(len(shot_names))]
n_xValues = 30
engine = pyttsx3.init()


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setUpGraph()
        self.shotsBoughtString = " "
        self.ui.lineEdit.returnPressed.connect(self.use_LE_input)
        self.show()



    def setUpGraph(self):
        self.ui.graphicsView.addLegend()

        # styles = {'color': 'r', 'font-size': '50px'}
        #self.ui.graphicsView.setLabel('left', "Preis in Cent", **styles)
        # self.setWindowTitle("STONKS!")

        # INITIALIZE THE GRAPHS
        self.n_Shots = len(shot_names)
        pens = [pg.mkPen(width=3, color=pen_color) for pen_color in pen_colors]
        self.x = list(range(n_xValues))  # 100 time points
        self.y = [randint(0,2*avg) for _ in range(n_xValues)] # 100 data points
        self.y_data = [[100 for _ in range(n_xValues)] for _ in shot_names]
        self.data_lines = [self.ui.graphicsView.plot(self.x, y_data, pen=pen, name=shot_name, symbol='o', symbolSize=10) for y_data, pen, shot_name in zip(self.y_data, pens, shot_names)]

        self.price = [100 for _ in shot_names]
        self.shots_bought = [0 for _ in shot_names]
        self.set_prices()
        self.print_price()

        # DO THE UPDATE-FUNCTION

    def use_LE_input(self):
        self.shotsBoughtString = self.ui.lineEdit.text()
        self.shotsBoughtString = self.shotsBoughtString.replace(" ", "")
        self.ui.lineEdit.setText("")
        #print(self.shotsBoughtString)
        if self.shotsBoughtString == "random":
            self.random_walk()
        elif self.shotsBoughtString == "longrandom":
            self.random_walk(nWalks=15)
        elif self.shotsBoughtString == "reset":
            self.reset()
        elif len(self.shotsBoughtString) == self.n_Shots:
            self.update_shotsBought()
            self.print_price()
            self.update_price()
            self.update_plot_data()
            self.set_prices()
        else:
            self.ui.pay.setText("Schu bsuffe? \nGib die richtige Anzahl an Shots ein!")

    def print_price(self):
        val = sum([nShot*price for nShot, price in zip(self.shots_bought, [y_data[-1] for y_data in self.y_data])])
        string = "Gekauft: \n"
        for nShot, shot_name in zip(self.shots_bought, shot_names):
            if nShot == 0:
                pass
            elif nShot >= 1:
                string += str(nShot) + " " + shot_name + "\n"
        val = round(val/10)/10
        string += "\nPreis: " + str(val) + "0€."

        self.ui.pay.setText(string)
        return val*100

    def set_prices(self):
        self.ui.priceList.clear()
        self.ui.priceList.addItems([shot_name+": "+str(round(price)/100) +"€" for shot_name, price in zip(shot_names, self.price)])
        for idx in range(self.n_Shots):
            if self.price[idx] < is_cheap_value and not is_already_cheap[idx]:
                self.praise_shots(idx)
                is_already_cheap[idx] = 1
            else:
                is_already_cheap[idx] = 0

    def update_plot_data(self):
        self.x = self.x[1:] + [self.x[-1]+1]
        for idx, data_line in enumerate(self.data_lines):
            self.y_data[idx][:] = self.y_data[idx][1:] + [self.price[idx]]  # Add a new random value.
            data_line.setData(self.x, self.y_data[idx][:])  # Update the data.

    def update_shotsBought(self):
        self.shots_bought = [int(val) for val in self.shotsBoughtString]

    # def detect_input(self):

    def update_price(self):
        val1 = sum(self.shots_bought)/(self.n_Shots-1)
        val2 = (1+1/(self.n_Shots-1))
        self.price = [max(lastPrice + val_priceIncrease*(val2 * nShotsBought - val1), minPrice) for lastPrice, nShotsBought in zip([y_data[-1] for y_data in self.y_data], self.shots_bought)]


    def reset(self):
        self.shots_bought = [0 for _ in range(self.n_Shots)]
        self.price = [100 for _ in range(self.n_Shots)]
        self.update_plot_data()
        self.set_prices()
        self.ui.pay.setText("VON NEUEM!")

    def random_walk(self, nWalks=5, nShots=5):
        for i in range(nWalks):
            self.shots_bought = [randint(0, nShots) for _ in range(self.n_Shots)]
            self.update_price()
            self.update_plot_data()
        self.set_prices()
        self.ui.pay.setText("Kleiner Randomwalk gefällig?")

    def repeat_currentData(self):
        self.shots_bought = [0 for _ in range(self.n_Shots)]
        self.update_price()
        self.update_plot_data()

    def praise_shots(self, idx):
        print('cheappppp')
        return
        shot_name = shot_names[idx]
        price = self.price[idx]
        n_praises = 3
        random_idx = randint(0, n_praises-1)
        if random_idx == 0:
            engine.say(shot_name + " ist billig! Kauft " + shot_name)
            engine.say(shot_name + " nur " + str(round(price)) + " Cent!")
        elif random_idx == 1:
            engine.say("Kauft " + shot_name + "!")
            engine.say("Er ist billig und willig!")
        elif random_idx == 2:
            engine.say("Der "+shot_name+"-Markt bricht zusammen!")
            engine.say("Kauft "+shot_name)
        engine.runAndWait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.showMaximized()
    sys.exit(app.exec())