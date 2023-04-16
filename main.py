# imports
## general
import json
from logging import raiseExceptions
import pyqtgraph as pg

import sys
from random import randint
import numpy as np
import pyttsx3
## PySide
from PySide6.QtWidgets import QDialogButtonBox, QPushButton, QApplication, QMainWindow, QDialog, QInputDialog, QVBoxLayout, QGroupBox, QGridLayout, QCheckBox, QFileDialog
from PySide6.QtCore import QSize, Qt, QCoreApplication
from PySide6 import *
## own
from myWidget import Ui_MainWindow
from initWindow import Ui_Dialog

# TODO: Schreibe aktuelle Preise ans Ende des Graphs
# TODO: GIB DIE KOSTEN-Berechnung aus
# TODO: Öffne die Nachfrage schön! InputWidget anpassen!
# TODO: Evtl Fehlerbehandlung

# Constant
ALL_SHOTS = ["Mexikaner", "Gimlet", "Blueshot",
             "Fishshot", "Tequila", "Vodka Brause",
             "Berentzen", "Joster", "Pfeffi"]
ALL_COLORS = [(189, 29, 23), (68, 250, 177), (60, 182, 204),
              (212, 67, 49), (225, 185, 68), (250, 250, 250),
              (161, 189, 68), (170, 54, 58), (0, 250, 5)]# BJ 100, 57, 28
ALL_DIC = dict(zip(ALL_SHOTS, ALL_COLORS))

# Current Shot selection
shot_selection = ["Mexikaner", "Gimlet", "Fishshot", "Tequila", "Vodka Brause"] #ALL_SHOTS
assert all(names in ALL_SHOTS for names in shot_selection),\
    f"Unrecognized Shot! Allowed shots are:\n{ALL_SHOTS}"
shot_dic = {names:pg.mkPen(width=4, color=ALL_DIC[names]) for names in shot_selection}

# Inits
val_price_increase = 4
avg = 100
min_price = 30
is_cheap_value = 60
is_already_cheap = [0 for i in range(len(shot_dic))]
# TODO DB: UPDATE NUMBER OF X-VALUES
n_x_values = 30
#engine = pyttsx3.init()

### Speak
class _TTS:

    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()

    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()

f = lambda x: "\t".join((map(str,x)))

class MyDialog(Ui_Dialog):
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        self.log_file = None
        self.toolButtonLogFile.clicked.connect(self.set_log_file)
    
    
    def extract_checks(self):
        ls = [self.mex.isChecked(), self.gim.isChecked(), self.blu.isChecked(),
                self.fis.isChecked(), self.teq.isChecked(), self.vod.isChecked(),
                self.ber.isChecked(), self.jos.isChecked(), self.pfe.isChecked()]
        return ls, self.log_file

    def set_log_file(self):
        """
        Gets path for logfile for party.
        """
        #fileName = QFileDialog.getOpenFileName(d, "Open File", "/home", "TextFiles (*.txt)")
        fileName, filter = QFileDialog.getOpenFileName(parent=None, caption='Open file', dir='.', filter='*.json')
        self.logfile.setText("..." + fileName[-40:])
        self.log_file = fileName


