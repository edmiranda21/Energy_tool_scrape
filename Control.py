from Cleaning_entire_year import *

"""
Scrape tools from Guatemala energy data generation
This python will have all the main function to extract, clean and save the data in formatted CSV files.

The will be two scrapper scripts, one for energy demand and another for a generation technology type. Each one
comes from a different tab of the same website.

Tool #1
The tool to scrape the data is playwright, the website is a little big tricky and buggy,
so the intervention of a human is needed to extract the data. 
The data extracted will be in hourly format, so the each iteration will extract a 4 months period of data for the
desired year.
The data will be extracted from the table and saved in a csv file unstructured and uncleaned, 
later this file will be cleaned and formatted as wide format and saved as a CSV file.

The is a script 'clean_year.py' that will join the data 
from different files into a single dataframe, clean it, save it as a CSV file and delete the files used.

Tool #2
The tool to scrape the data is playwright, the website is a little big tricky and more buggy than the first one,
so the intervention of a human is needed to extract the data. 
Note: the site takes a while to load between 20 to 30 seconds, so be patient.
The data extracted will be in hourly format, so the each iteration will extract a 3 months period (Trimester) 
of data for the desired year.
The data will be extracted from the table and saved in a csv file unstructured and uncleaned, 
later this file will be cleaned and formatted as wide format and saved as a CSV file.

The script 'clean_technology_entire_data.py' will create a folder with the name of the technology type,
loop for the files in the folder and will save the cleaned data in a CSV file with the name of the technology type
and the year.

The data used in this project are from the following sources:

AMM 'Administrator de Mercado Mayorista', open data source from Guatemala, url: [https://reportesbi.amm.org.gt/]
 
"""

"""
Clean files later will be saved as a unique file 'Generacion_2009.csv'
Files used will be erased
"""
save_name = 'May_2025'
file_names = [ 'Mayo_2025.csv'
    # f'Enero_abril_{save_name}.csv',
    # f'Mayo_agosto_{save_name}.csv',
    # f'Septiembre_diciembre_{save_name}.csv'
]

clean_year(file_names, save_name)

