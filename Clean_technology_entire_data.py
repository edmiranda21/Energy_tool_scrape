import pandas as pd
import csv
import re
from pathlib import Path
import os
from datetime import datetime, timedelta

# Search files in the directory
def clean_tecnology(file, tecnology_name):
    # Read the entire file as text to analyze structure
    with open(file, 'r', encoding='utf-8') as file_name:
        content = file_name.read()

    # Extract data rows (skip the header)
    data = []
    current_date = None
    day_of_week = None

    # Split content into lines
    lines = content.strip().split('\n')

    # Find where the data actually starts (after the headers)
    def find_first_non_null_index(file):
        with open(file, 'r') as file:
            reader = list(csv.reader(file))
            for i in range(len(reader) - 1, 0, -1):
                if not reader[i]:
                    return int(i+1)
        return None
    skip_row = find_first_non_null_index(file)

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
            # Handle missing hour entries (e.g., where some hours are skipped)
            elif current_date and "," in line:
                parts = line.split(',')
                if len(parts) == 2 and re.match(r'\d{2}:\d{2}:\d{2}', parts[0]):
                    hour = parts[0]
                    try:
                        value = float(parts[1])
                        data.append([current_date, hour, day_of_week, value])
                    except ValueError:
                        # Skip lines that don't have proper numeric values
                        continue
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['Date', 'Hour', 'Day (Spanish)', 'Potencia'])
    df['Tecnología'] = tecnology_name

    # Create a datetime column for easier analysis
    df['Index'] = pd.to_datetime(df['Date'] + ' ' + df['Hour'])
    df.drop(columns=['Hour'], inplace=True)
    df = df[df['Index'].dt.minute==1]
    df['Index'] = df['Index'].dt.floor('H')
    df.set_index('Index', inplace=True)
    df['Month'] = df.index.month_name()
    df['Year'] = df.index.year
    df['Day'] = df.index.day_name()
    df['Hour'] = df.index.strftime('%H:%M')
    # Set column Day (spanish) to just capitalize the first letter
    df['Day (Spanish)'] = df['Day (Spanish)'].str.capitalize()

    # Reorder columns
    df = df[['Potencia', 'Hour','Date' ,'Month','Year','Day','Day (Spanish)', 'Tecnología']]
    return df

# Iterate through all files in the directory
def clean_technology(technology_files, tecnology_name):

    # Get the current working directory
    home = os.getcwd()
    # Create the full path for the new folder
    file_path = Path(home + f'/{technology_files}')

    df_new = []
    for file in file_path.glob('*.csv'):
        df_clean = clean_tecnology(file, tecnology_name)
        df_new.append(df_clean)
        print(f'File: {file} '
              f'Total data: {len(df_clean)}')

    df = pd.concat(df_new)
    # Sort by index
    df.sort_index(inplace=True)
    year_name = min(df.index.year)
    df.to_csv(f'Clean_{tecnology_name}_{year_name}.csv', index=True)
    print(f'Data file save as: Clean_{tecnology_name}_{year_name}.csv '
          f'Total data: {len(df)}')


