# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 20:19:37 2021

@author: Vanchhit Kumar Dubey
"""

import cantera as ct
import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np
import csv

gas = ct.Solution('USC.yaml') #for getting mechanism
gas()


#Initial temperatures
Tmin = 0.6 # initial range of 1000/T
Tmax = 0.8 # final range
npoints = 20 #Number of points
nt = 100000
dt = 1.e-6

#Storage
#Temperature storage variables
Ti = np.zeros(npoints,'d') 
Ti2 = np.zeros(npoints,'d') #final temperature
#The initial storage variable become case dependent
tim = np.zeros(nt,'d')
temp_cas = np.zeros(nt,'d')
dtemp_cas = np.zeros(nt-1,'d')
#Additional storage variables for autoignition and mass fraction
Autoignition_cas = np.zeros(npoints,'d')
FinalTemp_cas = np.zeros(npoints,'d')
mfrac_cas = np.zeros([npoints,gas.n_species],'d')
                     
#Loop over initial conditions
for j in range(npoints):
    Ti2[j] = Tmin + (Tmax - Tmin)*j/(npoints - 1)
    Ti[j] = 1000/Ti2[j]

#Set gas state, at stoichiometry
    gas.TPX = Ti[j], 10*101325, 'CH4:0.8,O2:1,N2:3.76'
#Create the ideal batch reactor
    r = ct.IdealGasReactor(gas)

    sim = ct.ReactorNet([r])

# Initial simulation time
    time = 0.0
#Loop for nt time steps of dt seconds.
    for n in range(nt):
        time += dt
        sim.advance(time)
        tim[n] = time
        temp_cas[n] = r.T
    mfrac_cas[j][:] = r.thermo.Y



# Get autoignition timing
    Dtmax = [0,0.0]
    for n in range(nt-1):
        dtemp_cas[n] = (temp_cas[n+1]-temp_cas[n])/dt
        
        if (dtemp_cas[n]>Dtmax[1]):
            Dtmax[0] = n
            Dtmax[1] = dtemp_cas[n]
              

# Local print
    Autoignition = (tim[Dtmax[0]]+tim[Dtmax[0] + 1])/2.
    print ('For '+str(Ti[j]) +', Autoignition time = (s)' + str(Autoignition))
# Posterity
    Autoignition_cas[j] = Autoignition*1000 #ms
    FinalTemp_cas[j] = temp_cas[nt-1]


# writing the  output CSV file for importing into Excel
csv_file = 'Phi-0.5_P-10_Trange_UV.csv'
with open(csv_file, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Auto ignition time','Final Temperature'] + gas.species_names)

    for i in range(npoints):
        writer.writerow(['cas Ti = ', Ti[j]])
        writer.writerow([Autoignition_cas[i], FinalTemp_cas[i]] +

        list(mfrac_cas[i,:]))
print('output written to' +(csv_file))
m, b = np.polyfit(Ti2,Autoignition_cas,1)


# creaating plots for an specific pressure (Actual plot for varying pressure is shown using MATLAB)
plt.figure(0)
plt.plot(Ti2,Autoignition_cas, '^', color = 'orange')
plt.xlabel(r'Temp in [1000/K]', fontsize=20)
plt.ylabel("Autoignition [ms]")
plt.title(r'Autoignition of $CH_{4}$ + Air mixture at $\Phi$ = 0.8, and P = 10 bar',fontsize=22,horizontalalignment='center')
plt.axis([0.60,0.90,0.0,100.0])
plt.plot(Ti2,m*Ti2+b, color = 'blue')
plt.grid()
plt.show()