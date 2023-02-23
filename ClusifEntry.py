class ClusifEntry:
    def __init__(self,name,links,con):
        
        self.nom = name
        self.coordonnes = links
        self.contact = con

    def getDictEntry(self):
        return {
            "Nom":self.nom,
            "Coordonnees":self.coordonnes,
            "Contact":self.contact,
        }