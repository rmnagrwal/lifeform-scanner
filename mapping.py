# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 08:36:32 2020

@author: Raman Agarwal
"""


import matplotlib as plt 
import numpy as np
file1 = open('VIQuality.txt','r+')
allLines = file1.readlines()
file1.close()
height1 = (len(allLines))
width1 = (len(allLines[0].split()))
x=[]
# print(float(allLines[0].split()[0]))
for line in allLines:
    line1 = line.split()
    for value1 in line1:
        x.append(float(value1))

z = np.array(x).reshape(width1, height1)

# z.shape()
plt.image.imsave('name.png', z)
# plt.show()