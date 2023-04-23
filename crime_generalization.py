import pandas as pd

# Load the CSV file
crime = pd.read_csv('Crime.csv', index_col=0, header=0)

def keep_first_offense(offense):
    if isinstance(offense, str):
        return offense.split('/')[0].strip()
    else:
        return None

def generalize_offense(offense):
    if isinstance(offense, str):
        return offense[:2]
    else:
        return None

# Keep only the first crime
crime['First_Offense'] = crime['OFFENSES'].apply(keep_first_offense)

# Merge crimes with the same first two digits
crime['Generalized_Offense'] = crime['First_Offense'].apply(generalize_offense)

# Group by the Generalized_Offense and take the first value of the First_Offense
crime['Generalized_Offense'] = crime.groupby('Generalized_Offense')['First_Offense'].transform('first')

# Save the modified DataFrame to a new CSV file
crime.to_csv('generalized_crime.csv', index=True)
