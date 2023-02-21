import requests as rq
from bs4 import BeautifulSoup

baseUrl = 'https://www.studyrama.com'
uri = "/megamoteur/recherche?query=developpement&type=E%20F%20O"

response = rq.get(baseUrl + uri)

if(response.ok):
    swoup = BeautifulSoup(response.text, 'html.parser')
    
    ul = swoup.find("ul", {"class" : "results"})
    lis = ul.findAll("li")
    for li in lis:
        a = li.find("a")
        print(baseUrl + a["href"])

print(response.ok)