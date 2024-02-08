import numpy as np 
import PlotAssist, EZColors
from US76 import Atmos
myAtm = Atmos()             #P,T,rho = myAtm.Calculate(Z=0)

'''    LAUNCH PARAMETERS   '''
tol = 0.001                               #Tolerance for iterative guess
m_p = 1100/1000 #KG                              PAYLOAD MASS
v = 4.5 #m/s                                 ASCENT RATE DESIRED
P_SL = 101325 #Pa
T_SL = 298 #K 
'''     TANK INFORMATION      '''
WaterWeight = 44 #kg                       WATER WEIGHT OF K TANK TANK, FROM LINDE
WaterDensity= 997 #kg/m3
VTANK = WaterWeight/WaterDensity #m3     TANK VOLUME,  K cylinder (k type is 1.65ft3, S is 0.97ft3)
print("Tank volume is in m3 is"+ str(VTANK))

'''     BALLOON (HWOYEE) DATA FROM SCIENTIFICSALES      '''
M_B = np.array([200,300,350,600,800,1000,1200,1600,2000,3000])
D_BURST = np.array([2.4384, 3.3528, 3.6576, 4.8768, 5.7912, 6.4008, 6.7056, 8.2296, 9.144, 10.668])
R_BURST = D_BURST/2
V_BURST = 4/3 * np.pi * (R_BURST)**3

''' EXTRA METHODS'''
def AscEq(R, m_p,m_b, g0 = 9.81, Cd = 0.5, rho_Air = 1.205, rho_He = 0.1786):
    densDiff = rho_Air - rho_He
    Vol = 4/3 * (np.pi * R**3)
    Area = np.pi * R**2
    massMinus = -m_b - m_p 
    Second = densDiff * Vol + massMinus
    First = (2*g0) / (rho_Air * Cd * Area)

    Inside = (Second * First)
    if Inside < 0:
        return 0 #None
    else: 
        return np.sqrt(Inside)

def solveRatV(v, m_b, m_p, R0 = 1):
    #R0 is my guess, 1 meter
    #returns an R given a target v and mass specified
    guessR = R0
    scaleFactor = 1
    
    for i in range(0,1000):
    #while True:
        #print("plugging in", guessR)
        Vatguess = AscEq(R = guessR, m_p = m_p, m_b = m_b)
        #print(Vatguess - v)
        if np.abs(Vatguess - v) > tol:
            #need to keep looking
            sig = (v - Vatguess) / np.abs(Vatguess - v)
            err = np.abs(v-Vatguess)/v
            # #if sig is neg, vAtguess is greater (overshot)
            # #jump by an increment to the next guess
            guessR = guessR + scaleFactor*err*sig 
            #guessR = guessR + scaleFactor * sig*tol
            scaleFactor = scaleFactor*0.9
        else:
            #found R
            return guessR

def solveMaxAlt(V1, V2, Z0 = 50):
    #V1 is the launch volume, V2 is the burst volume, Z0 is guess 
    P1,T1,_ = myAtm.Calculate(Z=0)
    #Eq is P1 V1 / T1 = P2 V2 / T2
    #Re-arrange to k = P2/T2 = P1/T1 . V1/V2
    Zinc = 5; 
    Zdir = -1
    while True:
        P2,T2,_ = myAtm.Calculate(Z0)
        RHS = (P1/T1) * (V1/V2)
        LHS = P2/T2
        
        #print("Trying at "+str(Z0)+ " km,  LHS vs RHS is"+ str(LHS)+ " : "+str(RHS))
        if (np.abs(LHS-RHS))/RHS < tol:
            return Z0

        if (LHS - RHS > 0 ) and (Zdir<0): Zdir = 1; Zinc = Zinc/2  #going too low, need to go up
        elif (LHS - RHS < 0) and (Zdir>0): Zdir = -1; Zinc = Zinc/2
        Z0 += Zdir * Zinc

''' CALCULATION START'''



#GET MAX ALT
ZMaxList = np.zeros(np.size(V_BURST))
for i in range(0,np.size(V_BURST)):
    #COMPUTE V_SL, THE VOLUME OF BALLOON AT LAUNCH FOR A TARGETED ASCENT RATE v
    R_SL = solveRatV(v, M_B[i]/1000, m_p)
    V_SL = 4 / 3 * np.pi * R_SL ** 3

    V2 = V_BURST[i]
    ZMaxList[i] = solveMaxAlt(V_SL, V2)
    
#NOW POLYFIT
M_RANGE = np.linspace(0,3000,1000)
COE = np.polyfit(M_B,ZMaxList,2)
#CURVE = np.poly1d(COE)
FIT = np.polyval(COE,M_RANGE)

COE_D = np.polyfit(M_B, D_BURST,2)
FIT_D = np.polyval(COE_D, M_RANGE)

HPlot2 = PlotAssist.HigsPlot() #Plot contour
Clr = EZColors.CustomColors(colorLabel = 'blue')
Clr2 = EZColors.CustomColors(colorLabel = 'red')

HPlot2.AxLabels(X = "Balloon Size (g)", Y = "Burst Diameter")
HPlot2.SetLim(Left = 0, Right = 3000, Top =15, Bottom = 0)
HPlot2.Plot((M_RANGE, FIT_D), Color = Clr, LineStyle = '--')
HPlot2.plt.scatter(M_B, D_BURST)
HPlot2.Finalize()
HPlot2.Show()



HPlot = PlotAssist.HigsPlot() #Plot contour
Clr = EZColors.CustomColors(colorLabel = 'blue')
Clr2 = EZColors.CustomColors(colorLabel = 'red')

HPlot.AxLabels(X = "Balloon Size (g)", Y = "Estimated Burst Alt. (km)")
HPlot.SetLim(Left = 0, Right = 3000, Top = 40, Bottom = 0)
HPlot.Plot((M_RANGE, FIT), Color = Clr, LineStyle = '--')
HPlot.plt.scatter(M_B, ZMaxList)
HPlot.Finalize()
HPlot.Show()
