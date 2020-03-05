#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 16:58:33 2020
@author: h_djeddal

L'implementation de méthode de clustering des RRHs proposée dans ref1.

Implementation of RRHs-Clustering method proposed in ref1 
"""

import random
import math
import numpy as np

class RRH:
    def __init__(self,i,lat,lng,t=[]):
        self.lat=round(random.uniform(lat,lat+0.05),4)
        self.lng=round(random.uniform(lng,lng+0.05),4)
        self.id=i
        self.trafic=t
        self.peak=[]
    def setTrafic(self,t):
        self.trafic=t
    def setPeak(self,p):
        self.peak=p
       
def calcul_proba(C):
    proba=[]
    T=[]
    for i in range(len(C)):
        T+=C[i].peak
    longeur=len(T)
    for i in range(len(C[0].trafic)):
        p=T.count(i)/longeur
        if(p>0):
            proba.append(p)
    return proba

def entropie_shannon(p):
    s=0;
    for pi in p:
        s+= math.log(pi)*pi
    return (-s)

def capacity_utility(B,f):
    res=np.mean(f)/B
    l=-math.log1p(res)
    res=math.pow(res,l)
    return res
def aggregationTrafic(C):
    agg=np.zeros(len(C[0].trafic))
    for c in range(0,len(C)):
        agg+=C[c].trafic
    return agg
    
def complementarity(C,B):
    f=aggregationTrafic(C)
    p=calcul_proba(C)
    return (entropie_shannon(p)*capacity_utility(B,f))

def peak_tracking(B,F,r):
    T=[]    
    lesmax= np.amax(F,axis=1)
    minmax=min(lesmax)
    taux=min(int(B/2),minmax)
    #    methode 2: prendre maxligne +- delta=maxmax-minmax
    for i in range(len(F)):
        temp=[]
        for j in range(len(F[i])):
            if(F[i][j]>= taux):
                temp.append(j)
                T.append(j)
        r[i].setPeak(temp)
    return T
    

def distance(r1,r2):
    return math.sqrt((r1.lat-r2.lat)**2+(r1.lng-r2.lng)**2)

def matriceComplementarite(r,B,To):
    A=np.empty([len(r),len(r)])
    for i in range(len(r)):
        for j in range(len(r)):
            if((i!=j) and distance(r[i],r[j])<To):
                A[i][j]=complementarity(np.array([r[i],r[j]]),B)
            else:
                A[i][j]=0
    return A
def connectivity(C,W,rrh):
    res=0
    for ri in C:
        res+=W[ri.id][rrh.id]
    return res

def adjacent_clusters(P,W,rrh):
    AC=[]
    for C in P:
        if(connectivity(C,W,rrh) > 0):
            AC.append(C)
    return AC
def maxdist(C,rrh):
    m=0
    for ri in C:
        d=distance(rrh,ri)
        if(d>m):
            m=d
    return m
def evaluate(C,W,rrh,taux):
    c=connectivity(C,W,rrh)*math.log(taux/maxdist(C,rrh))
    return c

def DCCA(r,F,B,max_iter,taux):
    W=matriceComplementarite(r,B,taux)
    P=[]  #list of clusters
    labels=[]   #assigns a label of cluster to each rrh
    #step1: assign every rrh to a cluster
    for rrh in r:
        P.append([rrh])
        labels.append(rrh.id)
    #step2 : itere & cluster
    fin=False
    it=0
    while (not fin):
        it+=1
        change=False
        for rrh in r:
            maxvalue=0
            newC=[]
            AC=adjacent_clusters(P,W,rrh)
            for C in AC:
                value=evaluate(C,W,rrh,taux)
                if(value > maxvalue):
                    maxvalue=value
                    newC=C
            if(newC in P and labels[rrh.id] != P.index(newC)):
                newlabel=P.index(newC)
                oldlabel=labels[rrh.id] 
                labels[rrh.id] = newlabel  #update the label
                newC.append(rrh)   #add rrh to the new cluster
                P[newlabel]=newC   #update P
                P[oldlabel].remove(rrh)   #delete rrh from its old cluster
                change=True
        if(change == False or it== max_iter):
            fin=True
    return P,labels
        
        
def print_p(P):
    for C in P:
        print("Cluster : ")
        for r in C:
            print(r.id)
        
    
def normalize_trafic(F):
    nblig=len(F)
    nbcol=len(F[0])
    F_norm=np.empty([nblig,nbcol])
    for i in range (nblig):
        for j in range(nbcol):
            F_norm[i][j]=F[i][j]/np.sum(F[i])
    return F_norm