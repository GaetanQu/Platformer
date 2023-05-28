import csv
'''
Le but ici est d'enregistrer les settings sur un fichier et de les mettre dans une liste au lancement du programme.
Il sera possible de les actualiser

Les lignes ressembleront a ca :

    parametre;valeur
'''

def read():

    #On cree d'abord le dictionnaire qui va contenir les parametres
    setting = {}

    # Ouvre settings.csv en mode lecture
    with open("Settings.csv", 'r') as fichier:
        csv_reader = csv.reader(fichier, delimiter=';')
        for parametre in csv_reader:
            setting[parametre[0]] = parametre[1]

    return setting
