import pandas as pd
import csv
from datetime import datetime, timedelta
# # Read only the first 6 rows
import pandas as pd
pd.options.mode.copy_on_write = True

# file_name = 'table1.csv'
file_name = 'table_enero_mayo_2024.csv'

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
#%%
# Clean try
with open(file_name, 'r') as f:
    reader = csv.reader(f)

    # Step 1: Read the base date from the first row
    base_date_str = next(reader) # e.g., "Columns names as: 2024-01-01"
    values = list(csv.reader(f))[skip_row-1:]  # Each row is a list of values with the first as hour and the rest as values

print(base_date_str)
# print(values)
#%%
for i in range(len(values)):
    hour_value = values[i][0]
    power_value = values[i][1:]

    # Extrac the first item of each row in power_value
    for item in power_value[:1]:
        print(item)

#%%
# For each date test the first 5 days
count = 0
for date in base_date_str:
    for i in range(len(values)):
        hour_value = values[i][0]
        power_value = values[i][1+count]
        # Sum one place to the power_value
        print(f"Column: {count}, Date: {date}, Hour: {hour_value}, Value: {power_value}")

    count = count + 1


    # Extrac the first item of each row in power_value
    #     for item in power_value[:1]:
    #         print(f"Date: {date}, Hour: {hour_value}, Value: {item}")
