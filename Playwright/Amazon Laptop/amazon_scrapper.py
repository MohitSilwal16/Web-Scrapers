import re
import csv
from playwright.sync_api import sync_playwright
from os import system
from bs4 import BeautifulSoup
from time import time

system("cls")

"""
    Amazon's Website generate random UUID as id of product's div tag
    Sometimes the product name & price're under 6 elements or under 8 elements
    These elements're either div or span

    HTML Elements doesn't supports number to be first char in id, i.e., #0a is invalid but #a0 is valid
    Since some Google's UUID starts with number, we've to add escape character
    e.g.
    Instead of #0a we've to use #\30 a
    & since '\' is escape char, we've to use #\\30 a

    Using Beautiful Soup to process the HTML which is stored in variable, since fetching data from web-page
    slows down the process

    Playwright is used to interact with Web-Page (Clicking Buttons & Entering Text)
    Beautiful Soup is used to Parse HTML
"""


def fetch_data_from_html_and_write(page_html: str) -> tuple[bool, int]:
    soup = BeautifulSoup(page_html, "html.parser")

    elements = soup.find_all(id=True)

    # Filter those whose ID matches the pattern, i.e. Google's UUID
    matching_elements = [
        element for element in elements if re.match(uuid_pattern, element["id"])
    ]
    print(f"Total Products found on the Webpage: {len(matching_elements)}")

    if len(matching_elements) == 0:
        return (False, 0)

    product_count = 0

    for element in matching_elements:
        product_name = "NOT FOUND"
        product_price = "NOT FOUND"
        product_ratings = "NOT FOUND"

        element_id = element["id"]

        # If 1st char is letter, then use escape chars cuz css selector doesn't supports numeric values as first letter
        if escape_dict.get(element_id[0]):
            first_number = element_id[0]
            element_id = escape_dict[first_number] + " " + element_id[1:]

        is_expection = False
        try:
            product_name = soup.select_one(
                f"#{element_id} > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > div.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right > div > div > div.a-section.a-spacing-none.puis-padding-right-small.s-title-instructions-style > a > h2 > span"
            ).text

            product_price = soup.select_one(
                f"#{element_id} > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > div.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right > div > div > div:nth-child(3) > div.puisg-col.puisg-col-4-of-12.puisg-col-4-of-16.puisg-col-4-of-20.puisg-col-4-of-24 > div > div.a-section.a-spacing-none.a-spacing-top-micro.puis-price-instructions-style > div.a-row.a-size-base.a-color-base > div:nth-child(1) > a > span > span:nth-child(2) > span.a-price-whole"
            ).text

            product_ratings = soup.select_one(
                f"#{element_id} > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > div.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right > div > div > div.a-section.a-spacing-none.a-spacing-top-micro > div > span > a > *:first-child > span"
            ).text
            product_count += 1
        except:
            is_expection = True

        if is_expection:
            try:
                product_name = soup.select_one(
                    f"#{element_id} > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > div.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right > div > div > div.a-section.a-spacing-none.puis-padding-right-small.s-title-instructions-style > a > h2 > span"
                ).text

                product_price = soup.select_one(
                    f"#{element_id} > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > div.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right > div > div > div:nth-child(3) > div.puisg-col.puisg-col-4-of-12.puisg-col-4-of-16.puisg-col-4-of-20.puisg-col-4-of-24 > div > div.a-section.a-spacing-none.a-spacing-top-micro.puis-price-instructions-style > div.a-row.a-size-base.a-color-base > div:nth-child(1) > a > span > span:nth-child(2) > span.a-price-whole"
                ).text

                product_ratings = soup.select_one(
                    f"#{element_id} > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > *:first-child > div.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right > div > div > div.a-section.a-spacing-none.a-spacing-top-micro > div > span > a > *:first-child > span"
                ).text
                product_count += 1
            except:
                pass

        if product_ratings != "NOT FOUND":
            product_ratings = product_ratings.split()[0]

        if product_name == "NOT FOUND":
            continue

        with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([product_name, product_price, product_ratings])

    print(f"Products Successfully Retrieved: {product_count}")
    return (True, product_count)


uuid_pattern = r"[a-f0-9\-]{36}"

escape_dict = {
    "0": "\\30",
    "1": "\\31",
    "2": "\\32",
    "3": "\\33",
    "4": "\\34",
    "5": "\\35",
    "6": "\\36",
    "7": "\\37",
    "8": "\\38",
    "9": "\\39",
}


product_type = input(
    "Enter Electronic Device(e.g., Laptop, Mobile, Smartwatch, etc.): "
)

file_name = f"Amazon {product_type} Data.csv"

# Clear all previous data
with open(file_name, "w") as file:
    file.write("Name, Price, Ratings\n")


with sync_playwright() as p:
    print("\nStarting Scrapping ...")
    start_time = time()

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://amazon.in")
    print("Main WebPage Visited")

    page.fill("#twotabsearchtextbox", product_type)
    page.click("#nav-search-submit-button")

    page.wait_for_load_state("domcontentloaded")
    print("Products Page Visited\n")

    page_count = 1
    product_count = 0
    no_more_data = False

    while page_count <= 20:
        print(f"\nPage {page_count}")
        page.wait_for_load_state("domcontentloaded")

        try:
            # Wait for Products to Load & then fetch Data
            page.wait_for_selector(
                "#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > :nth-child(17)"
            )
            page.wait_for_selector(
                "#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > :nth-child(40)"
            )
        except:
            pass

        page_html = page.content()
        ret = fetch_data_from_html_and_write(page_html)
        # ret[0]: Did this Page had data
        # ret[1]: Count of Products which data was completely fetched successfully

        product_count += ret[1]
        if not ret[0]:
            print("This Page didn't have Data\n")
            continue

        if page_count == 20:
            print("\nNo Additional Pages\n")
            break

        try:
            page.click(
                ".s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-button-accessibility.s-pagination-separator"
            )
        except:
            print("\nNo Additional Pages\n")
            break
        page_count += 1

    end_time = time()
    print(f"Total Complete Product Count: {product_count}")
    print(f"Time Taken: {end_time - start_time:.2f} \n")

    while True:
        if input("Enter 'q' to Quit: ") == "q":
            break

    browser.close()
