# Astra_HAB
This is the HAB Predictor that I "borrowed" from U South hampton

Go into Astra_sim -> FlightPredictor.py. 
I have commented a bunch of long/lats of previously used or tentative launch locations
Use those as inputs for the latitude and longitude variable on line 55-56

SimNo is the monte carlo number of iterations. By default 10, for 10 runs
If you change your balloon, you might want to look into balloonModel
TrainEquivSphere is the payload size if it was a sphere, but this variable remains a a mystery to me
NozzleLift SHOULD BE the lift of the balloon including the balloon weight but excluding the balloon payload weight,
but through many trials it just doesnt do what it should do and i dont know what kind of black magic is involved here.
I recommend a value of 1.6-2, but I iteratively checked with NOAA and UKHAUS. A good rule of thumb is to use the Sondehub burst calculator
to get a  necklift value (= to nozzle lift)

If you want design charts, consult AscRateCalc_200g or _350g. These generate 3 plots drawing the edge limits of your
balloon flight by fixing ascent rates. Someone should double check these calculations, but I know with MRT flights that these graphs almost always works.

Run these predictorss, again andf again, they should all converge to the same spot more or less

 There was a certain level of self-hate to be able to use this predictor

 anyway, that' about it. See ya

"Sometimes in life, you gotta leave some mysteries unsolved." - arnab
