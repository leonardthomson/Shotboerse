import math
import random
from tkinter import *
from time import sleep

import numpy as np
class myWheel():
    def __init__(self, shots, width=400, height=400):
        self.shots = shots
        self.width = width
        self.height = height
        self.colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "grey"][0:len(shots)]
        self.angle_width = int(360/len(shots))
        self.wheel_angle = 0
        self.timing_step = 50
        self.main_window = Tk()
        self.main_window.configure(bg="black")
        self.main_window.title("Wheel of Fortune")

        self.main_window.geometry("520x520+300+200")
        self.canvas = Canvas(self.main_window, width=500, height=500, bg="black", bd=0, highlightthickness=0)
        self.canvas.place(x=50, y=50)
        self.canvas.create_oval(100, 100, 300, 300, fill="white", outline="black")

        self.draw_wheel()
        self.button = Button(self.main_window, text="Spin", command=self.set_up_spin)
        self.button.place(x=150, y=100)
        self.main_window.mainloop()


    def draw_wheel(self, angle=0):
        self.starting_angle = angle * 360/100
        coord = 100, 100, 300, 300
        self.edge_angles = [self.starting_angle + idx * self.angle_width for idx in range(len(self.shots))]

        for idx in range(len(self.shots)):
            # draw the piece
            self.canvas.create_arc(coord, start=self.edge_angles[idx], extent=self.angle_width, fill=self.colors[idx], outline=self.colors[idx])
            # put text into the middle of the piece
            # 1. calculate the middle angle of the piece
            mid_angle = self.edge_angles[idx] + self.angle_width/2
            # 2. calculate the middle point of the piece
            midX = 200 + 100 * math.cos(mid_angle/360*2*np.pi) / 2
            midY = 200 - 100 * math.sin(mid_angle/360*2*np.pi) / 2
            # 3. put the text into the middle point
            # change color of text to white
            self.canvas.create_text(midX, midY, text=self.shots[idx], fill="black", font="Times 10 bold")
        # return the angle at the top


    def set_up_spin(self):
        spin_time = (3 + random.randint(0, 3)) * 1000
        n_steps = spin_time // self.timing_step
        step_increase = np.linspace(6, 0, n_steps)
        angles = np.zeros(n_steps)
        angles[0] = self.wheel_angle
        for idx in range(n_steps - 1):
            angles[idx + 1] = angles[idx] + step_increase[idx]

        # clear the canvas
        for i in range(n_steps):
            wheel_angle = angles[i]
            self.spin_step(wheel_angle)
            self.main_window.update()
            sleep(0.05)
        self.wheel_angle = angles[-1]
        # highlight the winning piece
        self.canvas.create_arc(100, 100, 300, 300, start=self.wheel_angle, extent=angles[0] - angles[-1],
                                 fill="white", outline="white")

    def spin_step(self, angle):
        # clear the canvas
        self.canvas.delete("all")
        # create a pie chart
        self.draw_wheel(angle=angle)


def main():
    colV = ["Red", "Green", "Blue", "Yellow"]
    myWheel(colV)

if __name__ == "__main__":
    main()