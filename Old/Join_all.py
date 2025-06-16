import pandas as pd
import csv
from datetime import datetime, timedelta
# # Read only the first 6 rows
import pandas as pd
pd.options.mode.copy_on_write = True

# Join all the files

# List of files to join

file_names = [

]

# Extract the column names from the first file with pandas
df = pd.read_csv(file_names[0], header=0,  parse_dates=True)
columns_name = df.columns.tolist()


# pd.read_csv(file_names[0], header=0, parse_dates=True)
df_new = []
# Read the rest of the files and join them
for file_name in file_names:
    # Read the file
    df_temp = pd.read_csv(file_name, header=0, parse_dates=True)
    # Join the dataframes
    df_new.append(df_temp)

df= pd.concat(df_new, ignore_index=True)
df = df['MWh'].str.replace(',', '').astype(float)
# df.drop(columns=['time', 'day'], inplace=True)
# df.rename(columns={'Day2': 'Day'})


# Set the index as the Index column
df.set_index('Index', inplace=True)


# Save the joined dataframe to a new CSV file
df.to_csv('File.csv', index=True)

# Check for each Month the number of hours
# df[df['Month'] == 'January'].groupby('day')['MWh'].sum()
