import matplotlib.pyplot as plt
import pygame
from Settings import *
from Station import Station

class Train():
    def __init__(self,railway,destination,capacity = 400,max_speed=60,station_index=-1):
        self.capacity = capacity
        self.max_speed = max_speed*1000/3600
        self.accel = self.max_speed/10
        self.door_time = 1
        self.passenger_time = 1
        self.stop_time = self.passenger_time*self.capacity+2*self.door_time
        self.destination = destination

        if station_index == -1 and railway == 0:
            self.station_index = no_station
        else:
            self.station_index = station_index
        self.railway = railway

        self.width = 100
        self.passenger = []
        self.speed = 0

        self.state = "stop"
        self.next_time = 0
        self.entrance_time = self.door_time
        self.exit_time = self.door_time
        self.closing_time = self.stop_time - self.door_time 

        if self.railway == 0:
            self.pos_y = 415
            self.pos = distance[-1]
        else:
            self.pos_y = 390
            self.pos = 0

        if station_index > -1:
            self.pos = Station.stations[self.station_index].pos
            self.next_time = self.stop_time

        self.font = pygame.font.SysFont(None, 18)

        # self.rectangle_train = plt.Rectangle((self.pos-self.width/2, pos_y), self.width, 8, color='green')
        # ax.add_patch(self.rectangle_train)
        # self.text_train = ax.text(self.pos-self.width/4,pos_y+1,str(self.speed),fontsize=15)
    
    def update_train(self,current_time):
        if self.state == "stop":
            if current_time >= self.entrance_time and current_time <= self.closing_time and len(self.passenger) < self.capacity:
                if self.railway and len(Station.stations[self.station_index].platform1) > 0:
                    self.passenger.append(Station.stations[self.station_index].platform1.pop(0))
                elif self.railway == 0 and len(Station.stations[self.station_index].platform0) > 0:
                    self.passenger.append(Station.stations[self.station_index].platform0.pop(0))
                self.entrance_time = current_time + self.passenger_time 

            if current_time >= self.exit_time and current_time <= self.closing_time and len(self.passenger) > 0:
                for i in range(len(self.passenger)):
                    if self.passenger[i].target == self.station_index:
                        self.passenger.pop(i)
                        self.exit_time = current_time + self.passenger_time 
                        break

            if current_time >= self.next_time:
                if self.railway:
                    self.state = "move"
                    self.station_index = self.station_index + 1
                    if self.station_index == no_station:
                        self.break_pos = self.destination.pos - (self.max_speed**2)/(2*self.accel)
                    else:
                        self.break_pos = Station.stations[self.station_index].pos - (self.max_speed**2)/(2*self.accel)
                        print(Station.stations[self.station_index].pos)
                        print(self.break_pos)
                else:
                    self.state = "move"
                    self.station_index = self.station_index - 1
                    if self.station_index == -1:
                        self.break_pos = self.destination.pos + (self.max_speed**2)/(2*self.accel)
                    else:
                        self.break_pos = Station.stations[self.station_index].pos + (self.max_speed**2)/(2*self.accel)
        if self.state == "move":
            if self.speed < self.max_speed:
                self.speed = self.speed + self.accel
                if self.speed > self.max_speed:
                    self.speed = self.max_speed
            if self.railway:        
                self.pos = self.pos + self.speed
                if self.pos >= self.break_pos:
                    self.state = "break"
            else:
                self.pos = self.pos - self.speed
                if self.pos <= self.break_pos:
                    self.state = "break"

        if self.state == "break":
            self.speed = self.speed - self.accel
            if self.speed <= 0:
                self.speed = 1
            if self.railway:        
                self.pos = self.pos + self.speed
                if self.station_index < no_station:
                    if self.pos >= Station.stations[self.station_index].pos:
                        self.speed = 0
                        self.pos = Station.stations[self.station_index].pos
                        self.state = "stop"
                        self.next_time = current_time + self.stop_time
                        self.entrance_time = current_time + self.door_time
                        self.exit_time = current_time + self.door_time
                        self.closing_time = self.next_time - self.door_time 
                else:
                    if self.pos >= self.destination.pos:
                        self.destination.num_train = self.destination.num_train + 1
                        # self.destination.text_train_park.set_text(str(self.destination.num_train))
                        # self.rectangle_train.set_visible(False)
                        # self.text_train.set_visible(False)
                        return 'park'
            else:
                self.pos = self.pos - self.speed
                if self.station_index >= 0:
                    if self.pos <= Station.stations[self.station_index].pos:
                        self.speed = 0
                        self.pos = Station.stations[self.station_index].pos
                        self.state = "stop"
                        self.next_time = current_time + self.stop_time
                        self.entrance_time = current_time + self.door_time
                        self.exit_time = current_time + self.door_time
                        self.closing_time = self.next_time - self.door_time 
                else:
                    if self.pos <= self.destination.pos:
                        self.destination.num_train = self.destination.num_train + 1
                        # self.destination.text_train_park.set_text(str(self.destination.num_train))
                        # self.rectangle_train.set_visible(False)
                        # self.text_train.set_visible(False)
                        return 'park'

        # self.rectangle_train.set_x(self.pos-self.width/2)
        # self.text_train.set_x(self.pos-self.width/4)
        # self.text_train.set_text(str(len(self.passenger)))
        # self.text_train.set_text(str(self.speed/1000*3600))
    
    def draw(self,screen,train_img,offset):
        if offset+40-68+self.pos/scale > -68 and offset+40-68+self.pos/scale < 1280:
            screen.blit(train_img,(offset+40-68+self.pos/scale,self.pos_y))
            text = self.font.render(str(len(self.passenger)), True, (0, 0, 128))
            screen.blit(text,(offset+40+self.pos/scale, self.pos_y-10))