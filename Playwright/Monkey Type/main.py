import asyncio

from os import system
from playwright.async_api import Playwright, async_playwright

system("cls")


async def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()

    await page.goto("https://monkeytype.com", timeout=60 * 1000)

    await page.locator("button.acceptAll").click()
    await page.click("body")  # For Focus

    await page.wait_for_selector("#words > div.word.active")

    print("Started Typing ...")
    while True:
        try:
            await page.wait_for_selector(".word:not(.typed)", timeout=2 * 1000)  # 2 Sec
        except:
            print("Time Over ...")
            break

        words = await page.locator(".word:not(.typed)").all_inner_texts()

        text = " ".join(words) + " "
        await page.keyboard.type(text)

    input("Press Enter to Exit ...")
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
