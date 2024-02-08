#its contouring time

#SOLVE V IN FUNCTION OF R
import numpy as np 
import PlotAssist, EZColors
#pip install matplotlib-label-lines

tol = 0.001                               #Tolerance for iterative guess
m_p = np.array([.25,.5,.75,1,1.3])#np.array([0.588, .844])#np.arange(0.5,0.8,.05)#np.array([0.582]) #kg             PAYLOAD MASS
v = np.arange(0,7,.25) #m/s              ASCENT RATE, SWEEP
m_b = 0.35 #kg                           BALLOON MASS
Vtank = 0.961/35.315 #m3  (from 0.961ft3)       TANK VOLUME, PRAXAIR, S cylinder

R_Burst = 2.0574#(meters)
V_Burst = 4/3 * (np.pi * R_Burst**3)

Patm = 14.6959 #psi

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


def solveRatV(v, m, R0 = 1):
    #R0 is my guess, 1 meter
    #returns an R given a target v and mass specified
    guessR = R0
    scaleFactor = 1
    
    for i in range(0,1000):
    #while True:
        #print("plugging in", guessR)
        Vatguess = AscEq(R = guessR, m_p = m, m_b = m_b)
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


Rinits = [] #list of list of Rlists
HPlot = PlotAssist.HigsPlot() #Plot contour
Clr = EZColors.CustomColors(colorLabel = 'blue')
HPlot.AxLabels(X = "Ascent Rate (m/s)", Y = "Required Pressure (psi)")
HPlot.SetLim(Left = 1, Right = 6, Top = 2000, Bottom = 0)

for m in m_p:
    Rlist = np.full_like(v,0) #m              BALLOON RADIUS
    vindex = 0
    for vi in v:
        print("running", vi)
        Rlist[vindex] = solveRatV(vi,m)
        vindex +=1 

    V_fill = 4/3 * (np.pi) * (Rlist)**3
    Preq =  V_fill * Patm/ Vtank
    print("MY R LIST", Rlist)
   
    HPlot.Plot((v, Preq), Label = "$m_\mathrm{payload}$ = "+"{:.0f}".format(1000*m)+" g",Color = Clr)
    Clr.HueShift(Percent = 10/100)
    
    Rinits.append(Rlist)
    #to csv
    np.savetxt("ascrate",v,delimiter = ",")
    np.savetxt("preq", Preq, delimiter = ",")


#past data
#HPlot.plt.scatter(1.3,930, marker = 'x', c = (0,0.8,1),s = 25)
#HPlot.plt.scatter(4.88,1257, marker = 'x', c = (1,0,0),s = 75)

HPlot.ax.legend(frameon = False)
HPlot.Finalize()
HPlot.Show()



Clr = EZColors.CustomColors(colorLabel = 'blue')
minP = 0; maxP = 3000
H2 = PlotAssist.HigsPlot()
#H2.AxLabels(X = 'Delta Pressure (Psi)', Y = 'Initial Diameter (m)')
H2.AxLabels(X = 'Ascent Rate (m/s)', Y = 'Initial Diameter (m)')
#H2.SetLim(Left = 0, Right = 2000, Bottom = 0, Top = 3)
H2.SetLim(Left = 1, Right = 6, Bottom = 0, Top = 2.5)
rindex = 0
for myR in Rinits:
    #H2.Plot((Preq, 2*myR), Label = "m = "+"{:.0f}".format(1000*m_p[rindex])+"g", Color= Clr)
    H2.Plot((v, 2*myR), Label = "$m_\mathrm{payload}$ = "+"{:.0f}".format(1000*m_p[rindex])+" g", Color= Clr)
    Clr.HueShift(Percent = 10/100)

    rindex +=1
H2.plt.axhline(y = 2*R_Burst,label = 'Burst Diameter', xmin = 0, xmax = maxP, linestyle = '-.', color = 'k')
#H2.plt.axhline(y = 2*R_Nominal, xmin = 0, xmax = maxP, linestyle = '--')
H2.plt.axhline(y= 1.83,label = 'Regulation Limit', xmin =0,xmax = maxP, linestyle = '--', color = 'k')
H2.ax.legend(frameon = False)
#H2.ax.legend(['Initial Diameter', 'Burst Diameter', 'Regulation Limit'],frameon = False)
H2.Finalize()
H2.Show()




#Want to find max altitude
from US76 import Atmos
myAtm = Atmos()
#P,T,rho = myAtm.Calculate(Z=0)

P0,T0,rho0 = myAtm.Calculate(Z=0)
V1 = V_Burst

HPlot = PlotAssist.HigsPlot() #Plot contour
Clr = EZColors.CustomColors(colorLabel = 'blue')
HPlot.AxLabels(X = "Ascent Rate (m/s)", Y = "Max. Altitude (km)")
HPlot.SetLim(Left = 1, Right = 6, Top = 30, Bottom = 0)

Ri = 0
for R in Rinits:
    #R0 is a list of R0's
    R0 = np.array(R)
    V0 = 4/3 * np.pi * R0**3
    LeftK = (P0/T0) * (V0 / V1) #* (1/rho0)
    fullZ = np.zeros(np.size(LeftK))
    #print("my left K", LeftK)
    #print("my full Z", fullZ)

    Ki = 0 #index
    for K in LeftK:
        if K < 0 or np.isnan(K): continue #ignore exceptions

        eps = 0.01
        GuessZ = 0 #km
        
        while True:
            Pg, Tg, rhog = myAtm.Calculate(Z=GuessZ)
            newK = Pg/Tg #* (1/rhog)
            relErr = np.abs((K - newK))/(K) *100
            #escape condition
            if relErr < eps: 
                #print(" For k = ", K, "Found k", newK,"at Z =", GuessZ, "with error", relErr)
                fullZ[Ki] = GuessZ
                break
            GuessZ += eps/10
            if GuessZ > 70: break

        Ki+=1
    HPlot.Plot((v, fullZ), Label = "$m_\mathrm{payload}$ = "+"{:.0f}".format(1000*m_p[Ri])+" g", Color= Clr)
    Clr.HueShift(Percent = 10/100)
    Ri+=1
    #print("final full z", fullZ)


HPlot.ax.legend(frameon = False)
HPlot.Finalize()
HPlot.Show()

