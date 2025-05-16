import pandas as pd
import csv
from datetime import datetime
# # Read only the first 6 rows
import pandas as pd

def clean(file_name):
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

    # Long form
    df_long = df.melt(id_vars=['time'], var_name="day", value_name="MWh")
    df_long = df_long.sort_values(by=['time','day']).reset_index(drop=True).set_index('time')
    # Save the long format to a CSV file
    df_long.to_csv(f'table_cleaned_long.csv', encoding='utf8', index=True)

    df.set_index('time', inplace=True)

    # Guardar información en un archivo .csv
    df.to_csv(f'table_cleaned.csv', encoding='utf8', index=True)

    return print(f"The data has been saved in a .csv file with name: 'table_cleaned.csv'")

clean('table1.csv')