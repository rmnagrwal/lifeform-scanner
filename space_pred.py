from PIL import Image 
import numpy as np 
import pandas as pd

img = Image.open("map0.25.png") 
numpydata = np.asarray(img)

arr = numpydata.copy()

vege_df = pd.read_csv('vege.csv',header=None)
rain_df = pd.read_csv('rain.csv',header=None)
temp_df = pd.read_csv('temp.csv',header=None)
optical_df = pd.read_csv('optical.csv',header=None)

helper_df = pd.read_csv('helper.csv',header=None)

rain_land = helper_df*rain_df
optical_land = helper_df*optical_df
temp_land = helper_df*temp_df
vege_land = helper_df*vege_df

for i in range (helper_df.shape[0]):
    for j in range (helper_df.shape[1]):
        try:
            if 0.5<vege_land[j][i] and 1.641749188574094<temp_land[j][i]<26.505227476389237 and 0<optical_land[j][i]<0.5:
                arr[i,j] = np.array([255,255,255,255])
        except:
            pass

import matplotlib.pyplot as plt
plt.imsave('inter_map.png', arr)