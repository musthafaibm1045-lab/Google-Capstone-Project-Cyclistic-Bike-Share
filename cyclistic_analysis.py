import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# 1. Load Data
df_q1 = pd.read_csv('C:/Users/MUHAMMAD MUSTHAFA/Desktop/Data/Divvy_Trips_2019_Q1.csv')
df_q2 = pd.read_csv('C:/Users/MUHAMMAD MUSTHAFA/Desktop/Data/Divvy_Trips_2019_Q2.csv')
df_q3 = pd.read_csv('C:/Users/MUHAMMAD MUSTHAFA/Desktop/Data/Divvy_Trips_2019_Q3.csv')
df_q4 = pd.read_csv('C:/Users/MUHAMMAD MUSTHAFA/Desktop/Data/Divvy_Trips_2019_Q4.csv')

# Standardize column names for Q2 to match others 
df_q2.columns = ['trip_id', 'start_time', 'end_time', 'bikeid', 'tripduration',
                 'from_station_id', 'from_station_name', 'to_station_id',
                 'to_station_name', 'usertype', 'gender', 'birthyear']

# Combine Data
df_combined = pd.concat([df_q1, df_q2, df_q3, df_q4])

# 2. Data Preprocessing
df_combined['start_time'] = pd.to_datetime(df_combined['start_time'], format='%Y-%m-%d %H:%M:%S')
df_combined['starting_date'] = df_combined['start_time'].dt.date
df_combined['starting_time'] = df_combined['start_time'].dt.time
df_combined = df_combined.drop('start_time', axis=1)

df_combined['end_time'] = pd.to_datetime(df_combined['end_time'], format='%Y-%m-%d %H:%M:%S')
df_combined['ending_date'] = df_combined['end_time'].dt.date
df_combined['ending_time'] = df_combined['end_time'].dt.time
df_combined = df_combined.drop('end_time', axis=1)

# Drop unnecessary columns
df_combined = df_combined.drop(['trip_id', 'bikeid', 'from_station_id', 'gender',
                                'birthyear', 'from_station_name', 'to_station_id', 'to_station_name'], axis=1)

# Extract Days and Months
df_combined['starting_date'] = pd.to_datetime(df_combined['starting_date'])
df_combined['ending_date'] = pd.to_datetime(df_combined['ending_date'])
df_combined['starting_day'] = df_combined['starting_date'].dt.day_name()
df_combined['starting_month'] = df_combined['starting_date'].dt.month_name()
df_combined['ending_day'] = df_combined['ending_date'].dt.day_name()
df_combined['ending_month'] = df_combined['ending_date'].dt.month_name()

df_combined = df_combined.dropna(how='all')

# Calculate Ride Duration in Minutes
df_combined['starting_time'] = pd.to_datetime(df_combined['starting_time'], format='%H:%M:%S')
df_combined['ending_time'] = pd.to_datetime(df_combined['ending_time'], format='%H:%M:%S')
df_combined['duration'] = (df_combined['ending_time'] - df_combined['starting_time']).dt.total_seconds() // 60
df_combined['duration'] = df_combined['duration'].apply(lambda x: max(0, x))
df_combined['duration'] = df_combined['duration'].clip(lower=0).astype(int)
df_combined = df_combined[df_combined['duration'] != 0]

# Clean Usertype strings
df_combined['usertype'] = df_combined['usertype'].str.strip()

# --- 3. Visualizations ---

# Visual 1: Overall Riders by Usertype
plt.figure(figsize=(10, 8))
label_values = ['subscriber', 'customer']
df_combined['usertype'].value_counts().plot(kind='pie', labels=label_values, autopct='%1.1f%%')
plt.title('Overall Riders by Usertype')
plt.show()

# Visual 2: Daily Riders by Usertype
df_grouped = df_combined.groupby(['starting_day', 'usertype']).size().reset_index(name='count')
df_pivoted = df_grouped.pivot(index='starting_day', columns='usertype', values='count')
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_pivoted = df_pivoted.loc[day_order]
df_pivoted.plot(kind='bar')
plt.title('Daily Riders by Usertype')
plt.show()

# Visual 3: Number of Riders by Month and Usertype (Heatmap)
pivot_df = df_combined.pivot_table(index='starting_month', columns='usertype', aggfunc='size', fill_value=0)
plt.figure(figsize=(10, 8))
sns.heatmap(pivot_df, annot=True, cmap='Blues', fmt='d')
plt.title('Number of Riders by Month and Usertype')
plt.xlabel('Usertype')
plt.ylabel('Starting Month')
plt.show()

# Visual 4: Total Rides by Season and Usertype
month_to_season = {
    'January': 'winter', 'February': 'winter', 'March': 'spring',
    'April': 'spring', 'May': 'spring', 'June': 'summer',
    'July': 'summer', 'August': 'summer', 'September': 'fall',
    'October': 'fall', 'November': 'fall', 'December': 'winter'
}
df_combined['season'] = df_combined['starting_month'].map(month_to_season)
season_riders = df_combined.groupby(['season', 'usertype']).size().unstack()
plt.figure(figsize=(10, 6))
season_riders.plot(kind='bar')
plt.title('Total Rides by Season and Usertype')
plt.xlabel('Season')
plt.ylabel('Total Rides')
plt.tight_layout()
plt.legend(title='Usertype')
plt.show()

# Visual 5: Average Ride Duration by Day
df_grouped_dur = df_combined.groupby(['starting_day', 'usertype'])['duration'].mean().reset_index()
df_pivoted_dur = df_grouped_dur.pivot(index='starting_day', columns='usertype', values='duration')
df_pivoted_dur = df_pivoted_dur.loc[day_order]
df_pivoted_dur.plot(kind='bar')
plt.title('Average Ride Duration by User Type and Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Average Ride Duration (Minutes)')
plt.legend(title='User Type')
plt.show()

