import pandas as pd
import csv
from datetime import datetime, timedelta
import os
pd.options.mode.copy_on_write = True

def transform_long_clean(df_old):
    """
    Transform the dataframe from wide form to long format and clean it.

    Args:
    df_old (pd.DataFrame): Dataframe with the data in wide format.

    Returns:
    pd.DataFrame: Cleaned dataframe in long format with hourly data.
    """
    # Long form ideal
    df = df_old.melt(id_vars=['time'], var_name="day", value_name="MWh")
    df = df.sort_values(by=['time', 'day']).reset_index(drop=True)
    df['day'] = df['day'].astype(str)
    df['time'] = df['time'].astype(str)

    # Clean
    df['Index'] = df['day'] + '-' + df['time']
    df['Index'] = pd.to_datetime(df['Index'])
    df.set_index('Index', inplace=True)
    df.sort_index(inplace=True)
    # Drop day and time
    df.drop(columns=['day', 'time'], inplace=True)

    # New dataframe with time set as hourly
    min_date = df.index.min()
    max_date = df.index.max()
    date_range = pd.date_range(min_date,
                               max_date,
                               freq='H')

    clean_dataframe = pd.DataFrame(index=date_range)
    clean_dataframe.index = clean_dataframe.index.strftime('%Y-%m-%d-%H:%M:%S')

    # Filter original dataframe to keep only the dates hourly
    df_filtered = df[df.index.isin(clean_dataframe.index)]

    # df_filtered = df.copy()
    df_filtered['Hora'] = df_filtered.index.strftime('%H:%M')
    df_filtered['Month'] =df_filtered.index.month_name()
    df_filtered['Year'] = df_filtered.index.year
    df_filtered['Day'] = df_filtered.index.day_name()
    df_filtered['MWh'] = df_filtered['MWh'].str.replace(',', '').astype(float)
    #

    return df_filtered


def clean(file_name):
    """
    Extract the data from the file_name, clean it, and return a dataframe with the data in long format.

    Args:
    file_name (str): Name of the file to be cleaned in CSV format, obtained from the scrapping process.

    Returns:
    pd.DataFrame: Dataframe with the data in long format and cleaned.
    """
    # Step 1: Extract line 0
    with open(file_name, 'r') as file:
        line0 = next(file).strip().strip('"').split(',')  # Get line 0, remove newline and quotes
    # Step 2: Find the first non-null index to use in the skiprow in the next step
    def find_first_non_null_index(file_path):
        with open(file_path, 'r') as file:
            reader = list(csv.reader(file))
            for i in range(len(reader) - 1, 0, -1):
                if not reader[i]:
                    return int(i+1)
        return None
    skip_row = find_first_non_null_index(file_name)

    # Step 3: Read the data starting from the first non-null index
    df = pd.read_csv(file_name, header=None, skiprows=skip_row)

    # Step 4: Set the header
    df.columns = ['time'] + line0
    df['time'] = df['time'].astype(str)

    # Find the "24:00" and replace it with "00:00"
    df['time'] = df['time'].replace('24:00', '00:00')

    # Transform the 'time' column to datetime
    df['time'] = pd.to_datetime(df['time']).dt.strftime('%H:%M')
    df = df.sort_values(by='time')

    # Format the dataframe to long format and clean it
    dataframe = transform_long_clean(df)
    print(f"Clean data of: '{file_name}.csv'")
    return dataframe

# Join to a single file the data from different files obtained from the scrapping and cleaning process
def clean_year(file_names, save_name):
    """
    Join the data from different files into a single dataframe, clean it, and save it as a CSV file.
    Args:
    file_names (list): List of file names to be cleaned and joined.

    Returns:
    None: The function saves the cleaned data to a CSV file and prints the number of records.
    """
    df_new = []
    for file in file_names:
        df_clean = clean(file)
        df_new.append(df_clean)
        print(f'File: {file} '
              f'Total data: {len(df_clean)}')
    df = pd.concat(df_new)

    # Save the joined dataframe to a new CSV file
    df.to_csv(f'{save_name}.csv', index=True)
    print(f'Numero de datos: {len(df)}')

    # Erase the list of files
    for file in file_names:
        try:
            os.remove(file)
        except OSError as e:
            print(f"Error deleting file {file}: {e}")

    return print(f"Saved as '{save_name}.csv'")