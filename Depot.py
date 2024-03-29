import numpy as np
import matplotlib.pyplot as plt
from Settings import *
from Train import Train
import pygame

class Depot():
    start = None
    end =None

    def __init__(self,train_duration,trains,pos,type='start'):
        self.num_train = 100
        self.trains = trains
        # self.ax = ax

        self.train_duration = train_duration*60

        self.min_train = 0

        self.next_time = 0

        self.width = 300
        pos_y = 20
        self.type = type
        if type == 'start':
            self.pos = 0 
            pos_x = 0-self.width
        else:
            self.pos = pos
            pos_x = pos

        # self.rectangle_train_park = plt.Rectangle((pos_x, pos_y), self.width, 20, color='gold')
        # ax.add_patch(self.rectangle_train_park)
        # self.text_train_park = ax.text(pos_x+self.width/3,pos_y+10,str(self.num_train),fontsize=15)

    def update(self,current_time):
        if current_time >= self.next_time and self.num_train > self.min_train:
            self.next_time = self.next_time + self.train_duration

            if self.type == 'start':
                self.trains.append(Train(1,Depot.end))
            else:
                self.trains.append(Train(0,Depot.start))
            
            self.num_train = self.num_train - 1

            # self.text_train_park.set_text(str(self.num_train))

    def draw(self,screen,offset):
        im = pygame.image.load('img/depot.png').convert()
        im.set_colorkey((0,0,0))
        screen.blit(im,(offset+self.pos-158,370)) 
        screen.blit(im,(offset+self.pos-59,370)) 
        screen.blit(im,(offset+self.pos+40,370))     
        screen.blit(im,(offset+self.pos+139,370))  

        screen.blit(im,(offset+self.pos-158,450)) 
        screen.blit(im,(offset+self.pos-59,450)) 
        screen.blit(im,(offset+self.pos+40,450))     
        screen.blit(im,(offset+self.pos+139,450))         
