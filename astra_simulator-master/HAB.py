"""
McGill MRT HAB Launch, 2022/05/14
"""
import logging
import numpy as np
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    from datetime import datetime, timedelta
    from astra.simulator import *

    np.random.seed(62)

    # Environment parameters
    # Launch site: Daytona Beach, FL
    #        time: tomorrow, this time
    launch_datetime = datetime.now() + timedelta(days=1)
    simEnvironment = forecastEnvironment(launchSiteLat=45.962139,      # deg
                                         launchSiteLon= -74.173139,     # deg
                                         launchSiteElev=300,           # m
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
                       numberOfSimRuns=10,
                       trainEquivSphereDiam=0.1,                    # m
                       floatingFlight=False,
                       excessPressureCoeff=1,
                       outputFile=os.path.join('.', 'astra_output'),
                       debugging=True,
                       log_to_file=True)

    # simFlight.maxFlightTime = 5*60*60

    # Run the simulation
    simFlight.run()
