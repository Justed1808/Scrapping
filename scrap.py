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
        print("yes")
        soup = BeautifulSoup(response.text, 'html.parser')
        return process(soup)
    return []

def fileReader(file):
    result = []
    with open(file, 'r', encoding="UTF8", newline="") as f:
        reader = csv.DictReader(f)
        for line in reader:
            result.append(line)
    return result


def fileWriter(file, fieldnames, data):
    result = []
    with open(file, 'w', encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return fileReader(file)

data = fileReader("links.csv")

fields = ['test']
fileWriter('infos.csv', fields, data)
exit()

endpoints = swoup(baseUrl + uri, getEndPoints)


print(endpoints)
result = []
for endpoint in endpoints:
    result.extend(swoup(endpoint, getInfosByPage))

print(result)

