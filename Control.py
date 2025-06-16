# For energy demand data
from One_year_extract import *
from Clean_entire_year import *
from Extract_desired_month_year import *

# For generation by technology type
from One_year_extract_technology import *
from Clean_technology_entire_data import *

# For energy demand data
"""
Extract data for a specific year
"""
# Inputs to work
# generation_year = 2024
# # Call the function to clean the year
# extract_generation_data(generation_year)
#
# """
# Clean files later will be saved as a unique files used will be erased
# """
# # Inputs to work
# save_name = 'May_2025'
# file_names = [ 'Mayo_2025.csv'
#     # f'Enero_abril_{save_name}.csv',
#     # f'Mayo_agosto_{save_name}.csv',
#     # f'Septiembre_diciembre_{save_name}.csv'
# ]
# # Call the function to clean the year
# clean_year(file_names, save_name)
#
# For desired month and year of energy demand data
# Inputs to work
d_month_list = ['MAYO']
d_year = '2025'
d_save_name = "Mayo"
# Call the function to extract the desired month and year
# desired_month_year(d_month_list, d_year, d_save_name)
# save_name = 'May_2025'
# file_names = [ 'Mayo_2025.csv']
# clean_year(file_names, save_name)



# # For generation by technology type
# """
# Extract data for a specific year and technology type"""
#
# # Inputs to work
# year_selection = 2024
# technology = 'Turbina de Gas'
# # Call the function to extract the technology for the year
# extract_tecnologie(technology, year_selection)

# Call the function to clean the technology for the year
technology_files = 'Turbina de Gas'
tecnology_name = 'Turbina de Gas'
clean_technology(technology_files, tecnology_name)
