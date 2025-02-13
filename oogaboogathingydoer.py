import bs4
import requests
import time
import re
import random
from main import grabProjectData
import tkinter as tk

# sets the start and end link indexes
def search(start, end):
    for i in range(start, end):
        # get page with studios for each class
        url = 'https://scratch.mit.edu/classes/'+ str(i) +'/studios/'
        page = requests.get(url)
        
        # sleep delay to avoid getting flagged
        time.sleep(random.uniform(0.4, 0.6))

        # grab working studio numbers
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        data = soup.find_all("a", href=re.compile("/studios/"))
        
        # use a set to isolate dupes
        studio_set = set()
        for number in data:
            if(number != 0):
                studio_set.add(number)
        
        # check each studio
        for studio in studio_set:
            # use href to get studio number out of the html
            href = studio.get("href")
            studio_number = href.split("/")[2]

            # request projects from stdio
            url2 = 'https://api.scratch.mit.edu/studios/' + str(studio_number) + '/projects/'
            page2 = requests.get(url2)

            # sleep delay to avoid getting flagged
            time.sleep(random.uniform(0.4, 0.6))

            # download as json to more easily parse ids
            json_data = page2.json()
            for data in json_data:
                with open("output.txt", "a") as file:
                    file.write(str(data['id']) + "\n")

# Create main window
root = tk.Tk()
root.title("Web Scrape")

# Create input fields and labels
tk.Label(root, text="Enter start index:").grid(row=0, column=0)
tk.Label(root, text="Enter end index:").grid(row=1, column=0)

entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)

# Create button to calculate
button = tk.Button(root, text="Start", command=search)
button.grid(row=2, column=0, columnspan=2)

# Run the GUI
root.mainloop()