import matplotlib.pyplot as plt
from Settings import *
from Station import Station

class Train():
    def __init__(self,railway,ax,destination,station_index=-1):
        self.capacity = 1000
        self.max_speed = 100*1000/3600
        self.accel = self.max_speed/5
        self.stop_time = 3*60
        self.door_time = 1
        self.passenger_time = 1
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
            pos_y = 25 - 4
            self.pos = distance*(no_station+1)
        else:
            pos_y = 35 - 4 
            self.pos = 0

        if station_index > -1:
            self.pos = Station.stations[self.station_index].pos
            self.next_time = self.stop_time


        self.rectangle_train = plt.Rectangle((self.pos-self.width/2, pos_y), self.width, 8, color='green')
        ax.add_patch(self.rectangle_train)
        self.text_train = ax.text(self.pos-self.width/4,pos_y+1,str(self.speed),fontsize=15)
    
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
                        # self.railway = 0
                        # self.rectangle_train.set_y(25 - 4)
                        # self.text_train.set_y(25 - 3)
                        # self.next_time = current_time + self.stop_time
                        # self.entrance_time = current_time + self.door_time
                        # self.exit_time = current_time + self.door_time
                        # self.closing_time = self.next_time - self.door_time 
                    else:
                        self.break_pos = Station.stations[self.station_index].pos - (self.max_speed**2)/(2*self.accel)
                        print(Station.stations[self.station_index].pos)
                        print(self.break_pos)
                else:
                    self.state = "move"
                    self.station_index = self.station_index - 1
                    if self.station_index == -1:
                        self.break_pos = self.destination.pos + (self.max_speed**2)/(2*self.accel)
                        # self.railway = 1
                        # self.rectangle_train.set_y(35 - 4)
                        # self.text_train.set_y(35 - 3)
                        # self.next_time = current_time + self.stop_time
                        # self.entrance_time = current_time + self.door_time
                        # self.exit_time = current_time + self.door_time
                        # self.closing_time = self.next_time - self.door_time 
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
                        self.destination.text_train_park.set_text(str(self.destination.num_train))
                        self.rectangle_train.set_visible(False)
                        self.text_train.set_visible(False)
                        print('delete')
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
                        self.destination.text_train_park.set_text(str(self.destination.num_train))
                        self.rectangle_train.set_visible(False)
                        self.text_train.set_visible(False)
                        return 'park'

        self.rectangle_train.set_x(self.pos-self.width/2)
        self.text_train.set_x(self.pos-self.width/4)
        self.text_train.set_text(str(len(self.passenger)))
        # self.text_train.set_text(str(self.speed/1000*3600))