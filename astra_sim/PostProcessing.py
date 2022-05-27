'''
Post Process into graphs
By Arnab Sinha (arnab.sinha@mail.mcgill.ca)
'''

import csv
import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt


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
        

    def drawTrajectory(self,):
        pass

    def drawAltimeter(self,):
        self.__tabulateCSV()
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
        self.Runs = AllRuns
        print(self.Runs[3]['Latitude'])

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

            


        
        #rows = [list(row) for row in df.values]
        #print(rows)

from PostProcessing import Processor
Grapher = Processor(10,0,0,0)
Grapher.drawAltimeter()
