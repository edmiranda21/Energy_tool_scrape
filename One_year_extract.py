import time
from playwright.sync_api import Playwright, sync_playwright, expect
import csv
import datetime


month_list = ['ENERO','FEBRERO', 'MARZO','ABRIL']
month_list_2 = ['MAYO', 'JUNIO', 'JULIO', 'AGOSTO']
month_list_3 = ['SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
year_selection = 2025

# Function to save the table content to a CSV file
def save_to_csv(table_locator, save_name):
    """
    Locate the table and save its content to a CSV file.
    Args:
        table_locator: The locator for the table element, obtained from Playwright.

    Returns:
        None: The function saves the table content to a CSV file, and prints a confirmation message.
    """
    # Extract the table content
    table_content = table_locator.inner_text()
    print("EXTRACTING... TABLE CONTENT...")
    # print(table_content)
    # Lest save the table content
    lines = table_content.strip().split("\n")

    with open(f'{save_name}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write each line to the CSV file
        for line in lines:
            # Split the line by whitespace and write to the CSV file
            writer.writerow(line.split())

    return print(f'Done writing the table to CSV: {save_name}.csv')


def extract_generation_data(year_selection):
    """
    Extracts generation data for a specific year from the AMM website using Playwright.

       Args:
        year_selection (int): The year for which the generation data will be extracted.

    Returns:
        None: The function performs the extraction and saves the data to CSV files, each file corresponds a four-month period.
       """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_viewport_size({"width": 1280, "height": 720})
        page.goto("https://reportesbi.amm.org.gt/knowage/servlet/AdapterHTTP?PAGE=LoginPage&NEW_SESSION=TRUE")
        page.get_by_role("link", name="Generación").click()
        page.get_by_role("link", name="Generación por Hora").click()
        page.wait_for_load_state("networkidle")

        # Scroll to the bottom of the page
        for x in range(1, 2):
            page.mouse.wheel(0, 500)
            time.sleep(1)

            # Enter the new page table to select data
            page.locator("#iframeDoc").content_frame.locator("iframe").content_frame.locator(
                "iframe[name=\"documentFrame\"]").content_frame.locator("[id=\"\\31 531756345950\"]").get_by_role(
                "button").click()
            time.sleep(5)
            # Filter the table
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                        name="Parameters").nth(
                1).click()

            # Deselect the previous selected values YEAR
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("#select_8 span").nth(
                1).click()
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                        name="2025").locator(
                "div").first.click()

            # Select the desired year. Default is 2025
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                        name=f"{year_selection}").locator(
                "div").first.click()

            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("md-backdrop").click()

            # Deselect the previous selected values MONTH
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("#select_42 span").nth(
                1).click()
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                        name="ENERO").locator(
                "div").first.click()

            # Select the desired months, to get hourly data only a period of every 4 months can be select at time.
            # Default month is ENERO
            for month in month_list:
                page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                            name=f"{month}").locator(
                    "div").first.click()

            # Select the previous selected values DAY
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("md-backdrop").click()
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("#select_56 span").nth(
                1).click()

            # Select all days from 2 to 31. Day 1 is default selected
            for day in range(2,32):
                page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option", name=f"{day}",
                                                                                                            exact=True).locator(
                    "div").first.click()


            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("md-backdrop").click()
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                        name="Ejecutar").click()
            print('Waiting the table to load...')
            time.sleep(1)

            # Wait for the table to be visible
            table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
                "iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")

            save_name = f"Enero_abril_{year_selection}"
            # Find the table save its content
            save_to_csv(table_locator, save_name)

            """
            See the second list of months
            """

            # Find the parameters button and click it
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                        name="Parameters").nth(
                1).click()
            # Deselect the previous selected values MONTH
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("#select_42 span").nth(
                1).click()
            for month in month_list:
                page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                            name=f"{month}").locator(
                    "div").first.click()

            # Another list of months to select
            for month in month_list_2:
                page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                            name=f"{month}").locator(
                    "div").first.click()

            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("md-backdrop").click()
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                        name="Ejecutar").click()
            print('Waiting the table to load...')
            time.sleep(1)

            # Wait for the table to be visible
            table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
                "iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")

            # Find the table save its content
            save_name = f"Mayo_agosto_{year_selection}"
            save_to_csv(table_locator, save_name)

            """
            See the third list of months
            """

            # Find the parameters button and click it
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                        name="Parameters").nth(
                1).click()
            # Deselect the previous selected values MONTH
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("#select_42 span").nth(
                1).click()
            for month in month_list_2:
                page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                            name=f"{month}").locator(
                    "div").first.click()

            # Another list of months to select
            for month in month_list_3:
                page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                            name=f"{month}").locator(
                    "div").first.click()

            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("md-backdrop").click()
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                        name="Ejecutar").click()
            print('Waiting the table to load...')
            time.sleep(1)

            # Wait for the table to be visible
            table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
                "iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")

            # Find the table save its content
            save_name = f"Septiembre_diciembre_{year_selection}"
            save_to_csv(table_locator, save_name)

            # ---------------------
            context.close()
            browser.close()

    return print('Done Extracting')