import numpy as np
import matplotlib.pyplot as plt
import time

from Settings import *
from Station import Station
from Depot import Depot

current_sim_time = 0

fig = plt.figure(figsize=(15,5))
ax = plt.axes()

plt.axis('off')

ax.set_xlim(-300,(no_station+1)*distance+)
ax.set_ylim(0,50)

stations = []
for i in range(no_station):
    Station.stations.append(Station(i,distance+i*distance,ax))

trains = []
# trains.append(Train(1,ax,0))
# trains.append(Train(2,1,ax))
# trains.append(Train(4,0,ax))
# trains.append(Train(9,0,ax))

Depot.start = Depot(10,trains,ax,type='start')
Depot.end = Depot(10,trains,ax,type='end')

railway1 = plt.Line2D([0,(no_station+1)*distance],[25,25],color='black',linewidth=3)
ax.add_line(railway1)

railway2 = plt.Line2D([0,(no_station+1)*distance],[35,35],color='black',linewidth=3)
ax.add_line(railway2)


update_show_time = 0
while(current_sim_time < simulation_time):
    Depot.start.update(current_sim_time)
    Depot.end.update(current_sim_time)

    for i in range(no_station):
        Station.stations[i].update_platform(current_sim_time)

    for train in trains:
        r = train.update_train(current_sim_time)
        if r == 'park':
            trains.remove(train)
    
    print("time:"+str(current_sim_time))
    current_sim_time = current_sim_time + 1        
    
    if current_sim_time >= update_show_time:
        plt.pause(0.001)
        update_show_time = update_show_time + show_speed

input()