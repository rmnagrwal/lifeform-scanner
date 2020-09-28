import pandas as pd
import numpy as np

main_df = pd.read_csv('hare.csv')
main_df = main_df.dropna()

main_df['day'] = main_df['day'].astype(int).astype(str)
main_df['month'] = main_df['month'].astype(int).astype(str)
main_df['year'] = main_df['year'].astype(int).astype(str)
main_df = main_df.reset_index(drop=True)

temp_df = pd.read_csv('air_temp.csv')
temp_df = temp_df.dropna()
temp_df['measured_on'] = temp_df['measured_on'].astype(str)
temp_df['measured_on'] = temp_df['measured_on'].apply(lambda x: str(int(x[3:5]))+'-'+str(x[6:]))
temp_df = temp_df.set_index('measured_on')

soil_temp_df = pd.read_csv('soil_temp.csv')
soil_temp_df = soil_temp_df.dropna()
soil_temp_df['measured_on'] = soil_temp_df['measured_on'].astype(str)
soil_temp_df['measured_on'] = soil_temp_df['measured_on'].apply(lambda x: str(int(x[3:5]))+'-'+str(x[6:]))
soil_temp_df = soil_temp_df.set_index('measured_on')

rain_df = pd.read_csv('precipitation.csv')
rain_df = rain_df.dropna()
rain_df['measured_on'] = rain_df['measured_on'].astype(str)
rain_df['measured_on'] = rain_df['measured_on'].apply(lambda x: str(int(x[3:5]))+'-'+str(x[6:]))
rain_df = rain_df.set_index('measured_on')

aerosol_df = pd.read_csv('aerosol.csv')
aerosol_df = aerosol_df.dropna()
aerosol_df['measured_on'] = aerosol_df['measured_on'].astype(str)
aerosol_df['measured_on'] = aerosol_df['measured_on'].apply(lambda x: str(int(x[3:5]))+'-'+str(x[6:]))
aerosol_df = aerosol_df.drop_duplicates(subset=['measured_on','latitude', 'longitude'])
aerosol_df = aerosol_df.set_index('measured_on')

from math import cos, asin, sqrt

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def closest(data, v):
    return min(data, key=lambda p: distance(v['decimalLatitude'],v['decimalLongitude'],p['latitude'],p['longitude']))

for i in range (main_df.shape[0]):
    time = main_df.iloc[i][5] + '-' + main_df.iloc[i][6]
    v = main_df.iloc[i][['decimalLatitude','decimalLongitude']].to_dict()
    
    try:
        time_rain = rain_df.loc[time]
        rain_arr = time_rain[['latitude','longitude']].to_dict('records')
        closest_rain_point = closest(rain_arr, v)
        rain = time_rain[time_rain['latitude']==closest_rain_point['latitude']]['precipitation monthlies'][0]
        main_df.at[i, 'rain'] = rain
    except:
        pass
    
    try:
        time_temp = temp_df.loc[time]
        temp_arr = time_temp[['latitude','longitude']].to_dict('records')
        closest_temp_point = closest(temp_arr, v)
        temp = time_temp[time_temp['latitude']==closest_temp_point['latitude']]['average temp (deg C)'][0]
        main_df.at[i, 'temp'] = temp
    except:
        pass
    
    try:
        time_soil_temp = soil_temp_df.loc[time]
        soil_temp_arr = time_soil_temp[['latitude','longitude']].to_dict('records')
        closest_soil_temp_point = closest(soil_temp_arr, v)
        soil_temp = time_soil_temp[time_soil_temp['latitude']==closest_soil_temp_point['latitude']]['average temp (deg C)'][0]
        main_df.at[i, 'soil_temp'] = soil_temp
    except:
        pass
    
    try:
        time_aerosol = aerosol_df.loc[time]
        aerosol_arr = time_aerosol[['latitude','longitude']].to_dict('records')
        closest_aerosol_point = closest(aerosol_arr, v)
        optical_thickness = time_aerosol[time_aerosol['latitude']==closest_aerosol_point['latitude']]['optical thickness'][0]
        transmission_percent = time_aerosol[time_aerosol['latitude']==closest_aerosol_point['latitude']]['transmission percent'][0]
        main_df.at[i, 'optical_thickness'] = optical_thickness
        main_df.at[i, 'transmission_percent'] = transmission_percent
    except:
        pass
    
main_df = main_df.dropna()
main_df = main_df.reset_index(drop=True)

temp_range = [np.mean(main_df['temp'])-1.5*np.std(main_df['temp']),np.mean(main_df['temp'])+1.5*np.std(main_df['temp'])]
soil_temp_range = [np.mean(main_df['soil_temp'])-1.5*np.std(main_df['soil_temp']),np.mean(main_df['soil_temp'])+1.5*np.std(main_df['soil_temp'])]
rain_range = [np.mean(main_df['rain'])-1.5*np.std(main_df['rain']),np.mean(main_df['rain'])+1.5*np.std(main_df['rain'])]
optical_thickness_range = [np.mean(main_df['optical_thickness'])-1.5*np.std(main_df['optical_thickness']),np.mean(main_df['optical_thickness'])+1.5*np.std(main_df['optical_thickness'])]
transmission_percent_range = [np.mean(main_df['transmission_percent'])-1.5*np.std(main_df['transmission_percent']),np.mean(main_df['transmission_percent'])+1.5*np.std(main_df['transmission_percent'])]

import matplotlib.pyplot as plt
import seaborn as sns

graph1 = sns.kdeplot(data=main_df['temp'], shade=True)
graph1.axvline(temp_range[0])
graph1.axvline(temp_range[1])
graph1.set_xlabel("Temprature")
graph1.set_ylabel("Fraction")
plt.savefig('kde_temp_hare.png')
plt.show()

graph2 = sns.kdeplot(data=main_df['soil_temp'], shade=True)
graph2.axvline(soil_temp_range[0])
graph2.axvline(soil_temp_range[1])
plt.xlabel("Soil Temprature")
plt.ylabel("Fraction")
plt.savefig('soil_temp_hare.png')
plt.show()

graph = sns.kdeplot(data=main_df['optical_thickness'], shade=True)
graph.axvline(optical_thickness_range[0])
graph.axvline(optical_thickness_range[1])
plt.xlabel("Optical Thickness")
plt.ylabel("Fraction")
plt.savefig('optical_hare.png')
plt.show()

graph = sns.kdeplot(data=main_df['transmission_percent'], shade=True)
graph.axvline(transmission_percent_range[0])
graph.axvline(transmission_percent_range[1])
plt.xlabel("Transmission Percent")
plt.ylabel("Fraction")
plt.savefig('trans_hare.png')
plt.show()

plt.hist(main_df['temp'])
plt.xlabel("Temprature")
plt.ylabel("No. of Occurrences in Data")
plt.savefig('hist_temp_hare.png')