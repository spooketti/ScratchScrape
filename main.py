import requests
import sqlalchemy
# from bs4 import BeautifulSoup

# def grabDataFromURL(url):
#     response = requests.get(url)
#     if response.status_code != 200:
#         print("Did not return success code")
#         print(response.text)
#     soup = BeautifulSoup(response.content,)

projectApiLink = "https://api.scratch.mit.edu/projects/"

def grabProjectData(projectID):
    response = requests.get(projectApiLink+projectID)
    
    if response.status_code != 200:
        print("Unable to reach project")
        print(response.text)
        return
    
    data = response.json()
    
    