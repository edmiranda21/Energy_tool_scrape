from rich import print
import time
from playwright.sync_api import Playwright, sync_playwright, expect
import csv
import datetime
from Demo_generacion_enero_abril import *
from Demo_generacion_junio_agosto import *
from Demo_generacion_septiembre_diciembre import *
from Clean import *

# extract_january_april('enero_abril_2025', 2025)
# extract_june_august('june_august_2024', 2024)
# extract_september_december(september, 2024)
clean('Mayo_2025.csv', 'may_2025')

