import requests as rq
from bs4 import BeautifulSoup

import csv

baseUrl = 'https://clusif.fr'
uri = "/services/annuaire-des-prestataires/"

response = rq.get(baseUrl + uri)

def getEndPoints(swoup):

    links = []
    div = swoup.find("div", {"class" : "col-page list"})
    ahref = div.findAll("a")
    for a in ahref:
        links.append(a ["href"])
    
    return links

def getInfosByPage(swoup):
    infosTries = [swoup]
    return infosTries

def swoup(url, process):
    response = rq.get(url)
    if response.ok:
        #print("yes")
        soup = BeautifulSoup(response.text, 'html.parser')
        return process(soup)
    return []

def fileWriter(file, fieldnames, data):
    result = []
    with open(file, 'w', encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d in data:
            writer.writerow(d)



endpoints = swoup(baseUrl + uri, getEndPoints)

result = []
for endpoint in endpoints:
    result.append({"link" : endpoint})


fields = ['link']
fileWriter('infos.csv', fields, result)