class MyMainWindow(QMainWindow):
    """
    Implementing the functionality for the stock development.
    """
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.log_bool = False
        self.log_file_path = None
        self.n_shots = None
        self.shot_names = []
        self.shot_dic = dict()
        self.count_dic = dict()
        self.ui = Ui_MainWindow()
        self.init_dialog()
        self.ui.setupUi(self)
        self.show()
        self.set_up_graph()
        self.shots_bought_string = " "
        self.is_already_cheap = [0 for _ in range(self.n_shots)]

        # TODO: INSERT POTENTIAL TIMER HERE
        #self.timer = pg.QtCore.QTimer()
        #self.timer.timeout.connect(self.use_le_input())

        self.ui.lineEdit.returnPressed.connect(self.use_le_input)

    def init_dialog(self):
        d = QDialog()
        per_diag = MyDialog()
        per_diag.setupUi(d)
        if not d.exec():
            sys.exit(1)
        ls, log_file_path = per_diag.extract_checks()
        if log_file_path:
            self.log_bool = True
        self.log_file_path = log_file_path
        self.update_shot_names(ls)

    def update_shot_names(self, ls: list):
        self.shot_names = [name for i, name in enumerate(ALL_SHOTS) if ls[i]]
        self.n_shots = len(self.shot_names)
        self.shot_dic = {x: pg.mkPen(width=4, color=ALL_DIC[x]) for x in self.shot_names}
        if self.log_bool:
            self.count_dic = {x:0 for x in self.shot_names}
            self.count_dic["Umsatz"] = 0


    def set_up_graph(self):
        """
        Initializes the Graph with constanst entries.
        """
        self.ui.graphicsView.addLegend()

        # styles = {'color': 'r', 'font-size': '50px'}
        #self.ui.graphicsView.setLabel('left', "Preis in Cent", **styles)
        # self.setWindowTitle("STONKS!")

        # INITIALIZE THE GRAPHS with 100 points
        self.x = np.arange(n_x_values)
        self.y = np.random.rand(n_x_values) * 2 * avg
        self.y_data = np.full(shape=(self.n_shots, n_x_values), fill_value=100)
        self.data_lines = [
            self.ui.graphicsView.plot(
                self.x, y_data,pen=self.shot_dic[name],
                name=name, symbol='o', symbolSize=10)
            for y_data, name in zip(self.y_data, self.shot_dic)]
        self.price = np.full(shape=self.n_shots, fill_value=100)
        self.shots_bought = np.zeros(shape=self.n_shots)
        self.set_prices()
        self.print_price()
        # DO THE UPDATE-FUNCTION

    def use_le_input(self):
        """
        Interpret input from user.
        Counts shot and adapts prices or applies special cases.
        """
        self.shots_bought_string = self.ui.lineEdit.text()
        self.shots_bought_string = self.shots_bought_string.replace(" ", "")
        self.ui.lineEdit.clear()
        if self.shots_bought_string == "random":
            self.random_walk()
        elif self.shots_bought_string == "longrandom":
            self.random_walk(nWalks=20)
        elif self.shots_bought_string == "reset":
            self.reset()
        elif self.shots_bought_string == "clear":

            self.y_data = np.full(shape=(self.n_shots, n_x_values), fill_value=100)
            self.x = np.arange(n_x_values)
            self.reset()
        elif len(self.shots_bought_string) == self.n_shots:
            self.update_shots_bought()
            self.print_price()
            self.update_price()
            self.update_plot_data()
            self.set_prices()
        else:
            self.ui.pay.setText("Schu bsuffe? \nGib die richtige Anzahl an Shots ein!")

    def print_price(self):
        """
        Updates list of prices.
        """
        val = sum([nShot*price for nShot, price in zip(
            self.shots_bought, [y_data[-1] for y_data in self.y_data])])
        string = "Gekauft: \n"
        for nShot, shot_name in zip(self.shots_bought, self.shot_names):
            if self.log_bool:
                self.count_dic[shot_name] += nShot
            if nShot == 0:
                pass
            elif nShot >= 1:
                string += str(nShot) + " " + shot_name + "\n"
        val = round(val/10)/10
        string += "\nPreis: " + str(val) + "0€."
        if self.log_bool:
            self.count_dic["Umsatz"] += val
        self.ui.pay.setText(string)
        
        if self.log_bool:
            with open(self.log_file_path, "w") as outfile:
                outfile.write(json.dumps(self.count_dic, indent=4))
        return val*100

    def set_prices(self):
        """
        Calculate prices.
        """
        self.ui.priceList.clear()
        self.ui.priceList.addItems([shot_name+": "+str(round(price)/100) +"€"\
            for shot_name, price in zip(self.shot_names, self.price)])
        for idx in range(self.n_shots):
            if self.price[idx] < is_cheap_value and not is_already_cheap[idx]:
                self.praise_shots(idx)
                is_already_cheap[idx] = 1
            else:
                is_already_cheap[idx] = 0

    def update_plot_data(self):
        """
        Update plots for new data points.
        """
        self.x += 1
        self.y_data[:,:-1] = self.y_data[:,1:]
        self.y_data[:,-1] = self.price  # Add a new random value.
        [data_line.setData(self.x, self.y_data[idx][:])\
            for idx, data_line in enumerate(self.data_lines)] # Update the data.

    def update_shots_bought(self):
        """
        Updates Attribute.
        """
        self.shots_bought = [int(val) for val in self.shots_bought_string]

    def update_price(self):
        """
        Update lineEdit price.
        """
        val1 = sum(self.shots_bought)/(self.n_shots-1)
        val2 = (1+1/(self.n_shots-1))
        self.price = [max(last_price + val_price_increase*(val2 * n_shots_bought - val1), min_price)\
            for last_price, n_shots_bought in zip(self.y_data[:,-1], self.shots_bought)]


    def reset(self):
        """
        Resets the stock prices to 1Euro.
        """
        self.shots_bought = [0 for _ in range(self.n_shots)]
        self.price = [100 for _ in range(self.n_shots)]
        self.update_plot_data()
        self.set_prices()
        self.ui.pay.setText("VON NEUEM!")

    def random_walk(self, nWalks=5, n_shots=5):
        """
        Simulates 5 random orders.
        """
        for _ in range(nWalks):
            self.shots_bought = [randint(0, n_shots) for _ in range(self.n_shots)]
            self.update_price()
            self.update_plot_data()
        self.set_prices()
        self.ui.pay.setText("Kleiner Randomwalk gefällig?")

    def repeat_current_data(self):
        """
        constant graph?
        """
        self.shots_bought = [0 for _ in range(self.n_shots)]
        self.update_price()
        self.update_plot_data()

    def praise_shots(self, idx):
        """
        Funny message when shots are espacially cheap.
        """
        shot_name = self.shot_names[idx]
        price = self.price[idx]
        n_praises = 3
        random_idx = randint(0, n_praises-1)
        shout_out = ""
        if random_idx == 0:
            shout_out = (
                f"{shot_name} ist billig! Kauft {shot_name}"
                f"{shot_name} nur {str(round(price))} Cent!"
            )
        elif random_idx == 1:
            shout_out = (
                f"Kauft {shot_name}!"
                f"Er ist billig und willig!"
            )
        elif random_idx == 2:
            shout_out = (
                f"Der {shot_name}-Markt bricht zusammen!"
                f"Kauft {shot_name}"
            )
        engine = _TTS()
        engine.start(shout_out)
        del(engine)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.showMaximized()
    sys.exit(app.exec())
