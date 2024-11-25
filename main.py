import requests
import sqlalchemy
from init import init, Session
from model.user import User
from model.project import Project
import time
import atexit
import signal
# from bs4 import BeautifulSoup

# def grabDataFromURL(url):
#     response = requests.get(url)
#     if response.status_code != 200:
#         print("Did not return success code")
#         print(response.text)
#     soup = BeautifulSoup(response.content,)

currentProjectIndex = open("currentProjectIndex.txt","r")
currentProject = int(currentProjectIndex.read())
currentProjectIndex.close()


projectApiLink = "https://api.scratch.mit.edu/projects/"
testProjectID = [1072618379,938868806,983800322]

def grabProjectData(projectID):
    response = requests.get(projectApiLink+str(projectID))
    
    if response.status_code != 200:
        print("Unable to reach project")
        print(response.text)
        return
    
    data = response.json()
    dbProjectID = projectID
    dbTitle = data["title"]
    dbDesc = data["description"]
    dbAuthor = data["author"]["username"]
    dbCreateOn = data["history"]["created"]
    dbLastMod = data["history"]["modified"]
    dbRemixRoot = data["remix"]["root"]
    dbViews = data["stats"]["views"]
    dbRemixes = data["stats"]["remixes"]
    
    session.add(Project(projectID=dbProjectID,
    title=dbTitle,description=dbDesc,author=dbAuthor,createdOn=dbCreateOn,
    lastModified=dbLastMod,remixRoot=dbRemixRoot,views=dbViews,remixes=dbRemixes))
    session.commit()
    
init()
session = Session()

def saveCurrentIndex(*args):
    currentProjectIndex = open("currentProjectIndex.txt","w")
    currentProjectIndex.write(str(currentProject+1))
    currentProjectIndex.close()

atexit.register(saveCurrentIndex)
signal.signal(signal.SIGTERM, saveCurrentIndex)
signal.signal(signal.SIGINT, saveCurrentIndex)
    
def __del__(self):
    saveCurrentIndex()
    
while True:
    grabProjectData(currentProject)
    currentProject+=1
    time.sleep(0.5)
    
    