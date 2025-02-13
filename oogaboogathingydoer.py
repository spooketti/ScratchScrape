import bs4
import json
import matplotlib.pyplot as plt
import os
import requests
import re
import random
import sqlalchemy as db
import time
import tkinter as tk

from init import init, Session, db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def search():
    # sets the start and end link indexes
    start = (int)(entry1.get())
    end = (int)(entry2.get())

    # print("bounds acquired", start, end)

    for i in range(start, end):
        status_label.config(text="Currently On Class:" + str(i))
        root.update()
        
        # get page with studios for each class
        url = 'https://scratch.mit.edu/classes/'+ str(i) +'/studios/'
        page = requests.get(url)
        
        # sleep delay to avoid getting flagged
        time.sleep(random.uniform(0.4, 0.6))

        # print("page acquired")

        # grab working studio numbers
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        data = soup.find_all("a", href=re.compile("/studios/"))
        
        # use a set to isolate dupes
        studio_set = set()
        for number in data:
            if(number != 0):
                studio_set.add(number)
        
        # print("checking studio_set")
 
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

            # print("being json data parse")

            # download as json to more easily parse ids
            json_data = page2.json()
            for data in json_data:
                # with open("output.txt", "a") as file:
                #     file.write(str(data['id']) + "\n")
                logicComplexity["totalProjectsScraped"] += 1
                curr_project = requests.get("https://api.scratch.mit.edu/projects/" + str(data['id'])).json()

                # grabProjectData(curr_project['id'])
                processProjectFile(curr_project['id'], curr_project['project_token'], start, end)
            
            # print("json data parse end")
    
    root.destroy()
    graphAndSave(start, end)


logicComplexity = {"repeat":0, #
                   "variables":0,
                   "functions":0,
                   "conditionals":0,
                   "arithmetic":0,
                   "comparison":0, # < > =
                   "complexMath":0, #anything in the menu that lets you do cos sin atan etc
                   "scriptCount":0,
                   "totalProjectsScraped":0} #defined by how many blocks have no parents (start of a script)

def processProjectFile(projectId, projectToken, start, end):
    file = requests.get("https://projects.scratch.mit.edu/"+str(projectId)+"?token="+str(projectToken))
    data = file.json()

    try:
        numOfSprites = len(data['targets'])
    except:
        print("too old")
    else:
        blocks_with_no_parent = list()

        for i in range(numOfSprites):
            def followCodeChain(blockData):
                if(blockData["opcode"] in ["control_repeat","control_repeat_until"] ):
                    logicComplexity["repeat"] += 1
                #i dont know how to find functions so u can have fun james
                
                if(blockData["opcode"] in ["control_if", "control_if_else"]):
                    logicComplexity["conditionals"] += 1
                    
                if(blockData["opcode"] in ["operator_add", "operator_subtract", "operator_multiply", "operator_divide"]):
                    logicComplexity["arithmetic"] += 1
                
                if(blockData["opcode"] in ["operator_equals", "operator_lt", "operator_gt"]):
                    logicComplexity["comparison"] += 1
                    
                if(blockData["opcode"] in ["operator_mathop"]):
                    logicComplexity['complexMath'] += 1
                
                # followCodeChain(data["targets"][i]["blocks"][blockData["next"]])
                
            logicComplexity["variables"] += len(data["targets"][i]["variables"])

            blocks = data['targets'][i]['blocks']
            # print(data["targets"][i]["name"])
            
            try:
                blocks_with_no_parent = list(filter(lambda item: item[1].get("parent") is None, blocks.items()))
            except:
                logicComplexity["scriptCount"] += 0
            else:
                logicComplexity["scriptCount"] += len(blocks_with_no_parent)
            
            for j in blocks:
                followCodeChain(blocks[j])

def graphAndSave(start, end):
    print(logicComplexity)

    filename = os.path.join("./data/", str(start)+"To"+str(end)+"Scrape.json")
    with open(filename, "w") as file:
        json.dump(logicComplexity, file, indent=4)

    plt.bar(range(len(logicComplexity)), list(logicComplexity.values()), align='center')
    plt.xticks(range(len(logicComplexity)), list(logicComplexity.keys()))
    plt.title("Scratch User Project Complexity")
    plt.show()

def scrape():
    # Create main window
    root.title("Web Scrape")

    # Create input fields and labels
    tk.Label(root, text="Enter start index(Note that 5 years ago was 255000):").grid(row=0, column=0)
    tk.Label(root, text="Enter end index:").grid(row=1, column=0)

    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)

    status_label.grid(row=3, column=0, columnspan=2)

    # Create button to calculate
    button = tk.Button(root, text="Start", command=search)
    button.grid(row=2, column=0, columnspan=2)

    # Run the GUI
    root.mainloop()

# init()
# session = Session()

root = tk.Tk()
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
status_label = tk.Label(root, text="Waiting for Input")
start, end = 0, 0

scrape()
