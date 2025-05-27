from rich import print
import time
from playwright.sync_api import Playwright, sync_playwright, expect
import csv
import datetime


month_list = ['MAYO']
save_name = "Mayo_2025"

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
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                    name="2024").locator(
            "div").first.click()

        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("md-backdrop").click()

        # Deselect the previous selected values MONTH
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("#select_42 span").nth(
            1).click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                    name="ENERO").locator(
            "div").first.click()

        for month in month_list:
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option",
                                                                                                        name=f"{month}").locator(
                "div").first.click()

        # Select the previous selected values DAY
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("md-backdrop").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("#select_56 span").nth(
            1).click()
        for day in range(2,32):
            page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("option", name=f"{day}",
                                                                                                        exact=True).locator(
                "div").first.click()


        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator("md-backdrop").click()
        page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.get_by_role("button",
                                                                                                    name="Ejecutar").click()
        print('Lets see the table')
        time.sleep(1)
        table_locator = page.locator("#iframeDoc").content_frame.locator("iframe").nth(1).content_frame.locator(
            "iframe[name=\"documentFrame\"]").content_frame.get_by_role("table")

        # Extract the table content
        table_content = table_locator.inner_text()
        print("SEE TABLE CONTENT, EXTRACTING...")
        print(table_content)
        # Lest save the table content
        lines = table_content.strip().split("\n")
        print("lines")
        print(lines)

        with open(f'{save_name}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write each line to the CSV file
            for line in lines:
                # Split the line by whitespace and write to the CSV file
                writer.writerow(line.split())

        print('Done writing the table to CSV')
        # ---------------------
        context.close()
        browser.close()