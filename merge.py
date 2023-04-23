import pandas as pd

def simplify_offenses(offense):
    offense = str(offense).split('/')[0].strip()

    if "Possession" in offense or "Marijuana" in offense:
        return "Illegal Possession"
    elif "Driv" in offense or "33" in offense:
        return "Driving Violation"
    elif "Assault" in offense:
        return "Assault"
    elif "5503" in offense:
        return "Disorderly Conduct"
    elif "Theft" in offense:
        return "Theft"
    elif "13" in offense:
        return "vehicle registration"
    elif "17" in offense:
        return "financial responsibility"
    elif '25' in offense:
        return "homicide"
    elif 'terror' in offense:
        return "terroristic threats"
    elif 'Strangulation' in offense:
        return "strangulation"
    elif 'Harassment' in offense:
        return "harassment"
    elif '3304' in offense:
        return 'criminal mischief'
    
    else:
        return offense

# Load the CSV file
crime = pd.read_csv('Crime.csv', index_col=0, header=0)
weather = pd.read_csv('pittsburgh_weather_2018.csv', index_col=0, header=0)

crimecopy = crime.copy()

crimecopy['ARRESTTIME'] = pd.to_datetime(crimecopy['ARRESTTIME'])

# Create a new column 'ARRESTDATE' to store the date information
crimecopy['ARRESTDATE'] = crimecopy['ARRESTTIME'].dt.strftime('%Y-%m-%d')

# Create a new column 'ARRESTTIMEONLY' to store the time information
crimecopy['ARRESTTIMEONLY'] = crimecopy['ARRESTTIME'].dt.strftime('%H:%M:%S')

crimecopy = crimecopy.set_index('ARRESTDATE')

# Preprocess and simplify offenses
crimecopy['OFFENSES'] = crimecopy['OFFENSES'].apply(simplify_offenses)

merged_df = crimecopy.join(weather, how='inner')

merged_df.to_csv('merged_new.csv', index=True)
