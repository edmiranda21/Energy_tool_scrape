from Cleaning_entire_year import *

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

