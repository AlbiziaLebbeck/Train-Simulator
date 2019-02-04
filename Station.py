import numpy as np
import matplotlib.pyplot as plt
import pygame
from Settings import *
from Passenger import Passenger

class Station():
    stations = []

    def __init__(self,id,pos,name=None,arrival_rate = 1/10):
        self.id = id
        self.arrival_rate = arrival_rate # arrival per seccond

        if name == None:
            self.name = str(id)
        else:
            self.name = name
        self.pos = pos
        self.width = 200

        self.platform0 = []
        self.inter_arrival_time0 = np.random.exponential(1/self.arrival_rate)

        self.platform1 = []
        self.inter_arrival_time1 = np.random.exponential(1/self.arrival_rate)

        self.station_img = pygame.image.load('img/station.png').convert()
        self.station_img.set_colorkey((157,196,153))

        self.font = pygame.font.SysFont(None, 24)

        # self.rectangle_platform0 = plt.Rectangle((pos-self.width/2, 15), self.width, 5, color='salmon')
        # ax.add_patch(self.rectangle_platform0)
        # self.text_platform0 = ax.text(pos-self.width/4,16,str(self.platform0),fontsize=15)

        # rectangle_platform1 = plt.Rectangle((pos-self.width/2, 40), self.width, 5, color='salmon')
        # ax.add_patch(rectangle_platform1)
        # self.text_platform1 = ax.text(pos-self.width/4,41,str(self.platform1),fontsize=15)

    def update_platform(self,current_time):
        if(current_time >= self.inter_arrival_time0 and self.id > 0):
            self.platform0.append(Passenger(self.id,0))
            self.inter_arrival_time0 = current_time + np.random.exponential(1/self.arrival_rate)

        if(current_time >= self.inter_arrival_time1 and self.id < no_station - 1):
            self.platform1.append(Passenger(self.id,1))
            self.inter_arrival_time1 = current_time + np.random.exponential(1/self.arrival_rate)

        # self.text_platform0.set_text(str(len(self.platform0)))
        # self.text_platform1.set_text(str(len(self.platform1)))

    def draw(self,screen,offset):
        # pygame.draw.rect(screen, (255,0,0), pygame.Rect(40+self.pos/(2*distance+(no_station-1)*distance)*1200, 380, 20, 20))
        # pygame.draw.rect(screen, (255,0,0), pygame.Rect(40+self.pos/(2*distance+(no_station-1)*distance)*1200, 420, 20, 20))
        if offset+40-20+self.pos/scale > -80 and offset+40-20+self.pos/scale <= 1280+40:
            screen.blit(self.station_img,(offset+40-60+self.pos/scale,375))
            screen.blit(self.station_img,(offset+40-20+self.pos/scale,375))
            screen.blit(self.station_img,(offset+40+20+self.pos/scale,375))
            text = self.font.render(self.name, True, (0, 128, 0))
            screen.blit(text,(offset+40-40+self.pos/scale, 340))
            text = self.font.render(str(len(self.platform1)), True, (0, 128, 0))
            screen.blit(text,(offset+40-40+self.pos/scale, 360))
            text = self.font.render(str(len(self.platform0)), True, (0, 128, 0))
            screen.blit(text,(offset+40-40+self.pos/scale, 460))