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
To=0.24
max_iter=20
iter_converge=6


"""
Préparation du dataset   
fichier = open("BS_Locations/Lille_antenna_location.csv",'r')
fichier2 = open("BS_Locations/Lille_antenna_location2.csv",'w')        # On rajoute un tilde à la fin pour éviter d'écraser le fichier source en cas de bug
lignes = fichier.readlines()                # On parcours les lignes du fichier source
for ligne in lignes:
    ligneFinale = ligne.replace(';',', ')            # On remplace tout les espaces par groupe de 4 en tabulation
    fichier2.write(ligneFinale)             # On écrit la nouvelle ligne dans le nouveau fichier
                 
fichier.close()                     # Fermeture du fichier source
fichier2.close()    
"""       
df_geo=pd.read_csv("BS_Locations/Lille_antenna_location2.csv")

df_geo_norm=DCCA.normalize_distance(df_geo) #a que les deux colonnes X et Y sans ID

#Avec les heures 
"""
fichier = open("data/Lille/Lille.csv",'r')
fichier2 = open("data/Lille/Lille_traite.csv",'w')        # On rajoute un tilde à la fin pour éviter d'écraser le fichier source en cas de bug
lignes = fichier.readlines()                # On parcours les lignes du fichier source
for ligne in lignes:
    ligneFinale = ligne.replace(';',', ')            # On remplace tout les espaces par groupe de 4 en tabulation
    fichier2.write(ligneFinale) 
fichier.close()                     # Fermeture du fichier source
fichier2.close()
"""
df_traffic=pd.read_csv("data/Lille/Lille_traite.csv")

#Nr=df_geo_norm.count()[0]  #nombre des RRHs
RRH_ID= df_traffic['CellID'].unique()
Nr=np.size(RRH_ID)  # nbre de RRH dans données trafic < nbre RRHs dans geo données
r=[]
F=np.empty([Nr,Nt])
Fup=np.empty([Nr,Nt])
for i in range (Nr) :
    print("RRH = ",i,"/790")
    id=RRH_ID[i]
    trafic_RRH =df_traffic.loc[df_traffic['CellID']==id,:]
    for h in range(Nt):
        #print(     "H= ",h,"/24")
        if (h <10):
            sh='0'+str(h)
        else:
            sh=str(h)
        tu=0
        td=0
        nbr=0
        j=0
        for ind in (trafic_RRH.index.values):
            slot=trafic_RRH.iloc[j]
            if(slot[' TimeSlot'][12:14] == sh):
                trafic_RRH=trafic_RRH.drop([ind])
                nbr+=1
                td+=slot[' ByteDn']
                tu+=slot[' ByteUp'] 
                break;
            else:
                j+=1
        F[i][h]=td #/nbr
        Fup[i][h]=tu 
    r.append(DCCA.RRH(id,i,df_geo_norm.iloc[i,0],df_geo_norm.iloc[i,1],F[i]))





F_norm=DCCA.normalize_trafic(F)
T=DCCA.peak_tracking(CBBU,F_norm,r)  
W=DCCA.matriceComplementarite(r,CBBU,To)
P,l=DCCA.iterative_DCCA (r,F_norm,CBBU,max_iter,To,iter_converge)

""" affichage des clusters """
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
        plt.scatter(X[:,0],X[:,1])
    
"""
lescomp=np.array(lescomp)
print("K =",k,"\n",
      "max :",np.max(lescomp),"\n",
      "min :",np.min(lescomp),"\n",
      "moyenne :",np.mean(lescomp),"\n",
      "mediane :",np.median(lescomp),)
#plt.hist(lescomp,bins='auto')
"""