import numpy as np
# import matplotlib.pyplot as plt
import time
import pygame

from Settings import *
from Station import Station
from Depot import Depot

current_sim_time = 0

pygame.init()
pygame.display.set_caption("Train Simulator")
# screen = pygame.display.set_mode((1280,720),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
screen = pygame.display.set_mode((1280,720), pygame.HWSURFACE|pygame.DOUBLEBUF)
offset = 0

# train_img = pygame.transform.scale(pygame.image.load('img/train.png').convert(),(215,20))
train_img = pygame.image.load('img/train.png').convert()
train_img.set_colorkey((253,236,166))

sky_img = pygame.image.load('img/sky.png').convert()

# fig = plt.figure(figsize=(15,5))
# ax = plt.axes()

# plt.axis('off')

# ax.set_xlim(-300,(no_station+1)*distance+)
# ax.set_ylim(0,50)

stations = []
for i in range(no_station):
    Station.stations.append(Station(i,distance[i+1],name[i],1/10))

trains = []

Depot.start = Depot(15,trains,type='start')
Depot.end = Depot(15,trains,type='end')

# railway1 = plt.Line2D([0,(no_station+1)*distance],[25,25],color='black',linewidth=3)
# ax.add_line(railway1)

def draw_railway(screen,offset):
    railway = pygame.image.load('img/railway.png').convert()
    railway.set_colorkey((255,255,255))

    for i in range(int(distance[-1]/scale/200)+1):
        if offset+40+200*i >= 1280:
            break
        if offset+40+200*i > -200 and offset+40+200*i < 1280:
            screen.blit(railway,(offset+40+200*i,400))
            screen.blit(railway,(offset+40+200*i,480))

# train = pygame.transform.scale(pygame.image.load('img/train.png').convert(),(100,10))
# train.set_colorkey((157,196,153))
# screen.blit(train,(200,395))

# railway2 = plt.Line2D([0,(no_station+1)*distance],[35,35],color='black',linewidth=3)
# ax.add_line(railway2)
# pygame.display.update()


update_show_time = 0
running = True
shift_speed = 0
while current_sim_time < simulation_time and running:
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shift_speed = 2
            if event.key == pygame.K_RIGHT:
                shift_speed = -2
            
            if event.key == pygame.K_ESCAPE:
                running = False
        
        if event.type == pygame.KEYUP:
            shift_speed = 0
    if shift_speed != 0:
        offset += shift_speed

    screen.fill((255,255,255))
    screen.blit(sky_img,(0-20+offset*0.03,0))

    Depot.start.update(current_sim_time)
    Depot.end.update(current_sim_time)

    for i in range(no_station):
        Station.stations[i].update_platform(current_sim_time)
        Station.stations[i].draw(screen,offset)

    for train in trains:
        r = train.update_train(current_sim_time)
        if r == 'park':
            trains.remove(train)
        else:
            train.draw(screen,train_img,offset)

    draw_railway(screen,offset)

    pygame.display.update()

    print("time:"+str(current_sim_time))
    current_sim_time = current_sim_time + 1     
    
    if current_sim_time >= update_show_time:
        # plt.pause(0.001)
        update_show_time = update_show_time + show_speed

pygame.quit()