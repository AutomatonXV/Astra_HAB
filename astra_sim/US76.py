#WORK IN PROGRESS

import numpy as np
import PlotAssist, EZColors

#Consts
g0 = 9.80665 #m/s^2
M0 = 28.9644 #kg/kmol, from p.9 of the us76 doc
Rstar = 8.314 * 10 ** (3) #N.m/kmol-K

class Atmos:
    def __init__(self,):
        self.L_mb = np.array([-6.5,0,1,2.8,0,-2.8,-2]) #K/km
        self.H_b = np.array([0,11,20,32,47,51,71,84.8520]) #km

        self.T_mb = np.array([288.15,0,0,0,0,0,0,0])# %Kelvin
        self.P_b = np.array([101325,0,0,0,0,0,0,0])# %mb, mult by 100 for N/m2
        self.b = 0   #%subscript to index geopotential stuff
        self.Z0 = 0  #%km
        self.T = 0   #%K
        self.P = 0   #%Pa
        self.p = 0   #%kg/m3

        for b in range(0, np.size(self.L_mb)):
            nextb = b+1

            #set b dependent properties
            self.Z0 = self.H_b[b]
            self.Z = self.H_b[nextb]

            self.T_mb[nextb] = self.T_mb[b] + self.L_mb[b]*(self.Z-self.Z0)
            myLb = self.L_mb[b]
            myPb = self.P_b[b]
            myTmb = self.T_mb[b]

            resultP = 0
            if myLb != 0:
                bracket = myTmb / (myTmb + myLb*(self.Z-self.Z0))
                expo = 1000*g0 * M0 / (Rstar * myLb)
                resultP = myPb*bracket**expo
            else:
                resultP = myPb*np.exp(-1000*g0*M0*(self.Z-self.Z0)/(Rstar * myTmb))
            self.P_b[nextb] = resultP

    def findHb(self, Z):
        b = 0
        for Hb in self.H_b:
            if Hb > Z: return b-1, self.H_b[b-1]
            b +=1 
        
    
    def Calculate(self, Z): #Z in km
        if Z > 86: print("GREATER THAN 86 km NOT SUPPORTED"); return None 
        if Z < 0: print("below 0 alt not supported"); return None
        
        K = g0 * M0 / Rstar
        b,Z0 = self.findHb(Z)
        
        

        b = b-1
        self.T = self.T_mb[b+1] + self.L_mb[b+1] * (Z-Z0)
        
        myLb = self.L_mb[b+1]
        myPb = self.P_b[b+1]
        myTmb = self.T_mb[b+1]
        resultP = 0
        if myLb != 0:
            bracket = myTmb / (myTmb + myLb*(Z-Z0))
            expo = 1000*g0 * M0 / (Rstar * myLb)
            resultP = myPb*bracket**expo
        else:
            resultP = myPb*np.exp(-1000*g0*M0*(Z-Z0)/(Rstar * myTmb))
        self.P = resultP

        self.p = self.P * M0 / (Rstar * self.T);

        return self.P, self.T, self.p
    


myAtm = Atmos()
P10,T10,rho10 = myAtm.Calculate(Z=6)
print("P at 5", rho10)
# HPlot = PlotAssist.HigsPlot() #Plot contour
# Clr = EZColors.CustomColors(colorLabel = 'blue')
# HPlot.AxLabels(X = "Pressure (kPa)", Y = "Altitude (km)")
# HPlot.SetLim(Left = 0, Right = 100, Top = 35, Bottom = 0)

# Alt = np.linspace(0,35,100)
# Plist = np.zeros(np.size(Alt))
# Tlist = np.zeros(np.size(Alt))
# i = 0
# for Z in Alt:
#     P,T,p = myAtm.Calculate(Z)
#     Plist[i] = P
#     Tlist[i] = T
#     print(Z,P/1000)
#     i+=1

# HPlot.Plot((np.array(Plist)/1000,Alt), Color = Clr)

# HPlot.Finalize()
# HPlot.Show()


# HPlot = PlotAssist.HigsPlot() #Plot contour
# Clr = EZColors.CustomColors(colorLabel = 'blue')
# HPlot.AxLabels(X= "Temperature (K)", Y = "Altitude (km)")
# HPlot.SetLim(Left = 200, Right = 300, Top = 35, Bottom = 0)
# HPlot.Plot((np.array(Tlist),Alt), Color = Clr)
# HPlot.Finalize()
# HPlot.Show()

