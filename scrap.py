import requests as rq
from bs4 import BeautifulSoup

baseUrl = 'https://www.studyrama.com'
uri = "/megamoteur/recherche?query=developpement&type=E%20F%20O"

response = rq.get(baseUrl + uri)

if(response.ok):
    print(response.text)
    #swoup = BeautifulSoup()


print(response.ok)