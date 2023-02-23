import requests 
from bs4 import BeautifulSoup 
from Toolkit import Toolkit

class Scrapping:
    def __init__(self, ScrapInstance, linkFile, finalFile):
        self.setScrapInstance(ScrapInstance)
        self.setFinalFile(finalFile)
        self.setLinkFile(linkFile)
        self.finalFileNameFields = self.ScrapInstance.getFinalFieldNames()
        self.linkFileNameFields = ['id', 'category','link']

    def setScrapInstance(self, instance):
        self.ScrapInstance = instance
        return self

    def setLinkFile(self, filePath):
        self.linkFile = filePath
        return self

    def setFinalFile(self, filePath):
        self.finalFile = filePath
        return self

    def swoup(self, url, process):
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                return process(soup)
            except Exception:
                return False
        else:
            return False
        return

    def swoupMultiple(self, urls, process):
        result = []
        for url in urls:
            soup = self.swoup(url, process)
            if hasattr(soup, '__len__'):
                result.extend(soup)
            else: 
                result.append(soup)
        return result

    def exec(self):

        i = 0
        rows= []
        for url in self.ScrapInstance.getEndpoints():
            row = {}
            row["link"] = url
            row["category"] = "$category$"
            row['id'] = i
            i += 1
            rows.append(row)
        Toolkit.fileWriter(self.linkFile, self.linkFileNameFields, rows )

        self.swoupMultiple(self.ScrapInstance.getEndpoints(), self.ScrapInstance.getInfoByPage )
        Toolkit.fileWriter(self.finalFile, self.finalFileNameFields, self.ScrapInstance.getDictResult() )