from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://xoso.com.vn/xsmb-5000-ngay.html")

while True:
    try:
        driver.find_element(by=By.XPATH, value='//*[@id="loadmore"]').click()
        break
    except:
        print("error")
        time.sleep(2)
        continue

time.sleep(20)
website_html = BeautifulSoup(driver.page_source, "html.parser")
days = website_html.select(".result-flex")

header = "date"
for i in range(1, 28):
    header = header + "," + str(i)

def format(string):
    string = string.replace(",-", "")
    string = string.replace("-,", "")
    for ind in range(len(string) - 1, -1, -1):
        if string[ind] == '(':
            rep = int(string[ind + 1])
            num = string[(ind - 2) : ind]
            trans = ""
            for i in range(0, rep):
                trans = trans + num + ","
            trans = trans[:-1]
            string = string.replace(string[(ind - 2) : (ind + 3)], trans)
    arr = []
    for ind in range(0, len(string), 3):
        arr.append(int(string[ind: ind + 2]))
    arr.sort()
    string = ""
    for num in arr:
        string = string + str(num) + ","
    return string[: -1]

all_result = ""

for row in days:
    data = row.select(".table-loto tbody tr td")
    result = ""
    for each in data:
        text = each.getText() 
        result = result + each.getText().replace(" ", "") + ","
    date = row.select(".head-th a")[1]
    result = date.getText() + "," + format(result[:-1])
    all_result = all_result + result + "\n"

with open('data.csv', mode='w') as file:
    file.write(header)
    file.write("\n")
    file.write(all_result)
