# -*- coding: utf-8 -*-
"""
Created on Wed May 12 01:01:36 2021

@author: abc
"""
##WORKING HURRAY HURRAY ####
import cantera as ct
import numpy as np
import matplotlib.pylab as plt 
import sys
import csv

gas = ct.Solution('gri30.yaml')  

ifuel = gas.species_index('CH4')
io2 = gas.species_index('O2')
in2 = gas.species_index('N2')
n=5
m = 4      
Pin = np.zeros(n)  
Tin = np.zeros(m)
phi = 1.0

air_n2_o2_ratio = 3.716
X = np.zeros(gas.n_species)     
su = np.zeros((n,m))

for j in range(1,4):
    Tin[j] = 300 + (500-300)*j/(m-1) 
    for i in range(1,5):
        Pin[i] = 1013250 + (6*1013250-1013250)*i/(n-1)
        stoich_o2 = 2
        X = np.zeros(gas.n_species)
        X[ifuel] = phi
        X[io2] = stoich_o2
        X[in2] = stoich_o2*air_n2_o2_ratio

        gas.TPX = Tin[j], Pin[i], X
        gas()
    #initial_grid = 5*np.array([0.0,0.001,0.01,0.02,0.029,0.03],'d')/3
        width = 0.03
        loglevel = 1
        flame = ct.FreeFlame(gas,width=width)
        flame.set_refine_criteria(ratio=3,slope=0.1,curve=0.1)
        flame.solve(loglevel=loglevel,auto=True)
        su[i,j]=flame.u[0]
        print("flamespeed is: {:.2f} cm/s".format(su[i,j]))
        


plt.plot(Pin,su, c = 'red', marker = 'v',LineWidth = 2)
plt.xlabel('Pressures in Pa')
plt.ylabel('Laminar Flame Speed in m/s')
plt.title('Laminar Flame Speed vs Pressure')
