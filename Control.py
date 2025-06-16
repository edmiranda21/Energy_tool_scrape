from Cleaning_entire_year import *

# extract_january_april('enero_abril_2025', 2025)
# extract_june_august('june_august_2024', 2024)
# extract_september_december(september, 2024)
# clean('May_2025.csv', 'may_2025')

"""
Extract data generation total for desired year
"""
# extract_january_april(2009)

"""
Just for cleaning for desired year
Files after cleaning will be saved as a unique file 'Generacion_2009.csv'
Then files_names will be erased
"""
save_name = 'May_2025'
file_names = [ 'Mayo_2025.csv'
    # f'Enero_abril_{save_name}.csv',
    # f'Mayo_agosto_{save_name}.csv',
    # f'Septiembre_diciembre_{save_name}.csv'
]

clean_year(file_names, save_name)

