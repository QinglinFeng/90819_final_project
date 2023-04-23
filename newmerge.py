
import pandas as pd


# Load the CSV file
crime = pd.read_csv('classified_crime.csv', index_col=0, header=0)
weather = pd.read_csv('pittsburgh_weather_2018.csv', index_col=0, header=0)

crimecopy = crime.copy()


crimecopy['ARRESTTIME'] = pd.to_datetime(crimecopy['ARRESTTIME'])
crimecopy['ARRESTTIME'] = crimecopy['ARRESTTIME'].dt.strftime('%Y-%m-%d')
crimecopy = crimecopy.set_index('ARRESTTIME')

#print(crimecopy)
#print(weather)
merged_df = crimecopy.join(weather, how='inner')
print(merged_df)
merged_df.to_csv('merge_classified.csv', index=True)