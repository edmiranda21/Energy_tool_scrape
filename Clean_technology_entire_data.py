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
        # If the line has more than 1 comma print it for debugging
        if line.count(',') > 2:
            parts = line.split(',')
            current_date = parts[0]
            day_of_week = parts[3]
            hour = parts[4]
            # If there is more than one part after the 5th, join them as value and transform to float
            value = ','.join(parts[5:]) if len(parts) > 1 else None
            # Eliminate the "" in the value that are in the begging and the end in some cases
            value = value.replace('"', '')
            # print(f'--{current_date} - {hour} -{day_of_week} - {value}--')
            data.append([current_date, hour, day_of_week, value])
        else:
            # print(line)
            line = line.replace('"', '')
            # if there is two, split by comma replace the second one with nothing
            parts = line.split(',')
            # print(parts)
            hour = parts[0]
            if len(parts) > 2:
                value_long = float(parts[1] + parts[2])
                # print(f'Check: {current_date} - {hour} - {day_of_week} - {value_long}')
                data.append([current_date, hour, day_of_week, value_long])
            else:
                value = parts[1]
                # print(f'Check: {current_date} - {hour} - {day_of_week} - {value}')
                data.append([current_date, hour, day_of_week, value])
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
    print(file_path)


    df_new = []
    for file in file_path.glob('*.csv'):
        if 'Clean' in file.name:
                continue
        df_clean = clean_tecnology(file, tecnology_name)
        df_new.append(df_clean)
        print(f'File: {file} '
              f'Total data: {len(df_clean)}')

    # Erase the files in the folder
    # for file in file_path.glob('*.csv'):
    #     if 'Clean' in file.name:
    #         continue
    #     try:
    #         os.remove(file)
    #     except OSError as e:
    #         print(f"Error deleting file {file}: {e}")

    df = pd.concat(df_new)
    # Sort by index
    df.sort_index(inplace=True)
    df['Potencia'] = df['Potencia'].astype(str).str.replace('"', '', regex=False).str.replace(',', '', regex=False)
    df['Potencia'] = df['Potencia'].astype(float)
    # Save a csv for every year with
    years_list = df.index.year.unique()
    for year in years_list:
        df_year = df.query('Year == @year')
        df_year.to_csv(f'{file_path}/Clean_{tecnology_name}_{year}.csv', index=True)
        print(f'Data file save as: {file_path}/Clean_{tecnology_name}_{year}.csv '
          f'Total data: {len(df_year)}')

# Test
technology_files = 'Hidroeléctrica'
tecnology_name = 'Hidroeléctrica'
clean_technology(technology_files, tecnology_name)