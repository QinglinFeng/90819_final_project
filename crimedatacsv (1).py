# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 15:24:36 2023

@author: kothi
"""

import pandas as pd


# Load the CSV file
crash = pd.read_excel('CrashData_Clean.xlsx', index_col=0, header=0)
crime = pd.read_csv('crimedata.csv', index_col=0, header=0)
weather = pd.read_csv('pittsburgh_weather_2018.csv', index_col=0, header=0)

crimecopy = crime.copy()


crimecopy['ARRESTTIME'] = pd.to_datetime(crimecopy['ARRESTTIME'])
crimecopy['ARRESTTIME'] = crimecopy['ARRESTTIME'].dt.strftime('%Y-%m-%d')
crimecopy = crimecopy.set_index('ARRESTTIME')

crimecopy = crimecopy.drop(['ARRESTLOCATION','OFFENSES', 'INCIDENTLOCATION','INCIDENTZONE','INCIDENTTRACT','COUNCIL_DISTRICT','PUBLIC_WORKS_DIVISION','X','Y','CCR'], axis=1)
#print(crimecopy)
#print(weather)
merged_df = crimecopy.join(weather, how='inner')
print(merged_df)
merged_df.to_excel('merged_data.xlsx', index=True)