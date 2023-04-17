# imports
## general
import glob
import json
from datetime import datetime
from logging import raiseExceptions
import pyqtgraph as pg
import os

import sys
from random import randint
import numpy as np
import pyttsx3
## PySide
from PySide6.QtWidgets import QDialogButtonBox, QPushButton, QApplication, QMainWindow, QDialog, QInputDialog, \
    QVBoxLayout, QGroupBox, QGridLayout, QCheckBox, QFileDialog, QLabel, QSizePolicy
from PySide6.QtCore import QSize, Qt, QCoreApplication
from PySide6.QtGui import QFont, QShortcut, QKeySequence
from PySide6 import *
## own
from myWidget import Ui_MainWindow
from initWindow import Ui_Dialog

import random_events

# TODO DB: Maybe count, how often every shot was bought

# Constant
# Mexi, Gin, Tequila, Vodka

ALL_SHOTS = ["Mexikaner", "Gimlet", "Blueshot",
             "Fishshot", "Tequila", "Vodka Brause",
             "Berentzen", "Joster", "Pfeffi"]
ALL_COLORS = [(189, 29, 23), (68, 250, 177), (60, 182, 204),
              (212, 67, 49), (225, 185, 68), (250, 250, 250),
              (161, 189, 68), (170, 54, 58), (0, 250, 5)]# BJ 100, 57, 28
ALL_DIC = dict(zip(ALL_SHOTS, ALL_COLORS))

# Current Shot selection
shot_selection = ["Mexikaner", "Gimlet", "Tequila", "Vodka Brause"] #ALL_SHOTS
assert all(names in ALL_SHOTS for names in shot_selection),\
    f"Unrecognized Shot! Allowed shots are:\n{ALL_SHOTS}"
shot_dic = {names: pg.mkPen(width=4, color=ALL_DIC[names]) for names in shot_selection}

# Inits

# Time, after which a shot automatically updates (in seconds)
update_time = 1
# The noise we add in each time step
step_noise = .7

# Time, after which a stock event occurs (in seconds)
event_time = 20
# Events occure every event_time +- event_time_variance(in seconds)
event_time_variance = 2

# Time, after which we save the y_data (in minutes)
logging_minutes = 5

# Buying a shot increases it's price by this size
val_price_increase = 4


# Price, from which the shots start
avg = 100

# Minimal price for shots. If it goes lower, we just choose min_price
min_price = 50

# From this point on we consider the shot to be cheap
is_cheap_value = 50
is_already_cheap = [0 for i in range(len(shot_dic))]

