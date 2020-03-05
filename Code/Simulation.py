#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 11:57:01 2020

@author: h_djeddal

Simulation dans un environement restreint 
qu'on définie, afin de pouvoir detecter les critères
importants pour l'évaluation des clusters des RRHs. 

Pour un jour j, on suppose qu'on a déjà le traffic prédit
et on applique le clustering.
"""

import numpy as np
import matplotlib.pyplot as plt
import DCCA 
            

Nr=3  #nombre de RRHs
dt=1  #DeltaT = 1heure
Nt=int(24/dt)  #nombre de timespan  par jour
NBBU=2
CBBU=1
To=0.024
max_iter=20
lat=48.85
lng=2.34


"""
Génération de Fj : Fj a la structure [Nr,Nt] et contient le traffic prédit 
pour les RRHs à differents time spans (forcast hourly traffic for the next day).
methode : MuLSTM
Dans cette simulation, on génère nous même la matrice pour tester. 
""" 
F=np.empty([Nr,Nt])
F=np.array([[3,5,7,12,19,15,10,5,3,2,2,5,6,8,10,15,17,19,16,12,8,2,2,2],
           [3,4,6,11,18,15,11,8,7,5,5,5,4,4,3,3,3,2,2,3,3,2,2,2],
            [3,3,3,2,2,2,3,5,5,5,5,6,7,9,12,15,17,16,15,14,10,8,7,2]])
F_norm=DCCA.normalize_trafic(F)


# CREATION DES RRHs
r=[]   #liste des RRHs
for i in range(Nr):
    r.append(DCCA.RRH(i,lat,lng,F_norm[i]))
    
 
T=DCCA.peak_tracking(CBBU,F_norm,r)  

P,l=DCCA.DCCA(r,F_norm,CBBU,max_iter,To)

print(l)
for C in (P):
    print("Cluster")
    if(C != []):
        print(DCCA.complementarity(C,CBBU))
    for j in (C):
        print (j.id)

"""
lesmax=[]
lesmin=[]
nbcluster=[]

x=[(i/1000) for i in range(20,70)]
for i in range(50):
    P,l=DCCA.DCCA(r,F_norm,CBBU,max_iter,x[i])
    nbcluster.append(0)
    lesmax.append(0)
    lesmin.append(1000)
    for C in (P):
        if(C != []):
            nbcluster[i]+=1
            c=DCCA.complementarity(C,CBBU)
            if(c>lesmax[i]):
                lesmax[i]=c
            if(c<lesmin[i]):
                lesmin[i]=c

x=[i for i in range(50)]
for i in range(50):
    r=[]   #liste des RRHs
    for j in range(Nr):
        r.append(DCCA.RRH(j,lat,lng,F_norm[j])) 
    T=DCCA.peak_tracking(CBBU,F_norm,r)  
    P,l=DCCA.DCCA(r,F_norm,CBBU,10,To)
    nbcluster.append(0)
    lesmax.append(0)
    lesmin.append(1000)
    for C in (P):
        if(C != []):
            nbcluster[i]+=1
            c=DCCA.complementarity(C,CBBU)
            if(c>lesmax[i]):
                lesmax[i]=c
            if(c<lesmin[i]):
                lesmin[i]=c

plt.plot(x,nbcluster)
plt.xlabel('nombre d''itérations')
plt.ylabel('nombre de clusters crees')
plt.show()
plt.plot(x,lesmax)
plt.xlabel('nombre d''itérations')
plt.ylabel('complementarity max')
plt.show()
plt.plot(x,lesmin)
plt.xlabel('nombre d''itérations')
plt.ylabel('complementarity min')
plt.show()
"""