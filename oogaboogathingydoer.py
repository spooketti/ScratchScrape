from bs4 import BeautifulSoup
import requests
import time
import re
import random
from main import grabProjectData

start, end = 1000, 1001
studio_set, project_set = set(), set()

for i in range(start, end):
    url = 'https://scratch.mit.edu/classes/'+ str(i) +'/studios/'
    page = requests.get(url)
    time.sleep(random.uniform(0.4, 0.6))

    soup = BeautifulSoup(page.text, 'html.parser')

    data = soup.find_all("a", href=re.compile("/studios/"))
    for number in data:
        if(number != 0):
            studio_set.add(number)

    time.sleep(0.5)

    for studio in studio_set:
        href = studio.get("href")
        studio_number = href.split("/")[2]
        # print(studio_number)

        url2 = 'https://api.scratch.mit.edu/studios/' + str(studio_number) + '/projects/'
        page2 = requests.get(url2)
        time.sleep(random.uniform(0.4, 0.6))

        json_data = page2.json()
        # print(len(json_data))
        for data in json_data:
            with open("output.txt", "a") as file:
                file.write(str(data['id']) + "\n")
