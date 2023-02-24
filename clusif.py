from Toolkit import Toolkit
from ClusifEntry import ClusifEntry

class Clusif:
    def __init__(self, baseUrl, uri):
        self.baseUrl = baseUrl
        self.uri = uri
        self.urls = []
        self.endpoints = []
        self.result = []
        self.finalFileNameFields = ["Nom", "Activité", "Adresse", "Code Postal", "Ville", "Téléphone", "Email", "Site"]

    def setEndpoints(self,soup):
        div = (soup.find("div", {"class" : "col-page list"}))
        ahref = div.findAll("a")
        links = []
        for a in ahref:
            try: 
                links.append(a['href'])
            except:
                pass
        self.endpoints.extend(Toolkit.addBaseUrl(self.baseUrl, links))
        return self.endpoints

    def getEndpoints(self):
        return self.endpoints

    def getFinalFieldNames(self):
        return self.finalFileNameFields
    
    def getInfoByPage(self, soup):

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
            infosTries = Toolkit.tryToCleanOrReturnBlank(i)
            for i in range(len(infosTries.split("'"))):
                if "Activité" in infosTries.split("'")[i]:
                    activity = infosTries.split("'")[i].replace('Activité : ', '')
                    name = Toolkit.tryToCleanOrReturnBlank(soup.find("h1", {"class" : "title-page"}))

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
            infosTries = Toolkit.tryToCleanOrReturnBlank(p)
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
        
        self.result.extend(fiches)
        return fiches
    
    def getResult(self):
        return self.result

    def getDictResult(self):
        result = []
        for res in self.getResult():
            result.append(res.getDictEntry())
        return 