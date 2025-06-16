import pandas as pd
import csv
from datetime import datetime, timedelta
# # Read only the first 6 rows
import pandas as pd
pd.options.mode.copy_on_write = True

today = datetime.today().date().strftime("%d-%m-%Y")

# Create a function than transform and clean the data
def transform_long_clean(df_old, save_name):
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

    # New dataframe with a time set as hourly
    min_date = df.index.min()
    max_date = df.index.max()
    date_range = pd.date_range(min_date,
                               max_date,
                               freq='H')

    clean_dataframe = pd.DataFrame(index=date_range)
    clean_dataframe.index = clean_dataframe.index.strftime('%Y-%m-%d-%H:%M:%S')

    # Filter the original dataframe to keep only the dates hourly
    df_filtered = df[df.index.isin(clean_dataframe.index)]

    # df_filtered = df.copy()
    df_filtered['Hora'] = df_filtered.index.strftime('%H:%M')
    df_filtered['Month'] =df_filtered.index.month_name()
    df_filtered['Year'] = df_filtered.index.year
    df_filtered['Day'] = df_filtered.index.day_name()
    df_filtered['MWh'] = df_filtered['MWh'].str.replace(',', '').astype(float)

    # Save the long format to a CSV file
    df_filtered.to_csv(f'{save_name}.csv', encoding='utf8', index=True)
    return print(df_filtered.head())


def clean(file_name, save_name):
    # Step 1: Extract line 0
    with open(file_name, 'r') as file:
        line0 = next(file).strip().strip('"').split(',')  # Get line 0, remove newline and quotes
    # print(len(line0))
    # Step2: find the values
    def find_first_non_null_index(file_path):
        with open(file_path, 'r') as file:
            reader = list(csv.reader(file))
            for i in range(len(reader) - 1, 0, -1):
                if not reader[i]:
                    return int(i+1)
        return None
    skip_row = find_first_non_null_index(file_name)

    # Step 2: Read the data starting from the time-value pairs
    df = pd.read_csv(file_name, header=None, skiprows=skip_row)

    # Add the column names with the line0, starting from the second element
    df.columns = ['time'] + line0

    df['time'] = df['time'].astype(str) # Remove spaces from the time column
    # Find the "24:00" and replace it with "00:00"
    df['time'] = df['time'].replace('24:00', '00:00')
    # Transform the time column to datetime
    df['time'] = pd.to_datetime(df['time']).dt.strftime('%H:%M')
    df = df.sort_values(by='time')

    transform_long_clean(df, save_name)


    # df.set_index('time', inplace=True)

    # Guardar información en un archivo .csv
    # df.to_csv(f'table_cleaned.csv', encoding='utf8', index=True)

    return print(f"The data has been saved in a .csv file with name: '{save_name}.csv'")
