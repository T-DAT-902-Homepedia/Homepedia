import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import time

# --- Connexion MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["homepedia"]
collection = db["villes"]

# --- Chargement du fichier des communes ---
communes = pd.read_csv("20230823-communes-departement-region.csv", dtype=str)
print(f"Nombre de communes : {len(communes)}")

# --- Fonction pour construire l'URL ---
def construire_url(nom, code_insee):
    # "L ABERGEMENT CLEMENCIAT" → "l-abergement-clemenciat"
    nom_formate = nom.lower().replace(" ", "-")
    return f"https://www.ville-ideale.fr/{nom_formate}_{code_insee}"

# --- Fonction pour scraper une ville ---
def scraper_ville(url, nom_ville):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        # Si la page n'existe pas on passe
        if response.status_code != 200:
            print(f"❌ Page introuvable : {url}")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")

        # Note globale
        note_tag = soup.find("p", id="ng")
        if not note_tag:
            print(f"⚠️ Pas de note pour {nom_ville}")
            return None
        note = note_tag.text.split("/")[0].strip()

        # Notes par critère
        criteres = {}
        table = soup.find("table", id="tablonotes")
        if table:
            for row in table.find_all("tr"):
                th = row.find("th")
                td = row.find("td")
                if th and td:
                    criteres[th.text.strip()] = td.text.strip()

        return {
            "ville": nom_ville,
            "url": url,
            "note_globale": note,
            "criteres": criteres
        }

    except Exception as e:
        print(f"❌ Erreur pour {nom_ville} : {e}")
        return None

# --- On teste sur les 5 premières villes ---
for index, row in communes.iterrows():
    nom = row["nom_commune_postal"]
    code_insee = row["code_commune_INSEE"]
    
    url = construire_url(nom, code_insee)
    print(f"Scraping : {nom} → {url}")
    
    data = scraper_ville(url, nom)
    
    if data:
        collection.insert_one(data)
        print(f"✅ {nom} stocké dans MongoDB")
    
    # Pause de 2 secondes entre chaque requête
    # pour ne pas surcharger le serveur
    time.sleep(0.5)

print("\nTerminé !")