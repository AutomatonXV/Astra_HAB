'''
Post Process into graphs
By Arnab Sinha (arnab.sinha@mail.mcgill.ca)
'''

import csv
import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
import PlotAssist, EZColors

class Processor:
    def __init__(self, SimulationNo,Lat,Long,Elev):
        self.SimNo = SimulationNo
        #zero ref
        self.Latitude = Lat
        self.Longitude = Long
        self.Elevation = Elev
        #dict of runs
        #   the structure is
        #   {
        #       [1] = {'Time' = [], 'Lat' = [], ...}
        # }
        self.Runs = {}
        

    def drawTrajectory2D(self,):
        self.__tabulateCSV()
        HPlot = PlotAssist.HigsPlot()
        for i in range(1, self.SimNo+1):
            #lat/long to cartesian:
            R = 6371 #km
            long = np.deg2rad(self.Runs[i]['Longitude'])
            lat = np.deg2rad(self.Runs[i]['Latitude'])
            long0 = np.deg2rad(self.Longitude)
            lat0 = np.deg2rad(self.Latitude)

            x = R * np.cos(lat) * np.cos(long)  ;   x0 = R * np.cos(lat0) * np.cos(long0)
            y = R * np.cos(lat) * np.sin(long)  ;   y0 = R * np.cos(lat0) * np.sin(long0) 
            z = R * np.sin(lat)

            Clr = EZColors.CustomColors(colorLabel = 'red')
            Clr.HueShift(Val = i*5)
            HPlot.AxLabels(X = "Longitude (km)", Y = "Latitude (km)")
            #HPlot.SetTicks('Y',0.0,1,0.2)
            HPlot.SetLim(Left = 0, Right = 35, Top = 35, Bottom = 0.0)
            #HPlot.SetTicks('Y',1,11,1)
            HPlot.Plot((x-x0, y-y0), Color = Clr)

        HPlot.Finalize()
        HPlot.Show()
        pass

    def drawTrajectory3D(self,):
        self.__tabulateCSV()
        #fig = plt.figure()
        #ax = plt.axes(projection = '3d')
        HPlot = PlotAssist.HigsPlot()
        HPlot.Mode3D()
        for i in range(1, self.SimNo+1):
            #lat/long to cartesian:
            R = 6371 #km
            long = np.deg2rad(self.Runs[i]['Longitude'])
            lat = np.deg2rad(self.Runs[i]['Latitude'])
            long0 = np.deg2rad(self.Longitude)
            lat0 = np.deg2rad(self.Latitude)

            x = R * np.cos(lat) * np.cos(long)  ;   x0 = R * np.cos(lat0) * np.cos(long0)
            y = R * np.cos(lat) * np.sin(long)  ;   y0 = R * np.cos(lat0) * np.sin(long0) 
            z = R * np.sin(lat)

            Clr = EZColors.CustomColors(colorLabel = 'red')
            Clr.HueShift(Val = i*5)
            
            HPlot.SetLim(Left = 0.0, Right = 35, Top = 35, Bottom = 0, Front = 15000, Back = 0.0)
            HPlot.AxLabels(X = "Distance (km)", Y = "Distance (km)", Z = "Elevation (km)")

            HPlot.Plot3D((x-x0,y-y0,self.Runs[i]['Elevation']/1000), Color = Clr)

        HPlot.Finalize()
        HPlot.Show()
        
        pass

    def drawAltimeter(self,):
        self.__tabulateCSV()
    
        HPlot = PlotAssist.HigsPlot()
        for i in range(1, self.SimNo+1):
            Clr = EZColors.CustomColors(colorLabel = 'red')
            Clr.HueShift(Val = i*5)
            HPlot.AxLabels(X = "Time (s)", Y = "Elevation (m)")
            #HPlot.SetTicks('Y',0.0,1,0.2)
            HPlot.SetLim(Left = 0.0, Right = 2500, Top = 20000, Bottom = 0.0)
            #HPlot.SetTicks('Y',1,11,1)
            HPlot.Plot((self.Runs[i]['Time'], self.Runs[i]['Elevation']), Color = Clr)

        HPlot.Finalize()
        HPlot.Show()

        pass
    
    def __tabulateCSV(self,):
        abspath = os.path.abspath('astra_sim\\astra_output\\out.csv')
        df = pd.read_csv(abspath, delimiter = ',')
        CurrentRun = 1
        Iter = 0
        AllRuns = {}; AllRuns = self.__newSection(1, AllRuns)
        for row in df.values:
            if Iter <= 1: Iter +=1 ; continue #skip header lines
            Run, Time, Lat, Long, Elev, Remark = self.__correctFormat(row)
            if Run != CurrentRun: AllRuns = self.__newSection(Run, AllRuns); CurrentRun +=1
            AllRuns[Run]['Time'].append(Time)
            AllRuns[Run]['Latitude'].append(Lat)
            AllRuns[Run]['Longitude'].append(Long)
            AllRuns[Run]['Elevation'].append(Elev)
            AllRuns[Run]['Remark'].append(Remark)
            
            Iter +=1 
        #finalize, into numpy array
        AllRuns = self.__finalizeSection(self.SimNo,AllRuns)
        self.Runs = AllRuns
        #print(self.Runs[3]['Latitude'])

    def __correctFormat(self, row):
        newRow = []
        pos = 0
        for val in row:
            pos +=1 
            filtered = val[1:]
            if pos != 6: filtered = np.float64(filtered.replace("'", ''))
            newRow.append(filtered)

        return int(newRow[0]), newRow[1], newRow[2], newRow[3], newRow[4], newRow[5]

    def __newSection(self, Run, AllRuns):
        AllRuns[Run] = {}
        AllRuns[Run]['Time'] = []
        AllRuns[Run]['Latitude'] = []
        AllRuns[Run]['Longitude'] = []
        AllRuns[Run]['Elevation'] = []
        AllRuns[Run]['Remark'] = []

        return AllRuns

    def __finalizeSection(self,Runs, AllRuns):
        for Run in range(1,Runs+1):
            AllRuns[Run]['Time'] = np.array(AllRuns[Run]['Time'])
            AllRuns[Run]['Latitude'] = np.array(AllRuns[Run]['Latitude'])
            AllRuns[Run]['Longitude'] = np.array(AllRuns[Run]['Longitude'])
            AllRuns[Run]['Elevation'] = np.array(AllRuns[Run]['Elevation'])
            AllRuns[Run]['Remark'] = np.array(AllRuns[Run]['Remark'])

        return AllRuns
            


        
        #rows = [list(row) for row in df.values]
        #print(rows)

