import numpy as np
import matplotlib.pyplot as plt
from Settings import *
from Passenger import Passenger

class Station():
    stations = []

    def __init__(self,id,pos,ax):
        self.id = id
        self.arrival_rate = 1/10 # arrival per seccond

        self.pos = pos
        self.width = 200

        self.platform0 = []
        self.inter_arrival_time0 = np.random.exponential(1/self.arrival_rate)

        self.platform1 = []
        self.inter_arrival_time1 = np.random.exponential(1/self.arrival_rate)

        self.rectangle_platform0 = plt.Rectangle((pos-self.width/2, 15), self.width, 5, color='salmon')
        ax.add_patch(self.rectangle_platform0)
        self.text_platform0 = ax.text(pos-self.width/4,16,str(self.platform0),fontsize=15)

        rectangle_platform1 = plt.Rectangle((pos-self.width/2, 40), self.width, 5, color='salmon')
        ax.add_patch(rectangle_platform1)
        self.text_platform1 = ax.text(pos-self.width/4,41,str(self.platform1),fontsize=15)

    def update_platform(self,current_time):
        if(current_time >= self.inter_arrival_time0 and self.id > 0):
            self.platform0.append(Passenger(self.id,0))
            self.inter_arrival_time0 = current_time + np.random.exponential(1/self.arrival_rate)

        if(current_time >= self.inter_arrival_time1 and self.id < no_station - 1):
            self.platform1.append(Passenger(self.id,1))
            self.inter_arrival_time1 = current_time + np.random.exponential(1/self.arrival_rate)

        self.text_platform0.set_text(str(len(self.platform0)))
        self.text_platform1.set_text(str(len(self.platform1)))