"""
Flight Predictor (Astra Simulator, UofSouthHampton)
Launch Site: St-Adel, QC.
"""
import os

import logging
import numpy as np
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":

    from datetime import datetime, timedelta
    from astra.simulator import *
    from PostProcessing import Processor
    #ENVIRO PARAMS    
    #39.64866115419141, -121.64503100860261
    #45.61533578362935, -73.71145897397793
    outputFile = os.path.join('.','astra_sim','astra_output')
    # NORAD ALTERNATE
    # Latitude = 45.938142185048434
    # Longitude = -74.3146341884165
    # CHANTECLER
#45.99097, -74.11714

    #THE PIONEERS
    #45.77840892738032, -73.35713692500629, 8 meters

    #PARK LAMBTON
    #45.12416763373802, -73.99752331434091, 39m

    #DRUMMOND 
    #45.41582212267562, -72.68475367380931, 118

    #ST BERNARD
    #45.04630699636315, -73.43415965812812, 59m

    #st-adel
    #45.962139, -74.173139 #371,

    #parking lot near st-adel, p'tit train du nord
    #45.99097, -74.11714


    #park duquette
    #45.84896333976364, -73.98573911636356

    #Southern launch
    #45.29379729119799, -73.11108997929406

    MASS_Balloon = 0.2 #kg 0.2 was prev config
    MASS_Payload = 0.8 #kg 0.582 was prev config
    MASS_tot = MASS_Balloon + MASS_Payload

    Latitude = 45.29379729119799 
    Longitude = -73.11108997929406
    Elevation = 10
    TerminateAlt = 3000 #in meters, otherwise set to None
    #launch_datetime = datetime.now() + timedelta(days=0, hours =0)
                                #year/month/day/hour (hour is +4h )
    launch_datetime = datetime(2023,11,18,14)

    #LAUNCH PARAMS
    SimNo = 10

    #Post
    Post = Processor(SimNo, Latitude, Longitude, Elevation, TermAlt = TerminateAlt)

    np.random.seed(62)
    
    simEnvironment = forecastEnvironment(launchSiteLat=Latitude,      # deg
                                         launchSiteLon= Longitude,     # deg
                                         launchSiteElev=Elevation,           # m
                                         dateAndTime=launch_datetime,
                                         forceNonHD=True,
                                         debugging=True)

    # Launch setup
    simFlight = flight(environment=simEnvironment,
                       balloonGasType='Helium',
                       balloonModel='HW200',#'TA350',
                       nozzleLift= 2,#2,                                # kg USE NOZZLELIFT.PY CODE
                       payloadTrainWeight=MASS_tot,                    # kg, THIS IS TOTAL PAYLOAD + BALLOON (i.e 0.558+0.2 kg)
                       parachuteModel='IntStar',
                       numberOfSimRuns=SimNo,
                       trainEquivSphereDiam=0.3059,                    # m
                       floatingFlight=False,
                       excessPressureCoeff=1,
                       outputFile=outputFile,
                       debugging=True,
                       log_to_file=True)

    # simFlight.maxFlightTime = 5*60*60

    # Run the simulation
    simFlight.run()
    print("FINALIZED FLIGHT PREDICTION")
    #Post.drawTrajectory2D()
    Post.drawTrajectory3D()
    Post.drawAltimeter()
