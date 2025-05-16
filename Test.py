import pandas as pd
import csv
from datetime import datetime, timedelta
# # Read only the first 6 rows
import pandas as pd
pd.options.mode.copy_on_write = True

# file_name = 'table1.csv'
file_name = 'table16-05-2025.csv'

with open(file_name, 'r') as file:
    line0 = next(file).strip().strip('"').split(',')  # Get line 0, remove newline and quotes

# print(len(line0))
# Step2: find the values
def find_first_non_null_index(file_path):
    with open(file_path, 'r') as file:
        reader = list(csv.reader(file))
        for i in range(len(reader) - 1, 0, -1):

            if not reader[i]:
                return int(i + 1)
    return None

skip_row = find_first_non_null_index(file_name)
print(skip_row)

df = pd.read_csv(file_name, header=None, skiprows=skip_row, on_bad_lines='skip')

# Add the column names with the line0, starting from the second element
df.columns = ['time'] + line0

# df['time'] = df['time'].astype(str)  # Remove spaces from the time column
# # Find the "24:00" and replace it with "00:00"
# df['time'] = df['time'].replace('24:00', '00:00')
# # Transform the time column to datetime
# df['time'] = pd.to_datetime(df['time']).dt.strftime('%H:%M')
# df = df.sort_values(by='time')
print(df)