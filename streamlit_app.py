
# Now you can safely import the required packages
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# Load data
data = pd.read_csv("merge_classified.csv")

# Set up Streamlit app
st.title("Weather and Crime Analysis")
st.write("Use the dropdown menu to select a specific crime category or reset to display all crimes. The visualizations will be updated accordingly.")

# Show data
st.write("## Data")
st.write(data)

# Create a dropdown menu for selecting the crime category
crime_categories = data['Generalized_Offense'].unique().tolist()
selected_category = st.selectbox("Select a crime category", ["All"] + crime_categories)

# Filter the data based on the selected crime category
if selected_category == "All":
    filtered_data = data
else:
    filtered_data = data[data['Generalized_Offense'] == selected_category]

# Use .loc to set values on the original DataFrame
filtered_data.loc[:, 'DATE'] = pd.to_datetime(filtered_data['DATE'])
filtered_data.loc[:, 'weather_category'] = pd.cut((filtered_data['high_temp'] + filtered_data['low_temp']) / 2, bins=[-100, 32, 60, 80, 1000], labels=['Freezing (<=0°C)', 'Cool (0°C to 15°C)', 'Warm (15°C to 26°C)', 'Hot (>26°C)'])

# Plot a bar chart of the crime occurrences by OFFENSES
st.write("## Crime occurrences by OFFENSES")
crime_by_offenses = filtered_data.groupby(['Generalized_Offense']).size().reset_index(name='counts')
fig, ax = plt.subplots()
sns.barplot(x='Generalized_Offense', y='counts', data=crime_by_offenses, ax=ax, palette='viridis')
plt.xticks(rotation=90)
st.pyplot(fig)

# Plot a line chart of the monthly crime occurrences by average temperature
st.write("## Monthly crime occurrences by average temperature")
monthly_crime = filtered_data.groupby(pd.Grouper(key='DATE', freq='M')).size().reset_index(name='counts')
monthly_weather = filtered_data.groupby(pd.Grouper(key='DATE', freq='M')).agg({'high_temp': 'mean', 'low_temp': 'mean'}).reset_index()
monthly_weather['avg_temp'] = (monthly_weather['high_temp'] + monthly_weather['low_temp']) / 2
monthly_data = pd.merge(monthly_crime, monthly_weather, on='DATE', how='outer')
monthly_data = monthly_data.dropna()
st.line_chart(monthly_data.set_index('DATE')[['counts', 'avg_temp']].rename(columns={'counts': 'Crime Occurrences', 'avg_temp': 'Avg. Temperature (C)'}), use_container_width=True)

# Plot a bar chart of the crime occurrences by weather category
st.write("## Crime occurrences by weather category")
crime_by_weather = filtered_data.groupby(['weather_category']).size().reset_index(name='counts')
crime_by_weather = crime_by_weather[crime_by_weather.weather_category != 'Hot (>26°C)']
fig.tight_layout()
st.bar_chart(crime_by_weather.set_index('weather_category'), use_container_width=True)


# ... (previous code)

# Plot a line chart of the crime occurrences by precipitation
st.write("## Crime occurrences by precipitation")
st.write("Choose a specific month to display the daily crime occurrences and precipitation.")
daily_crime = filtered_data.groupby(pd.Grouper(key='DATE', freq='D')).size().reset_index(name='counts')
daily_precipitation = filtered_data.groupby(pd.Grouper(key='DATE', freq='D')).agg({'precipitation': 'mean'}).reset_index()

# Create a dropdown menu for selecting the month
available_months = daily_crime['DATE'].dt.to_period('M').unique().strftime('%B %Y').tolist()
selected_month = st.selectbox("Select a month", available_months)

# Filter the data based on the selected month
start_date = pd.to_datetime(selected_month)
end_date = start_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)
filtered_daily_crime = daily_crime[(daily_crime['DATE'] >= start_date) & (daily_crime['DATE'] <= end_date)]
filtered_daily_precipitation = daily_precipitation[(daily_precipitation['DATE'] >= start_date) & (daily_precipitation['DATE'] <= end_date)]

# Merge the dataframes
daily_data = pd.merge(filtered_daily_crime, filtered_daily_precipitation, on='DATE', how='outer')
daily_data = daily_data.dropna()

# Create a line chart with two y-axes
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Crime Occurrences', color=color)
ax1.plot(daily_data['DATE'].dt.day, daily_data['counts'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Precipitation (in)', color=color)  # we already handled the x-label with ax1
ax2.plot(daily_data['DATE'].dt.day, daily_data['precipitation'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
st.pyplot(fig)
