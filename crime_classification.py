import pandas as pd

def simplify_offenses(offense):
    offense = str(offense).split('/')[0].strip()

    if "13" in offense:
        return "Illegal Possession or Use of Drugs"
    elif "Driv" in offense or "vehicle" in offense or "traffic" in offense or "4703" in offense or '4524' in offense:
        return "Driving Violation"
    elif "assult" in offense or "26" in offense or "27" in offense:
        return "Assault"
    elif "39" in offense:
        return "Theft"
    elif "55" in offense:
        return "Disorderly conduct"
    elif "17" in offense:
        return "Financial responsibility"
    elif '903' in offense:
        return "Conspiracy"
    elif '3304' in offense:
        return "Mischief"
    elif '61' in offense or "weapon" in offense or '912' in offense:
        return "Illegal possession of a firearm"
    elif '3502' in offense:
        return "Burglary"
    elif '100' in offense:
        return "Fugitive"
    elif '2501' in offense:
        return "Homicide"
    elif '3701' in offense:
        return "Robbery"
    elif '38' in offense:
        return "Impairment"
    elif '49' in offense:
        return "Counterfeiting"
    elif '5123' in offense:
        return "Contraband"
    elif '59' in offense:
        return "Prostitution"
    elif '601' in offense or '6301' in offense or '6310' in offense:
        return "Liquor law violation"
    elif '9501' in offense:
        return "Bench warrant"
    elif '4120' in offense:
        return "Identity theft"
    else:
        return "Other"

crime = pd.read_csv('generalized_crime.csv', index_col=0, header=0)

crimecopy = crime.copy()
# Preprocess and simplify offenses
crimecopy['Generalized_Offense'] = crimecopy['Generalized_Offense'].apply(simplify_offenses)
crimecopy.to_csv('classified_crime.csv', index=True)