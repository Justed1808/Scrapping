import requests as rq
from bs4 import BeautifulSoup
from Scrapping import Scrapping
from Clusif import Clusif

import csv

baseUrl = 'https://clusif.fr'
uri = "/services/annuaire-des-prestataires/"

'''
clusifInstance = Clusif(baseUrl, uri)

scraper = Scrapping(clusifInstance, "links.csv", "infos.csv")

scraper.exec()

print("Done")

'''
response = rq.get(baseUrl + uri)

def getEndPoints(swoup):

    links = []
    div = (swoup.find("div", {"class" : "col-page list"}))
    ahref = div.findAll("a")
    for a in ahref:
        links.append(a ["href"])
    
    return links

def tryToCleanOrReturnBlank(str):
    try:
        result = str.getText().strip()
    except:
        result = ''
    return result

def getInfosByPage(soup):
    fiches = []
    name = tryToCleanOrReturnBlank(soup.find("h1", {"class" : "title-page"}))

    left = soup.find("div", {"class" : "more-content"})
    infos = left.findAll("p")
    links = []
    city = ""
    for i in infos:
        infosTries = tryToCleanOrReturnBlank(i)
        for i in range(len(infosTries.split("'"))):
            if "Ville" in infosTries.split("'")[i]:
                city = infosTries.split("'")[i]
                links.append(infosTries)
            if "Adresse" in infosTries.split("'")[i]:
                links.append(infosTries)

    print(city)

    tab = soup.find("div", {"class" : "content"})
    right = tab.findAll("p")
    con = []
    for p in right:
        infosTries = tryToCleanOrReturnBlank(p)
        con.append(infosTries)

    fiches.append ({
        "Nom" : name,
        "coordonnes" : links,
        "Contact" : con
    })
    return fiches

def swoup(url, process):
    response = rq.get(url)
    if response.ok:
        #print("yes")
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
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for d in data:
            writer.writerow(d)

endpoints = swoup(baseUrl + uri, getEndPoints)

fields = ['lien']
rows = []
for endpoint in endpoints:
    row = {}
    row['lien'] = endpoint
    rows.append(row)
fileWriter('links.csv', fields, rows )

lignes = []
for link in fileReader('links.csv'):
    lignes.extend(swoup(link['lien'], getInfosByPage))

fields = ["Nom", "coordonnes", "Contact"]
fileWriter('infos.csv', fields, lignes)
