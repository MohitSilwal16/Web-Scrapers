from pandas import read_excel, read_csv
from playwright.sync_api import sync_playwright

from os import system

system("cls")


def progress_bar(progess: int, total: int) -> None:
    percentFloat = 100 * (progess / total)
    percentInt = int(100 * (progess / total))

    bar = "█" * percentInt + "-" * (100 - percentInt)
    print(f"\r|{bar}| {percentFloat:.2f} % ({progess:,} rows)", end="\r")


TIMEOUT = 5000  # ms

df = read_excel("NORTH BONDI NSW.xlsx")
url = "https://www.google.co.in/maps/dir/North+Bondi+NSW+2026,+Australia//@-33.8856508,151.2394267,13z/data=!4m8!4m7!1m5!1m1!1s0x6b12ad9780a4ff57:0x5017d681632c3a0!2m2!1d151.280712!2d-33.8857289!1m0?entry=ttu&g_ep=EgoyMDI1MDQxMy4wIKXMDSoASAFQAw%3D%3D"

number = int(input("Enter row number: "))
headless = input("Enter 'Y' if you want to Display Browser: ").upper() != "Y"

OUTPUT_FILE_NAME = f"Output {number}.csv"
with open(OUTPUT_FILE_NAME, "w") as file:
    file.write("Location,Hour,Min,Distance\n")

with sync_playwright() as p:
    print("Starting Scrapping ...")
    browser = p.chromium.launch(headless=headless)
    page = browser.new_page()
    c = 0
    n = len(df)

    page.goto(url)
    for _, row in df.iterrows():
        c += 1
        if c < number - 1:
            continue
        # temp = f"{row["Location"]} {row["State"]} {row["Postcode"]}"
        temp = f"{row["Suburb.1"]} {row["Zone Abbreviation.1"]} {row["Postcode.1"]}"

        page.fill("#sb_ifc51 > input", temp)
        page.press("#sb_ifc51 > input", "Enter")

        try:
            time = page.inner_text(
                "#section-directions-trip-0 > div.MespJc > div > div.XdKEzd > div.Fk3sm.fontHeadlineSmall.delay-light",
                timeout=TIMEOUT,
            )
            hr = "0 hr"
            minute = time
            if time.find("hr") != -1:
                hr, minute = time.split("hr")
                hr += "hr"

            distance = page.inner_text(
                "#section-directions-trip-0 > div.MespJc > div > div.XdKEzd > div.ivN21e.tUEI8e.fontBodyMedium > div",
                timeout=TIMEOUT,
            )
            data = f"{row["Suburb.1"]},{hr},{minute},{distance}\n"
            with open(OUTPUT_FILE_NAME, "a") as file:
                file.write(data)

            progress_bar(c, n)
        except Exception as err:
            progress_bar(c, n)
            # print(f"Error for {row["Suburb.1"]}: {err}")
            with open(OUTPUT_FILE_NAME, "a") as file:
                file.write(f"{row["Suburb.1"]},,,\n")

    print("Scrapping Completed ...")
    browser.close()