# TODO DB: UPDATE NUMBER OF X-VALUES
n_x_values = 1000
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
        self.shots_bought_string = " "
        self.ui = Ui_MainWindow()
        self.init_dialog()
        self.ui.setupUi(self)
        self.show()
        self.set_up_graph()


        # Flag, whether the shot was already announced as being cheap
        self.is_already_cheap = [0 for _ in range(self.n_shots)]

        # TIMERS
        self.timer_seconds = pg.QtCore.QTimer()
        self.timer_seconds.setInterval(update_time*1000)
        self.timer_seconds.timeout.connect(self.noised_time_step)
        self.timer_seconds.start()

        self.timer_events = pg.QtCore.QTimer()
        self.timer_events.setInterval(event_time*1000)
        self.timer_events.timeout.connect(self.stock_event)
        self.timer_events.start()

        # Time until we save the y_data
        self.timer_logging = pg.QtCore.QTimer()
        self.timer_logging.setInterval(logging_minutes * 60 * 1000)
        self.timer_logging.timeout.connect(self.save_y_data_as_file)
        self.timer_logging.start()

        self.all_events = random_events.get_events()
        self.event_idx = 0
        self.n_events = len(self.all_events)

        self.output_window = QDialog()
        self.output_window.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.output_window.setStyleSheet("background-color: black")
        self.output_window.setStyleSheet("border: 2px solid red;")
        self.output_label = QLabel("Output Window", self.output_window)
        self.output_label.setWordWrap(True)
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setFont(QFont("Arial", 50))
        self.output_label.setGeometry(300,200,300,300)
        self.output_label.setStyleSheet("color: red")

        self.output_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        shortcut = QShortcut(QKeySequence(Qt.Key_P), self.output_window)
        shortcut.activated.connect(self.output_window.close)

        #self.output_label.setSizePolicy(PySide6.QtWidgets.)
        #self.output_window.set_title("EVENT OCCURED!")

        self.ui.lineEdit.returnPressed.connect(self.use_le_input)

    def closeEvent(self, *args, **kwargs):
        super(MyMainWindow, self).closeEvent(*args, **kwargs)
        # Here we can simply save the y_data!
        print("We saved the data!")
        self.save_y_data_as_file()


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

    def save_y_data_as_file(self):
        # Use numpy to save the y_data and give a time_stamp
        time_stamp = datetime.now().strftime("%Y-%m-%d_%H")
        np.save(".\\time_stamps\y_data_"+str(time_stamp), self.y_data)

    def load_y_data(self, path):
        if path:
            # We load the newest y_data file in our current folder
            # RIGHT NOW WE ONLY LOAD THE NEWEST ONE
            files = glob.glob(r".\time_stamps\y_data_*.npy")
            if len(files) == 0:
                print("No y_data file found!")
                return 0
            files.sort(key=os.path.getmtime)
            self.y_data = np.load(files[-1])
            #self.update_price()
            #self.update_shots_bought()

    def set_up_graph(self):
        """
        Initializes the Graph with constanst entries.
        """
        self.ui.graphicsView.addLegend()
        self.ui.graphicsView.setLabel('left', "Price", units='.01€')
        # INITIALIZE THE GRAPHS with n_x_values points
        self.x = np.arange(n_x_values)
        if not self.log_bool:
            self.y_data = random_events.valid_random_walks(self.n_shots, n_x_values, avg, 2, epsilon=15)
        else:
            self.load_y_data(self.log_file_path)

        self.data_lines = [
            self.ui.graphicsView.plot(
                self.x, y_data,pen=self.shot_dic[name],
                name=name, symbol='o', linewidth=.5, symbolSize=2)
            for y_data, name in zip(self.y_data, self.shot_dic)]
        self.price = self.y_data[:,-1]#np.full(shape=self.n_shots, fill_value=100)
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

        # HARDCODED SPECIAL CASES
        if self.shots_bought_string == "stoptimer":
            self.timer_seconds.stop()
        elif self.shots_bought_string == "starttimer":
            self.timer_seconds.start()
        elif self.shots_bought_string == "stopevents":
            self.timer_events.stop()
        elif self.shots_bought_string == "startevents":
            self.timer_events.start()
        elif self.shots_bought_string == "random":
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
        self.ui.priceList.addItems([f"{shot_name}: {(price/100):.2f}€"
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
        self.y_data[:,-1] = self.price  # Add the new price value

        for idx, data_line in enumerate(self.data_lines):# Update the data.
            data_line.setData(self.x, self.y_data[idx][:])
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

        self.price = [max(last_price + val_price_increase*(val2 * n_shots_bought - val1), min_price) \
            for last_price, n_shots_bought in zip(self.y_data[:, -1], self.shots_bought)]

    def noised_time_step(self, noise=step_noise):
        """
        Simulates one time step.
        """
        self.price = [max(self.price[idx] + noise*(np.random.rand()-0.5), min_price) for idx in range(self.n_shots)]
        self.update_plot_data()
        self.set_prices()
        self.print_price()

    def stock_event(self):
        """
        Triggers the next event.

        """
        # Choose event
        current_evt =self.all_events[self.event_idx]
        event_text = current_evt[0]
        price_change = current_evt[1]

        self.output_label.setText(event_text)
        self.output_window.setStyleSheet("background-color: black")
        self.output_window.setStyleSheet("border: 2px solid red;")
        self.output_label.adjustSize()
        self.output_window.show()

        # Update event_idx
        self.event_idx += 1
        if self.event_idx >= self.n_events:
            # Return a new list of events
            self.all_events = random_events.get_events()
            self.event_idx = 0

        self.price = [max(self.price[idx] + price_change[idx], min_price) for idx in range(self.n_shots)]
        self.update_plot_data()
        self.set_prices()
        self.print_price()

        # Set a new event-timing
        self.timer_events.setInterval((event_time + np.random.randint(-event_time_variance, event_time_variance))* 1000)


    def reset(self):
        """
        Resets the stock prices to 1Euro.
        """
        self.shots_bought = [0 for _ in range(self.n_shots)]
        self.price = [100 for _ in range(self.n_shots)]
        self.update_plot_data()
        self.set_prices()
        self.ui.pay.setText("VON NEUEM!")

    def random_walk(self, nWalks=5):
        """
        Simulates 5 random orders.
        """
        for _ in range(nWalks):
            self.shots_bought = [randint(0, self.n_shots) for _ in range(self.n_shots)]
            self.update_price()
            self.update_plot_data()
        self.set_prices()
        #self.ui.pay.setText("Kleiner Randomwalk gefällig?")

    def praise_shots(self, idx):
        """
        Funny message when shots are espacially cheap.
        """
        shot_name = self.shot_names[idx]
        price = self.price[idx]
        n_praises = 3
        random_idx = randint(0, n_praises-1)

        shoutouts = [(f"{shot_name} ist billig! Kauft {shot_name}", f"{shot_name} nur {str(round(price))} Cent!"),
                     (f"Kauft {shot_name}!", f"Er ist billig und willig!"),
                     (f"Der {shot_name}-Markt bricht zusammen!", f"Kauft {shot_name}!")]
        shout_out = shoutouts[random_idx]
        engine = _TTS()
        engine.start(shout_out)
        del(engine)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
    window.showMaximized()
    sys.exit(app.exec())
