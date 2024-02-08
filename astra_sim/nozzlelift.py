#solve nozzle lift
import numpy as np 

tol = 0.001                               #Tolerance for iterative guess
v = 5#3 #m/s              ASCENT RATE, SWEEP
m_p = 1.1 #kg                         PAYLOAD MASS
m_b = 0.6#0.35 #kg                           BALLOON MASS
WaterWeight = 44 #kg                    WATER WEIGHT OF K TANK TANK, FROM LINDE
WaterDensity= 997 #kg/m3
Vtank = WaterWeight/WaterDensity #m3     TANK VOLUME,  K cylinder (k type is 1.65ft3, S is 0.97ft3)
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


R = solveRatV(v=v,m = m_p)
V = 4/3 * np.pi * R**3
F_nozzle = (1.205 - 0.1786) * V * 9.81 - m_b * 9.81 #necklift does not account mass of payload
print(F_nozzle/9.81)