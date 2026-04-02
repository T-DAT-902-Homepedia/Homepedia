import pandas as pd
import mysql.connector

# --- Connexion MySQL ---
conn = mysql.connector.connect(
    host="localhost",
    user="homepedia",
    password="homepedia123",
    database="homepedia"
)
cursor = conn.cursor()

# --- Chargement du CSV ---
print("Chargement du CSV...")
df = pd.read_csv("KaDo.csv")
print(f"Nombre de lignes : {len(df)}")
print(df.head())

# --- Import des clients ---
print("\nImport des clients...")
clients = df[["CLI_ID"]].drop_duplicates()
for _, row in clients.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO clients (CLI_ID)
        VALUES (%s)
    """, (int(row["CLI_ID"]),))
conn.commit()
print(f"✅ {len(clients)} clients importés")

# --- Import des produits ---
print("\nImport des produits...")
produits = df[["LIBELLE", "FAMILLE", "UNIVERS", "MAILLE"]].drop_duplicates()
for _, row in produits.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO produits (LIBELLE, FAMILLE, UNIVERS, MAILLE)
        VALUES (%s, %s, %s, %s)
    """, (row["LIBELLE"], row["FAMILLE"], row["UNIVERS"], row["MAILLE"]))
conn.commit()
print(f"✅ {len(produits)} produits importés")

# --- Import des tickets ---
print("\nImport des tickets...")

# On prépare toutes les données en une liste
tickets_data = [
    (int(row["TICKET_ID"]), int(row["MOIS_VENTE"]), 
     float(row["PRIX_NET"]), int(row["CLI_ID"]), row["LIBELLE"])
    for _, row in df.iterrows()
]

# On insère tout en une seule fois par blocs de 10000
taille_bloc = 10000
for i in range(0, len(tickets_data), taille_bloc):
    bloc = tickets_data[i:i+taille_bloc]
    cursor.executemany("""
        INSERT INTO tickets (TICKET_ID, MOIS_VENTE, PRIX_NET, CLI_ID, LIBELLE)
        VALUES (%s, %s, %s, %s, %s)
    """, bloc)
    conn.commit()
    print(f"✅ {min(i+taille_bloc, len(tickets_data))}/{len(tickets_data)} lignes importées")

print(f"✅ Tous les tickets importés !")

cursor.close()
conn.close()
print("\nTerminé !")