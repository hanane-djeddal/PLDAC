# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import random
import pandas as pd

a=np.array([[4,2],[8,2]])
b=np.array([2,2])
c=[1,1,1,1,2,8]
d=[[2,4],[],[]]
c+=d
indices=[i for i in range(5)]
random.shuffle(indices)
#print(indices)
e=np.random.choice(np.arange(1, 7), p=[0.1, 0.05, 0.05, 0.2, 0.4, 0.2])

df=pd.read_csv("traffictest.csv")
t=df.loc[df['Hour']==23,:].count()
cells=df['Hour'].unique()
print(df.count(),t,np.size(cells))
