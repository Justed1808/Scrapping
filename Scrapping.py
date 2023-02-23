class Scraping:
    def __init__(self, ScrapInstance, linkFile, finalFile):
        self.setScrapInstance(ScrapInstance)
        self.setLinkFile(linkFile)
        self.setfinalFile(finalFile)

    def swoup(url, process):
        response = rq.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            return process(soup)
        return []

    def exec(self):
