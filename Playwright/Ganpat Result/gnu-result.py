import time
import asyncio
from playwright.async_api import Playwright, async_playwright, Page, TimeoutError
from os import system

system("cls")


class Branch:
    def __init__(self, en_numbers: list[int], name: str) -> None:
        self.en_numbers = en_numbers
        self.name = name


def progressBar(progess, total) -> None:
    percentFloat = 100 * (progess / total)
    percentInt = int(100 * (progess / total))

    bar = "█" * percentInt + "-" * (100 - percentInt)
    print(f"\r|{bar}| {percentFloat:.2f} %", end="\r")


async def get_select_options(page: Page, selector: str):
    select_element = await page.query_selector(selector)

    if not select_element:
        raise ValueError(f"Element with selector '{selector}' not found.")

    options = await select_element.query_selector_all("option")

    option_values = [await option.get_attribute("value") for option in options]
    option_texts = [await option.inner_text() for option in options]

    return option_values, option_texts


en_num_file = input("Enter the path of the file of En Numbers: ")

CBA_start_en_number = ""
CBA_end_en_number = ""
CBA_start_D2D_en_number = ""
CBA_end_D2D_en_number = ""

BDA_start_en_number = ""
BDA_end_en_number = ""
BDA_start_D2D_en_number = ""
BDA_end_D2D_en_number = ""
BDA_extra_en_number = ""  # Dhairya Chotu

CS_start_en_number = ""
CS_end_en_number = ""
CS_start_D2D_en_number = ""
CS_end_D2D_en_number = ""
CS_extra_en_number = ""  # Kathan Bharti

CSE_start_en_number = ""
CSE_end_en_number = ""
CSE_start_D2D_en_number = ""
CSE_end_D2D_en_number = ""


# Read En Number Range from en_number.txt
with open("en-num/" + en_num_file, "r") as file:
    lines = file.readlines()

    for line in lines:
        tokens = line.split(",")
        branch = tokens[0]

        match branch:
            case "CBA":
                CBA_start_en_number = tokens[1]
                CBA_end_en_number = tokens[2]
            case "CBA_D2D":
                CBA_start_D2D_en_number = tokens[1]
                CBA_end_D2D_en_number = tokens[2]
            case "BDA":
                BDA_start_en_number = tokens[1]
                BDA_end_en_number = tokens[2]
            case "BDA_D2D":
                BDA_start_D2D_en_number = tokens[1]
                BDA_end_D2D_en_number = tokens[2]
            case "BDA_EXTRA":
                BDA_extra_en_number = tokens[1]
                BDA_extra_en_number = BDA_extra_en_number[:-1]
            case "CS":
                CS_start_en_number = tokens[1]
                CS_end_en_number = tokens[2]
            case "CS_D2D":
                CS_start_D2D_en_number = tokens[1]
                CS_end_D2D_en_number = tokens[2]
            case "CS_EXTRA":
                CS_extra_en_number = tokens[1]
                CS_extra_en_number = CS_extra_en_number[:-1]
            case "CSE":
                CSE_start_en_number = tokens[1]
                CSE_end_en_number = tokens[2]
            case "CSE_D2D":
                CSE_start_D2D_en_number = tokens[1]
                CSE_end_D2D_en_number = tokens[2]


cba_list = [i for i in range(int(CBA_start_en_number), int(CBA_end_en_number) + 1)] + [
    i for i in range(int(CBA_start_D2D_en_number), int(CBA_end_D2D_en_number) + 1)
]
cba = Branch(en_numbers=cba_list, name="CBA")

bda_list = [i for i in range(int(BDA_start_en_number), int(BDA_end_en_number) + 1)] + [
    i for i in range(int(BDA_start_D2D_en_number), int(BDA_end_D2D_en_number) + 1)
]
bda_list.append(BDA_extra_en_number)  # Add Dhairya's En Number
bda = Branch(en_numbers=bda_list, name="BDA")

