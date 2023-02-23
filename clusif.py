from Toolkit import Toolkit
from ClusifEntry import ClusifEntry

class Clusif:
    def __init__(self, baseUrl, uri):
        self.baseUrl = baseUrl
        self.uri = uri
        self.urls = []
        self.endpoints = []
        self.result = []
        self.finalFileNameFields = ["Nom", "coordonnes", "Contact"]

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
        name = Toolkit.tryToCleanOrReturnBlank(soup.find("h1", {"class" : "title-page"}))

        left = soup.find("div", {"class" : "more-content"})
        infos = left.findAll("p")
        links = []
        for i in infos:
            infosTries = Toolkit.tryToCleanOrReturnBlank(i)
            links.append(infosTries)

        tab = soup.find("div", {"class" : "content"})
        right = tab.findAll("p")
        con = []
        for p in right:
            infosTries = Toolkit.tryToCleanOrReturnBlank(p)
            con.append(infosTries)

        fiches.append ({
            "Nom" : name,
            "coordonnes" : links,
            "Contact" : con
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