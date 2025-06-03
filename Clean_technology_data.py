import pandas as pd
import csv
import re
from datetime import datetime

file_path = 'Test_Tecnologias_¨Exportacion_2024.csv'
# Read the entire file as text to analyze structure
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Extract data rows (skip the header)
data = []
current_date = None
day_of_week = None

# Split content into lines
lines = content.strip().split('\n')

# Find where the data actually starts (after the headers)
def find_first_non_null_index(file_path):
    with open(file_path, 'r') as file:
        reader = list(csv.reader(file))
        for i in range(len(reader) - 1, 0, -1):
            if not reader[i]:
                return int(i+1)
    return None
skip_row = find_first_non_null_index(file_path)


# Process lines with data
for i in range(skip_row, len(lines)):
    line = lines[i].strip()
    # print(line)

    # Skip empty lines
    if not line:
        continue
    #
    # # Parse date row - improved pattern to capture various date formats and month indicators
    date_match = re.match(r'(\d{4}-\d{2}-\d{2}),(\d{2}:\d{2}:\d{2}),(.+),(.+),(\d{2}:\d{2}:\d{2}),([-\d.]+)', line)
    # print(date_match)
    if date_match:
        current_date = date_match.group(1)
        day_of_week = date_match.group(4)
        hour = date_match.group(5)  # Use the second time field (after day of week)
        value = float(date_match.group(6))
        # print(current_date, hour,day_of_week, value)
        data.append([current_date, hour, day_of_week, value])
    else:
    #     # Parse hour row with more flexible pattern to account for missing data
        hour_match = re.match(r'^(\d{2}:\d{2}:\d{2}),([-\d.]+)$', line)
        # print(hour_match)
        if hour_match and current_date:
            hour = hour_match.group(1)
            value = float(hour_match.group(2))
            # print(current_date, hour, day_of_week, value)
            data.append([current_date, hour, day_of_week, value])
    #     # Handle missing hour entries (e.g., where some hours are skipped)
    #     elif current_date and "," in line:
    #         parts = line.split(',')
    #         if len(parts) == 2 and re.match(r'\d{2}:\d{2}:\d{2}', parts[0]):
    #             hour = parts[0]
    #             try:
    #                 value = float(parts[1])
    #                 data.append([current_date, hour, day_of_week, value])
    #             except ValueError:
    #                 # Skip lines that don't have proper numeric values
    #                 continue

