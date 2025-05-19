from rich import print
import time
from playwright.sync_api import Playwright, sync_playwright, expect
import csv
import datetime
from Demo_generacion_enero_abril import *
from Clean import *

# extract_january_april('enero_abril_2025', 2025)
clean('enero_abril_2025.csv', 'Generacion_2025')

