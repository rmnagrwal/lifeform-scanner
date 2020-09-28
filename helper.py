import pandas as pd
import numpy as np

df = pd.read_csv('vege.csv',header=None)
df_copy = df.copy()

for i in range (df.shape[0]):
    for j in range (df.shape[1]):
        if df[j][i] == 99999:
            df_copy[j][i] =0
        else:
            df_copy[j][i] =100
            
arr = np.array(df_copy)

import matplotlib.pyplot as plt
plt.imsave('base_map.png', arr)

for i in range (df.shape[0]):
    for j in range (df.shape[1]):
        if df[j][i] == 99999:
            df[j][i] =np.nan
        else:
            df[j][i] =1

df.to_csv('helper.csv',index=None)