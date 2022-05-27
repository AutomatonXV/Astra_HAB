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
    outputFile = os.path.join('.','astra_sim','astra_output')
    Latitude = 45.962139
    Longitude = -74.173139
    Elevation = 300
    launch_datetime = datetime.now() + timedelta(days=1)

    #LAUNCH PARAMS
    SimNo = 10


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
                       balloonModel='TA200',
                       nozzleLift=2.0,                                # kg
                       payloadTrainWeight=0.200,                    # kg
                       parachuteModel='',
                       numberOfSimRuns=SimNo,
                       trainEquivSphereDiam=0.1,                    # m
                       floatingFlight=False,
                       excessPressureCoeff=1,
                       outputFile=outputFile,
                       debugging=True,
                       log_to_file=True)

    # simFlight.maxFlightTime = 5*60*60

    # Run the simulation
    simFlight.run()
    print("FINALIZED FLIGHT PREDICTION")
    Processor.drawAltimeter()
