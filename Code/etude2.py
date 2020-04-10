#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 16:24:58 2020

@author: h_djeddal
"""

import numpy as np
import matplotlib.pyplot as plt
import DCCA 
import pandas as pd
from datetime import datetime as dt
import math



dt=1  #DeltaT = 1heure
Nt=int(24/dt)  #nombre de timespan  par jour
NBBU=2
CBBU=1
To=0.14
max_iter=20
iter_converge=6


"""
Préparation du dataset   
"""
fichier = open("BS_Locations/Lille_antenna_location.csv",'r')
fichier2 = open("BS_Locations/Lille_antenna_location2.csv",'w')        # On rajoute un tilde à la fin pour éviter d'écraser le fichier source en cas de bug
lignes = fichier.readlines()                # On parcours les lignes du fichier source
for ligne in lignes:
    ligneFinale = ligne.replace(';',', ')            # On remplace tout les espaces par groupe de 4 en tabulation
    fichier2.write(ligneFinale)             # On écrit la nouvelle ligne dans le nouveau fichier
                 
fichier.close()                     # Fermeture du fichier source
fichier2.close()           
df_geo=pd.read_csv("BS_Locations/Lille_antenna_location2.csv")

df_geo_norm=DCCA.normalize_distance(df_geo)
"""
Construction de la matrice F de traffic forcast à partir d'un dataset de LTE
"""
"""  En utilisant les Cells
df_traffic=pd.read_csv("smalltraffictest.csv")
cells=df_traffic['CellName'].unique()
Nr=np.size(cells)
F=np.empty([Nr,Nt])
for i in range(Nr):
    for h in range(24):
        F[i][h]=(df_traffic.loc[(df_traffic['CellName']==cells[i]) & (df_traffic['Hour']==h),:])['Traffic'].mean()
"""
#Avec les heures 
df_traffic=pd.read_csv("traffictest.csv")
Nr=df_geo_norm.count()[0]  #nombre des RRHs
F=np.empty([Nr,Nt])
for h in range(24):
    fh=np.array((df_traffic.loc[(df_traffic['Hour']==h),:])['Traffic'])
    for i in range(Nr):
        F[i][h]=fh[i]


r=[]
for i in range(Nr):
    r.append(DCCA.RRH(i,df_geo_norm.iloc[i,0],df_geo_norm.iloc[i,1],F[i]))

F_norm=DCCA.normalize_trafic(F)
T=DCCA.peak_tracking(CBBU,F_norm,r)  
W=DCCA.matriceComplementarite(r,CBBU,To)
P,l=DCCA.iterative_DCCA (r,F_norm,CBBU,max_iter,To,iter_converge)

"""affichage des clusters"""
k=0
lescomp=[]
for C in P:
    if (C!=[]):
        k+=1
        lescomp.append(DCCA.complementarity(C,CBBU))
        X=np.empty([len(C),2])
        for i in range(len(C)):
            X[i][0]=C[i].lat
            X[i][1]=C[i].lng
        #plt.scatter(X[:,0],X[:,1])
lescomp=np.array(lescomp)
print("K =",k,"\n",
      "max :",np.max(lescomp),"\n",
      "min :",np.min(lescomp),"\n",
      "moyenne :",np.mean(lescomp),"\n",
      "mediane :",np.median(lescomp),)
#plt.hist(lescomp,bins='auto')