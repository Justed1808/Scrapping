class ClusifEntry:
    def __init__(self,name,activity,adr,post,city,tel,mail,site):
        
        self.name = name
        self.activity = activity
        self.adr = adr
        self.post = post
        self.city = city
        self.tel = tel
        self.mail = mail
        self.site = site

    def getDictEntry(self):
        return {
            "Nom" : self.name,
            "Activité" : self.activity,
            "Adresse" : self.adr,
            "Code Postal" : self.post,
            "Ville" : self.city,
            "Téléphone" : self.tel,
            "Email" : self.mail,
            "Site" : self.site
        }