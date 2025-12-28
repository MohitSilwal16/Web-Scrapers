import html
import requests

from bs4 import BeautifulSoup
from os import system

system("cls")

print("Fetching Data ...")
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1jwG5iXTPLccpFhpT4sGsWn0frYTkjE5xfMVPXZ4BCRTbEktM79LEB5-tQV4y5Q/pubhtml?gid=1463439233&single=true"

res = requests.get(url)
print("Data Fetched Successfully ...")

soup = BeautifulSoup(res.content, "html.parser")
innerHTML = soup.select_one(selector="#\\31 463439233 > div > table").decode_contents()

rows = innerHTML.split("</tr>")
lenRows = len(rows)

fileName = "Mid-Sem-1 Sem-5.csv"

file_content = ""

with open(fileName, "w") as file:
    file.write("")

print("Processing Data ...")

for i in range(lenRows):
    num = ""
    branch = ""
    en_num = ""
    name = ""
    sub1 = ""
    sub2 = ""
    sub3 = ""
    sub4 = ""
    sub5 = ""

    cols = rows[i].split("</td>")

    try:
        num = soup.select_one(
            selector=f"#\\31 463439233 > div > table > tbody > tr:nth-child({i}) > td:nth-child(3)"
        ).decode_contents()
        branch = soup.select_one(
            selector=f"#\\31 463439233 > div > table > tbody > tr:nth-child({i}) > td:nth-child(4)"
        ).decode_contents()
        en_num = soup.select_one(
            selector=f"#\\31 463439233 > div > table > tbody > tr:nth-child({i}) > td:nth-child(5)"
        ).decode_contents()
        name = soup.select_one(
            selector=f"#\\31 463439233 > div > table > tbody > tr:nth-child({i}) > td:nth-child(6)"
        ).decode_contents()
        sub1 = soup.select_one(
            selector=f"#\\31 463439233 > div > table > tbody > tr:nth-child({i}) > td:nth-child(7)"
        ).decode_contents()
        sub2 = soup.select_one(
            selector=f"#\\31 463439233 > div > table > tbody > tr:nth-child({i}) > td:nth-child(8)"
        ).decode_contents()
        sub3 = soup.select_one(
            selector=f"#\\31 463439233 > div > table > tbody > tr:nth-child({i}) > td:nth-child(9)"
        ).decode_contents()
        sub4 = soup.select_one(
            selector=f"#\\31 463439233 > div > table > tbody > tr:nth-child({i}) > td:nth-child(10)"
        ).decode_contents()
        sub5 = soup.select_one(
            selector=f"#\\31 463439233 > div > table > tbody > tr:nth-child({i}) > td:nth-child(11)"
        ).decode_contents()
        sub6 = soup.select_one(
            selector=f"#\\31 463439233 > div > table > tbody > tr:nth-child({i}) > td:nth-child(12)"
        ).decode_contents()

        sub1 = html.unescape(sub1)
        sub2 = html.unescape(sub2)
        sub3 = html.unescape(sub3)
        sub4 = html.unescape(sub4)
        sub5 = html.unescape(sub5)
        sub6 = html.unescape(sub6)

        if branch == "":
            file_content += "\n"
        else:
            file_content += f"{num},{branch},{en_num},{num},{
                name},{sub1},{sub2},{sub3},{sub4},{sub5},{sub6}\n"

    except:
        pass

with open(fileName, "w") as file:
    file.write(file_content)

print("Data Added Successfully into", fileName)