cs_list = [i for i in range(int(CS_start_en_number), int(CS_end_en_number) + 1)] + [
    i for i in range(int(CS_start_D2D_en_number), int(CS_end_D2D_en_number) + 1)
]
cs_list.append(CS_extra_en_number)  # Add Bharti's En Number
cs = Branch(en_numbers=cs_list, name="CS")

cse_list = (
    [i for i in range(int(CSE_start_en_number), int(CSE_end_en_number) + 1)]
    + [i for i in range(int(CSE_start_D2D_en_number), int(CSE_end_D2D_en_number) + 1)]
    if CSE_start_en_number
    else []
)
cse = Branch(en_numbers=cse_list, name="CSE")

branches = [cs, cba, bda, cse]
sem = input("Enter Semester(In Capital Roman): ")


async def run(playwright: Playwright):
    start = time.time()
    chromium = playwright.chromium
    browser = await chromium.launch()
    page = await browser.new_page()

    totalStudents = len(cba_list) + len(bda_list) + len(cse_list) + len(cs_list)
    counter = 0

    await page.goto("https://result.ganpatuniversity.ac.in/")
    await page.select_option("#ddlInst", value="16 - ICT")
    await page.select_option("#ddlDegree", value="B.TECH-CSE(BDA)")
    await page.select_option("#ddlSem", value=sem)

    # Get all option elements within the select tag
    await page.wait_for_selector("#ddlScheduleExam")
    options = await page.locator(f"{"#ddlScheduleExam"} option").all()

    options_data = []
    options_len = len(options)
    print("\nExam Schedules: ")
    for i in range(1, options_len):
        text = await options[i].text_content()
        text = text.strip()
        options_data.append(text)
        print(f"{i} - {text}")

    while True:
        try:
            exam = int(input("\nSelect an Option: "))
        except:
            print("Only Integers")
            continue

        if exam >= 1 and exam <= options_len - 1:
            schedule_exam = options_data[exam - 1]
            break
        print("Lavde, sahi value select krna")

    fileName = f"data/{en_num_file.split(".")[0]} Sem-{sem}.csv"

    # Initialize file with empty data
    with open(fileName, "w") as file:
        data = "Branch,En Number,Name, SGPA, CGPA(Total)"
        file.write(data)

    print("\nFetching Data ...")

    for branch in branches:
        if branch.name == "CSE":
            await page.select_option("#ddlDegree", value="B.TECH-CSE")
        else:
            await page.select_option("#ddlDegree", value=f"B.TECH-CSE({branch.name})")

        # Try-Catch cuz seniors didn't have "CSE" Branch
        try:
            await page.select_option("#ddlSem", value=sem, timeout=5000)
        except:
            pass

        for enNumber in branch.en_numbers:
            counter += 1
            try:
                await page.select_option("#ddlScheduleExam", value=schedule_exam)
                await page.fill("#txtEnrNo", str(enNumber))
                await page.click("#btnSearch")

                # Timeout = 1 second
                name = await page.inner_text("#uclGrd_lblStudentName", timeout=1000)
                sgpa = await page.inner_text("#uclGrd_lblSGPA", timeout=1000)
                cgpa = await page.inner_text("#uclGrd_lblPrgCGPA", timeout=1000)

                with open(fileName, "a") as file:
                    data = f"\n{branch.name},{
                        str(enNumber)},{name},{sgpa},{cgpa}"
                    file.write(data)

                progressBar(counter, totalStudents)
            except TimeoutError as e:
                # Ignore this Exception, since some En No.s're Invalid
                progressBar(counter, totalStudents)
            except Exception as e:
                print(f"Error: {e}")

            await page.go_back()
        with open(fileName, "a") as file:
            file.write("\n")

    await browser.close()
    print(f"\n\nData fetched check {fileName}")
    print(f"Time Taken: {time.time()-start:.2f} seconds")


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
