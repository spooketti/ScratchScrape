import requests
import sqlalchemy
from init import init, Session
from model.user import User
from model.project import Project
# from bs4 import BeautifulSoup

# def grabDataFromURL(url):
#     response = requests.get(url)
#     if response.status_code != 200:
#         print("Did not return success code")
#         print(response.text)
#     soup = BeautifulSoup(response.content,)

projectApiLink = "https://api.scratch.mit.edu/projects/"
testProjectID = [1072618379,938868806]

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
    dbAuthor = data["author"]["id"]
    dbCreateOn = data["history"]["created"]
    
    session.add(Project(projectID=dbProjectID,
    title=dbTitle,description=dbDesc,author=dbAuthor,createdOn=dbCreateOn))
    session.commit()
    
init()
session = Session()
grabProjectData(938868806)