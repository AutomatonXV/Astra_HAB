from multiprocessing.dummy import Array
from tkinter.tix import Select
from PostProcessing import Processor
import numpy as np
import csv 
import os

Latitude = 45.990972
Longitude = -74.117139
Elevation = 280
SimNo = 10
RepresentativeRun = 1 #choose which run to export
Post = Processor(SimNo, Latitude, Longitude, Elevation)
RunData = Post.getData() #starts at 1

#methods
#YOU CANNOT AVERAGE VALUES, THEY HAVE DIFFERENT LENGTHS
# def averageArrays(Arrays):
#     #arrays is a dict containing all the arrays
#     Total = len(Arrays)
#     AvgDict = {}
#     #create the avg dict with keys corresponding
#     for arrName in Arrays[1]: 
#         sizeArray = len(Arrays[1][arrName])
#         AvgDict[arrName] = np.zeros(shape=(sizeArray))
        
#     for keys in AvgDict:
#         #avg = AvgDict[keys]
#         print(keys)
#         for run in Arrays: #go through each run
#             myvals = Arrays[run][keys] #grab the array of the corresponding key
#             AvgDict[keys]= AvgDict[keys] + myvals
#         #divide by the total number of values
#         AvgDict[keys]/Total
    
#     return AvgDict


    

#export code
with open(os.path.abspath('astra_sim\\astra_output\\Astra_Launch1.csv'), 'w') as f:
    writer = csv.writer(f)
    SelectData = RunData[RepresentativeRun]
    Rows = len(SelectData['Time'])
    for i in range(0,Rows):
        rowStr = []
        for labels in SelectData:
            if labels == 'Remark': continue 
            rowStr.append(str(SelectData[labels][i]))
        writer.writerow(rowStr)
