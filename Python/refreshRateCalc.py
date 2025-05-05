import pandas as pd

# Load the CSV file
df = pd.read_csv('Test_log_2025_05_05_14_07_37_Med10.csv', delimiter=";")

# Convert the timestamp column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S.%f')

# Calculate the time difference between consecutive timestamps
df['time_diff'] = df['Timestamp'].diff()

# Calculate the average time difference
avg_time_diff = df['time_diff'].mean()

# Convert the average time difference to seconds, minutes, or another unit if needed
avg_time_diff_seconds = avg_time_diff.total_seconds()

# Calculate the refresh rate (number of records per second, minute, etc.)
refresh_rate = 1 / avg_time_diff_seconds

print(f"Average refresh rate: {refresh_rate} records per second")
