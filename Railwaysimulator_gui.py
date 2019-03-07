import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import time
import pygame
import os

from Settings import *
from Station import Station
from Depot import Depot
from Train import Train


class RailwaySimulation(tk.Frame):
    def __init__(self, master,width=1024,height=250):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height
        self.master.title('Railway Simulator')
        self.master.geometry(str(width)+'x'+str(height))
        self.pack(fill=tk.BOTH)

        #########################################
        ######   Simulation Control Frame  ######
        #########################################
        self.run_frame = ttk.Frame(self,relief=tk.RAISED,height=40)
        self.run_frame.pack(fill=tk.X)
        
        ttk.Label(self.run_frame,text="Simulation time",font=('Verdana',16)).pack(side=tk.LEFT,padx=4,pady=4)

        self.simtime = tk.StringVar(value='1')
        self.simtime_entry = ttk.Entry(self.run_frame,textvariable=self.simtime,font=('Verdana',16),width=10)
        self.simtime_entry.pack(side=tk.LEFT,padx=4,pady=4)

        self.timeOption = tk.StringVar()
        self.timeOption.set("hours") # initial value
        self.timeOption_Menu = tk.OptionMenu(self.run_frame, self.timeOption, "hours", "minutes", "seconds")
        self.timeOption_Menu.pack(side=tk.LEFT,padx=4,pady=4)

        self.run_button = ttk.Button(self.run_frame,text = 'RUN',command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT,padx=4,pady=4)

        self.curtime = tk.StringVar(value="00:00:00")
        ttk.Label(self.run_frame,textvariable=self.curtime,font=('Verdana',16)).pack(side=tk.RIGHT,padx=4,pady=4)
        ttk.Label(self.run_frame,text="Time:",font=('Verdana',16)).pack(side=tk.RIGHT,padx=4,pady=4)

        #########################################
        ###### Notebook for parameter edit ######
        #########################################
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH)
        
        self.train_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.train_frame,text='Train')

        self.station_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.station_frame,text='Station')

        self.minimap_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.minimap_frame,text='Map')

        #########################################
        ######   Railway Monitor Screen    ######
        #########################################
        # self.monitor_Frame = ttk.Frame(self,height=768)
        # self.monitor_Frame.pack(fill=tk.X)
        # os.environ['SDL_WINDOWID'] = str(self.monitor_Frame.winfo_id())
        # os.environ['SDL_VIDEODRIVER'] = 'x11'
        # os.environ['SDL_VIDEODRIVER'] = 'windib'
        # self.master.bind("<Left>", self.dispatch_left_to_pygame)
        # self.master.bind("<Right>", self.dispatch_right_to_pygame)
        self.isRun = False

        ###### Train Parameter ######
        self.trainSpeed_label = ttk.Label(self.train_frame,text='Max Speed')
        self.trainSpeed_label.grid(row=0,column=0,padx=4,pady=4)
        self.trainSpeed = tk.StringVar(value='80')
        self.trainSpeed_entry = ttk.Entry(self.train_frame,textvariable=self.trainSpeed,font=('Verdana',16),width=5)
        self.trainSpeed_entry.grid(row=0,column=1,padx=4,pady=4)
        self.trainSpeed_unit = ttk.Label(self.train_frame,text='km/hr')
        self.trainSpeed_unit.grid(row=0,column=2,padx=4,pady=4)

        self.trainAcceleration_label = ttk.Label(self.train_frame,text='Acceleration')
        self.trainAcceleration_label.grid(row=1,column=0,padx=4,pady=4)
        self.trainAcceleration = tk.StringVar(value='10')
        self.trainAcceleration_entry = ttk.Entry(self.train_frame,textvariable=self.trainAcceleration,font=('Verdana',16),width=5)
        self.trainAcceleration_entry.grid(row=1,column=1,padx=4,pady=4)
        self.trainAcceleration_unit = ttk.Label(self.train_frame,text='km/hr/s')
        self.trainAcceleration_unit.grid(row=1,column=2,padx=4,pady=4)

        self.trainCapacity_label = ttk.Label(self.train_frame,text='Max Capacity')
        self.trainCapacity_label.grid(row=2,column=0,padx=4,pady=4)
        self.trainCapacity = tk.StringVar(value='400')
        self.trainCapacity_entry = ttk.Entry(self.train_frame,textvariable=self.trainCapacity,font=('Verdana',16),width=5)
        self.trainCapacity_entry.grid(row=2,column=1,padx=4,pady=4)
        self.trainCapacity_unit = ttk.Label(self.train_frame,text='passengers')
        self.trainCapacity_unit.grid(row=2,column=2,padx=4,pady=4)

        # self.trainNumber_label = ttk.Label(self.train_frame,text='Number of trains')
        # self.trainNumber_label.grid(row=0,column=3,padx=4,pady=4)
        # self.trainNumber = tk.StringVar(value='30')
        # self.trainNumber_entry = ttk.Entry(self.train_frame,textvariable=self.trainNumber,font=('Verdana',16),width=5)
        # self.trainNumber_entry.grid(row=0,column=4,padx=4,pady=4)
        # self.trainNumber_unit = ttk.Label(self.train_frame,text='trains')
        # self.trainNumber_unit.grid(row=0,column=5,padx=4,pady=4)

        self.trainDuration_label = ttk.Label(self.train_frame,text='Train Duration')
        self.trainDuration_label.grid(row=0,column=3,padx=4,pady=4)
        self.trainDuration = tk.StringVar(value='10')
        self.trainDuration_entry = ttk.Entry(self.train_frame,textvariable=self.trainDuration,font=('Verdana',16),width=5)
        self.trainDuration_entry.grid(row=0,column=4,padx=4,pady=4)
        self.trainDuration_unit = ttk.Label(self.train_frame,text='Minutes')
        self.trainDuration_unit.grid(row=0,column=5,padx=4,pady=4)

        self.trainStop_label = ttk.Label(self.train_frame,text='Stop times')
        self.trainStop_label.grid(row=1,column=3,padx=4,pady=4)
        self.trainStop = tk.StringVar(value='3')
        self.trainStop_entry = ttk.Entry(self.train_frame,textvariable=self.trainStop,font=('Verdana',16),width=5)
        self.trainStop_entry.grid(row=1,column=4,padx=4,pady=4)
        self.trainStop_unit = ttk.Label(self.train_frame,text='Minutes')
        self.trainStop_unit.grid(row=1,column=5,padx=4,pady=4)

        ###### Station Parameter ######
        self.numberStation_label = ttk.Label(self.station_frame,text='Number of Stations')
        self.numberStation_label.grid(row=0,column=0,padx=4,pady=4)
        self.numberStation = tk.StringVar(value=len(name))
        self.numberStation_entry = ttk.Entry(self.station_frame,textvariable=self.numberStation,font=('Verdana',14),width=3)
        self.numberStation_entry.grid(row=0,column=1,padx=4,pady=4)
        self.station_button = ttk.Button(self.station_frame,text='Apply',command=self.set_station)
        self.station_button.grid(row=0,column=2,padx=4,pady=4)

        self.name_label = ttk.Label(self.station_frame,text='Name')
        self.name_label.grid(row=1,column=0,padx=4,pady=4)
        self.position_label = ttk.Label(self.station_frame,text='Position')
        self.position_label.grid(row=2,column=0,padx=4,pady=4)
        self.arrivalrate_label = ttk.Label(self.station_frame,text='Arrival Rate')
        self.arrivalrate_label.grid(row=3,column=0,padx=4,pady=4)
        self.graph_label = ttk.Label(self.station_frame,text='Graph Results')
        self.graph_label.grid(row=4,column=0,padx=4,pady=4)

        self.name_var = []
        self.position_var = []
        self.arrivalrate_var = []
        self.graph_var = []
        self.name_entry = []
        self.position_entry = []
        self.arrivalrate_entry = []
        self.graph_check = []
        self.no_station = int(self.numberStation.get())
        for i in range(self.no_station):
            self.name_var.append(tk.StringVar(value=name[i]))
            self.name_entry.append(ttk.Entry(self.station_frame,textvariable=self.name_var[-1],font=('Verdana',14),width=4))
            self.name_entry[-1].grid(row=1,column=1+i,padx=4,pady=4)

            self.position_var.append(tk.StringVar(value=str(distance[i+1]-200)))
            self.position_entry.append(ttk.Entry(self.station_frame,textvariable=self.position_var[-1],font=('Verdana',14),width=4))
            self.position_entry[-1].grid(row=2,column=1+i,padx=4,pady=4)

            self.arrivalrate_var.append(tk.StringVar(value=str(0.1)))
            self.arrivalrate_entry.append(ttk.Entry(self.station_frame,textvariable=self.arrivalrate_var[-1],font=('Verdana',14),width=4))
            self.arrivalrate_entry[-1].grid(row=3,column=1+i,padx=4,pady=4)

            self.graph_var.append(tk.BooleanVar())
            self.graph_check.append(ttk.Checkbutton(self.station_frame,variable=self.graph_var[-1]))
            self.graph_check[-1].grid(row=4,column=1+i,padx=4,pady=4)
        
        ###### Minimap Parameter ######
        self.minimap = tk.Canvas(self.minimap_frame,height = 150)
        self.minimap.pack(fill=tk.X)
        self.minimap.create_line(50,55,950,55,width=5,fill='limegreen')
        self.minimap.create_line(50,65,950,65,width=5,fill='forestgreen')
        self.minimap_oval = []
        self.minimap_text = []
        self.minimap_train = []
        for i in range(self.no_station):           
            x = 50 + i*900/(self.no_station-1)
            self.minimap_oval.append(self.minimap.create_oval(x-10,50,x+10,70,fill='khaki',outline='maroon',width=3))
            name_str = name[i].split(' ')
            for j in range(len(name_str)):
                self.minimap_text.append(self.minimap.create_text(x,85+j*12,text=name_str[j]))
        self.minimap.bind("<Button-1>", self.gotoStation)
    
    def gotoStation(self,event):
        if event.y > 50 and event.y < 70 and self.isRun:
            for i in range(self.no_station):
                x = 50 + i*900/(self.no_station-1)
                if event.x > x-10 and event.x < x+10:
                    self.offset = -Station.stations[i].pos +450

    def set_station(self):
        for i in range(len(self.name_var)):
            self.name_entry[i].destroy()
            self.position_entry[i].destroy()
            self.arrivalrate_entry[i].destroy()
            self.graph_check[i].destroy()

        for i in self.minimap_oval:
            self.minimap.delete(i)
        for i in self.minimap_text:
            self.minimap.delete(i)

        self.name_var = []
        self.position_var = []
        self.arrivalrate_var = []
        self.graph_var = []
        self.name_entry = []
        self.position_entry = []
        self.arrivalrate_entry = []
        self.graph_check = []
        self.no_station = int(self.numberStation.get())
        for i in range(self.no_station):
            self.name_var.append(tk.StringVar())
            self.name_entry.append(ttk.Entry(self.station_frame,textvariable=self.name_var[-1],font=('Verdana',14),width=4))
            self.name_entry[-1].grid(row=1,column=1+i,padx=4,pady=4)

            self.position_var.append(tk.StringVar())
            self.position_entry.append(ttk.Entry(self.station_frame,textvariable=self.position_var[-1],font=('Verdana',14),width=4))
            self.position_entry[-1].grid(row=2,column=1+i,padx=4,pady=4)

            self.arrivalrate_var.append(tk.StringVar(value=str(0.1)))
            self.arrivalrate_entry.append(ttk.Entry(self.station_frame,textvariable=self.arrivalrate_var[-1],font=('Verdana',14),width=4))
            self.arrivalrate_entry[-1].grid(row=3,column=1+i,padx=4,pady=4)

            self.graph_var.append(tk.BooleanVar())
            self.graph_check.append(ttk.Checkbutton(self.station_frame,variable=self.graph_var[-1]))
            self.graph_check[-1].grid(row=4,column=1+i,padx=4,pady=4)

            x = 50 + i*900/(self.no_station-1)
            self.minimap_oval.append(self.minimap.create_oval(x-10,50,x+10,70,fill='khaki',outline='maroon',width=3))


    # def dispatch_left_to_pygame(self,event):
    #     if self.isRun:
    #         pgEvent = pygame.event.Event(pygame.KEYDOWN,{'key':pygame.K_LEFT})
    #         pygame.event.post(pgEvent)
    # def dispatch_right_to_pygame(self,event):
    #     if self.isRun:
    #         pgEvent = pygame.event.Event(pygame.KEYDOWN,{'key':pygame.K_RIGHT})
    #         pygame.event.post(pgEvent)

    def run_simulation(self):
        self.isRun = True
        print('running Railway Simulation')
        time_unit = self.timeOption.get()
        if time_unit == "hours":
            simulation_time = int(self.simtime.get())*3600
        elif time_unit == "minutes":
            simulation_time = int(self.simtime.get())*60
        elif time_unit == "seconds":
            simulation_time = int(self.simtime.get())*60
        current_sim_time = 0

        pygame.init()
        pygame.display.set_caption("Train Simulator")

        screen = pygame.display.set_mode((1024,700))
        self.offset = 0

        train_img = pygame.image.load('img/train.png').convert()
        train_img.set_colorkey((253,236,166))

        sky_img = pygame.image.load('img/sky.png').convert()

        Station.stations = []
        for i in range(self.no_station):
            Station.stations.append(Station(i,int(self.position_var[i].get())+400,self.name_var[i].get(),float(self.arrivalrate_var[i].get())))

        trains = []
        Train.capacity = int(self.trainCapacity.get())
        Train.max_speed = int(self.trainSpeed.get())*1000/3600
        Train.accel = int(self.trainAcceleration.get())*1000/3600
        Train.stop_time = int(self.trainStop.get())*60

        Depot.start = Depot(int(self.trainDuration.get()),trains,0,type='start')
        Depot.end = Depot(int(self.trainDuration.get()),trains,(int(self.position_var[-1].get())+1000),type='end')

        def draw_railway(screen,offset):
            railway = pygame.image.load('img/railway.png').convert()
            railway.set_colorkey((255,255,255))

            for i in range(-1,int((int(self.position_var[-1].get())+400)/scale/200)+5):
                if offset+40+200*i >= 1280:
                    break
                if offset+40+200*i > -200 and offset+40+200*i < 1280:
                    screen.blit(railway,(offset+40+200*i,400))
                    screen.blit(railway,(offset+40+200*i,480))

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
                        shift_speed = 10
                        # self.offset += 5
                    if event.key == pygame.K_RIGHT:
                        shift_speed = -10
                        # self.offset += -5
                    
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                if event.type == pygame.KEYUP:
                    shift_speed = 0

            if shift_speed != 0:
                self.offset += shift_speed

            screen.fill((255,255,255))
            screen.blit(sky_img,(0-20+self.offset*0.03,0))

            Depot.start.update(current_sim_time)
            Depot.end.update(current_sim_time)

            for i in range(self.no_station):
                Station.stations[i].update_platform(current_sim_time)
                Station.stations[i].draw(screen,self.offset)

            for i in self.minimap_train:
                self.minimap.delete(i)

            for train in trains:
                r = train.update_train(current_sim_time)
                if r == 'park':
                    trains.remove(train)
                else:
                    train.draw(screen,train_img,self.offset)

                    if train.state == 'stop' or \
                        (train.station_index == 0 and train.railway == 1) or\
                        (train.station_index == 12 and train.railway == 0):
                        x = 50+900/(self.no_station-1)*train.station_index
                    elif train.station_index >= self.no_station and train.railway == 1:
                        x = 50+900
                    elif train.station_index <= -1 and train.railway == 0:
                        x = 50
                    else:
                        x2 = Station.stations[train.station_index].pos
                        if train.railway == 0:
                            x1 = Station.stations[train.station_index+1].pos
                            x = 50+900/(self.no_station-1)*(train.station_index+1-(train.pos-x1)/(x2-x1))
                        else:
                            x1 = Station.stations[train.station_index-1].pos
                            x = 50+900/(self.no_station-1)*(train.station_index-1+(train.pos-x1)/(x2-x1))
                    if train.railway == 0:
                        y = 65
                    else:
                        y = 55
                    self.minimap_train.append(self.minimap.create_line(x-10,y,x+10,y,width=8,fill='midnightblue'))

            Depot.start.draw(screen,self.offset)
            Depot.end.draw(screen,self.offset)
            draw_railway(screen,self.offset)

            pygame.display.update()

            print("time:"+str(current_sim_time))
            current_sim_time = current_sim_time + 1    

            hh = current_sim_time//3600
            mm = (current_sim_time%3600)//60
            ss =  current_sim_time%60

            current_sim_time_str = '{0:02d}:{1:02d}:{2:02d}'.format(hh,mm,ss)
            self.curtime.set(current_sim_time_str)
            
            if current_sim_time >= update_show_time:
                update_show_time = update_show_time + show_speed
            simulation_Window.update()

        self.isRun = False

        linestyles = 5*['-']+5*['--']+5*['-.']+5*[':']
        legend = []
        plt.figure('All Station Platform 1')
        for i,s in enumerate(Station.stations):
            if self.graph_var[i].get():
                legend.append(s.name)
                plt.plot(range(len(s.queues_1)),s.queues_1,linestyle=linestyles[i])
        plt.legend(legend)
        
        plt.figure('All Station Platform ')
        for i,s in enumerate(Station.stations):
            if self.graph_var[i].get():
                plt.plot(range(len(s.queues_0)),s.queues_0,linestyle=linestyles[i])
        plt.legend(legend)

        for i,s in enumerate(Station.stations):
            print(self.graph_var[i].get())
            if self.graph_var[i].get():
                plt.figure(s.name)
                plt.plot(range(len(s.queues_1)),s.queues_1,linestyle=linestyles[i])
                plt.plot(range(len(s.queues_0)),s.queues_0,linestyle=linestyles[i])
                legend = ['Platform 1','Platform 2']
                plt.legend(legend)
        plt.show()

simulation_Window = RailwaySimulation(tk.Tk())
simulation_Window.mainloop()

pygame.quit()