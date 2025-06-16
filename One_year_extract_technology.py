from rich import print
import time
import re
from playwright.sync_api import Playwright, sync_playwright, expect
import csv
import os
import calendar
from datetime import datetime, date

"""
Objective: Extract hole year of one technology from the AMM website.
The result: Because the website is buggy the max data range is three months each trimester will produce a csv file.
Note:
Sometimes it takes a lot of time to display the data and appear some 
pop ups messages. So its necessary to click a popup message, reload the page or restart the script. 
"""

def create_user_folder(folder_name):
    """
    Creates a folder with the user-specified name in the current working directory.

    Args:
        folder_name (str): Name of the folder to create

    Returns:
        str: Path of the created folder or None if there was an error
    """
    try:
        # Get current working directory
        current_directory = os.getcwd()

        # Create the full path for the new folder
        folder_path = os.path.join(current_directory, folder_name)

        # Check if folder already exists
        if not os.path.exists(folder_path):
            # Create the folder
            os.makedirs(folder_path)

        return folder_path

    except Exception:
        return None

# Function to save the table content to a CSV file
def save_to_csv(table_locator, save_name, tecnologia):
    # Extract the table content
    table_content = table_locator.inner_text()
    print("EXTRACTING... TABLE CONTENT...")
    # print(table_content)
    # Lest save the table content
    lines = table_content.strip().split("\n")

    # Create folder to store the files
    folder_name = create_user_folder(tecnologia)

    with open(f'{folder_name}/{save_name}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write each line to the CSV file
        for line in lines:
            # Split the line by whitespace and write to the CSV file
            writer.writerow(line.split())

    return print(f'Done writing the table: {save_name}.csv')

# Function to get the last day of a month
def last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

def extract_tecnologie(tecnologia, year_selection):
    """
    The following code is to extract the table from the page AMM with playwright tool
    This code is for january to april the year is selected in the code and the name of the csv file

   #Note: Sometimes because the site is buggy,
   its necessary to click a popup message or reload the page at the beginning.
    """

    # Trimester 1: Jan-Mar
    fecha_inicial = f'01/01/{year_selection}'
    last_day_mar = last_day_of_month(year_selection, 3)
    fecha_final = f'03/{last_day_mar}/{year_selection}'

    # Trimester 2: Apr-Jun
    fecha_inicial_2 = f'04/01/{year_selection}'
    fecha_final_2 = f'06/30/{year_selection}'

    # Trimester 3: Jul-Sep
    fecha_inicial_3 = f'07/01/{year_selection}'
    fecha_final_3 = f'09/30/{year_selection}'

    # Trimester 4: Oct-Dec
    fecha_inicial_4 = f'10/01/{year_selection}'
    fecha_final_4 = f'12/31/{year_selection}'


    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(60000) # Test with 60 seconds
        page.set_viewport_size({"width": 1280, "height": 720})
        page.goto("https://reportesbi.amm.org.gt/knowage/servlet/AdapterHTTP?PAGE=LoginPage&NEW_SESSION=TRUE")
        page.get_by_role("link", name="Generación").click()
        page.get_by_role("link", name="Generación por Tecnología").click()
        # page.wait_for_load_state("networkidle")
        time.sleep(10)

        # Enter the new page table to select data
        page.locator("#iframeDoc").content_frame.locator("iframe").content_frame.locator(
            "iframe[name=\"documentFrame\"]").content_frame.get_by_role("button").filter(
            has_text=re.compile(r"^$")).click()
        time.sleep(20)
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role(
            "button",name="Parameters").nth(1).click()

        page.wait_for_load_state("networkidle")
    # Enter the parameter's options
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            ".md-datepicker-input-container").first.click()

    #Locate and add fecha inicial
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Inicial").get_by_role("textbox").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Inicial").get_by_role("textbox").fill(
            f"{fecha_inicial}")
    # Locate and add fecha final
    #     page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
    #         "document-paramenter-element").filter(has_text="Fecha Final").get_by_role("textbox").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Final").get_by_role("textbox").fill(f"{fecha_final}")

        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "#select_19").click()
    # Select tecnología
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role(
            "option",name=f"{tecnologia}").locator("div").first.click()
    # Select hour
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "md-backdrop").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "#select_33").click()
        # Loop from 0 to 24
        for hour in range(0,24):
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role(
                "option",name=f"{hour}",exact=True).locator("div").first.click()

        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "md-backdrop").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                        name="Ejecutar").click()
        # Add a wheel mouse

        print('Lets see the table')
        time.sleep(5)
        table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")


        # Extract the table content
        save_name = f"Enero_marzo_{year_selection}_{tecnologia}"
        # Find the table save its content
        save_to_csv(table_locator, save_name, tecnologia)

        """
        Second trimester: April to June
        """
        print('Second Trimester')
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role(
            "button", name="Parameters").nth(1).click()
        # Enter the parameter's options
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            ".md-datepicker-input-container").first.click()

        # Locate and add fecha inicial
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Inicial").get_by_role("textbox").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Inicial").get_by_role("textbox").fill(
            f"{fecha_inicial_2}")
        time.sleep(2)

        # Locate and add fecha final
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Final").get_by_role("textbox").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Final").get_by_role("textbox").fill(
            f"{fecha_final_2}")
        time.sleep(1)
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                    name="Ejecutar").click()

        print('Lets see the table')
        time.sleep(1)

        # table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")
        table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")

        # Extract the table content
        save_name = f"Abril_junio_{year_selection}_{tecnologia}"
        # Find the table save its content
        save_to_csv(table_locator, save_name, tecnologia)

        """
        Third trimester: July to September
        """
        print('Third Trimester')

        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role(
            "button", name="Parameters").nth(1).click()
        page.wait_for_load_state("networkidle")
        # Enter the parameter's options
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            ".md-datepicker-input-container").first.click()

        # Locate and add fecha inicial
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Inicial").get_by_role("textbox").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Inicial").get_by_role("textbox").fill(
            f"{fecha_inicial_3}")
        time.sleep(2)
        # Locate and add fecha final
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Final").get_by_role("textbox").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Final").get_by_role("textbox").fill(
            f"{fecha_final_3}")
        time.sleep(1)

        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                    name="Ejecutar").click()

        print('Lets see the table')
        time.sleep(1)

        # table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")
        table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")

        # Extract the table content
        save_name = f"Julio_septiembre_{year_selection}_{tecnologia}"
        # Find the table save its content
        save_to_csv(table_locator, save_name, tecnologia)

        """
        Four trimester: October to December
        """
        print('Four Trimester')

        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role(
            "button", name="Parameters").nth(1).click()
        page.wait_for_load_state("networkidle")
        # Enter the parameter's options
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            ".md-datepicker-input-container").first.click()

        # Locate and add fecha inicial
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Inicial").get_by_role("textbox").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Inicial").get_by_role("textbox").fill(
            f"{fecha_inicial_4}")
        time.sleep(2)
        # Locate and add fecha final
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Final").get_by_role("textbox").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "document-paramenter-element").filter(has_text="Fecha Final").get_by_role("textbox").fill(
            f"{fecha_final_4}")
        time.sleep(2)

        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                    name="Ejecutar").click()

        print('Lets see the table')
        time.sleep(1)

        # table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")
        table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")

        # Extract the table content
        save_name = f"Octubre_diciembre_{year_selection}_{tecnologia}"
        # Find the table save its content
        save_to_csv(table_locator, save_name, tecnologia)


        # ---------------------
        context.close()
        browser.close()

    return print('Done Extracting')

# Define the inputs
year_selection = 2024
tecnologia = 'Turbina de Gas'


extract_tecnologie(tecnologia, year_selection)