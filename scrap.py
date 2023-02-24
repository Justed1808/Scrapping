import requests as rq
from bs4 import BeautifulSoup
from Scrapping import Scrapping
from clusif import Clusif

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
    left = soup.find("div", {"class" : "more-content"})
    infos = left.findAll("p")

    city = ""
    adr = ""
    activity = ""
    post = ""
    name = ""
    site = ""
    for i in infos:
        infosTries = tryToCleanOrReturnBlank(i)
        for i in range(len(infosTries.split("'"))):
            if "Activité" in infosTries.split("'")[i]:
                activity = infosTries.split("'")[i].replace('Activité : ', '')
                name = tryToCleanOrReturnBlank(soup.find("h1", {"class" : "title-page"}))

            elif "Adresse" in infosTries.split("'")[i]:
                adr = infosTries.split("'")[i].replace('Adresse : ', '')

            elif "Code postal" in infosTries.split("'")[i]:
                post = infosTries.split("'")[i].replace('Code postal : ', '')

            elif "Ville" in infosTries.split("'")[i]:
                city = infosTries.split("'")[i].replace('Ville : ', '')

            elif "Site web" in infosTries.split("'")[i]:
                site = infosTries.split("'")[i].replace('Site web : ', '')
            

    tab = soup.find("div", {"class" : "content"})
    right = tab.findAll("p")
    tel = ""
    mail = ""
    for p in right:
        infosTries = tryToCleanOrReturnBlank(p)
        for j in range(len(infosTries.split("'"))):
            if "Téléphone" in infosTries.split("'")[j]:
                tel = infosTries.split("'")[j].replace('Téléphone : ', '')

            if "Email" in infosTries.split("'")[j]:
                mail = infosTries.split("'")[j].replace('Email : ', '')


    if(name != "" and activity != "" and adr != "" and post != "" and city != "" and tel != "" and mail != ""):
        fiches.append ({
            "Nom" : name,
            "Activité" : activity,
            "Adresse" : adr,
            "Code Postal" : post,
            "Ville" : city,
            "Téléphone" : tel,
            "Email" : mail,
            "Site" : site
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

fields = ["Nom", "Activité", "Adresse", "Code Postal", "Ville", "Téléphone", "Email", "Site"]
fileWriter('infos.csv', fields, lignes)
