# -*- coding: utf-8 -*-
"""
Created on Mon May 10 13:33:42 2021

@author: abc
"""

##WORKING CODE for temp

import cantera as ct
import numpy as np
import matplotlib.pylab as plt 
import sys
import csv

gas = ct.Solution('gri30.yaml')  

ifuel = gas.species_index('CH4')
io2 = gas.species_index('O2')
in2 = gas.species_index('N2')

Pin = 101325 
     
n = 25
phi = 1.0
Tin = np.zeros(n)    
air_n2_o2_ratio = 3.716
X = np.zeros(gas.n_species)     
su = np.zeros(n)


for i in range(1,25):
    Tin[i] = 288 + (700-288)*i/(n-1)
    stoich_o2 = 2
    X = np.zeros(gas.n_species) 
    X[ifuel] = phi
    X[io2] = stoich_o2
    X[in2] = stoich_o2*air_n2_o2_ratio

    gas.TPX = Tin[i], Pin, X
    gas()
    #initial_grid = 5*np.array([0.0,0.001,0.01,0.02,0.029,0.03],'d')/3
    width = 0.03
    loglevel = 1
    flame = ct.FreeFlame(gas,width=width)
    flame.set_refine_criteria(ratio=3,slope=0.07,curve=0.1)
    flame.solve(loglevel=loglevel,auto=True)
    su[i]=flame.u[0]
    print("flamespeed is: {:.2f} cm/s".format(su[i]))
plt.plot(Tin,su, c = 'red', marker = '^',LineWidth = 2)
plt.xlabel('Temperature in K')
plt.ylabel('Laminar Flame Speed in m/s')
plt.grid(axis = 'both')
plt.title('Laminar Flame Speed vs Temperature')


csv_file = 'LaminarFlameSpeed vs Temp.csv'
with open (csv_file,'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['T in K','Laminar Flame Speed'])
    for i in range (n):
        writer.writerow([Tin[i], su[i]])
print("the output file is written to", "%s"%(csv_file))
