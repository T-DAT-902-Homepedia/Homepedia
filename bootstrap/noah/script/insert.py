from pathlib import Path
import pandas as pd

BATCH_SIZE = 10000

def truncate_tables(cursor):
    print("🗑️  Truncate des tables...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE ticket_produits")
    cursor.execute("TRUNCATE TABLE ticket")
    cursor.execute("TRUNCATE TABLE produit")
    cursor.execute("TRUNCATE TABLE client")
    cursor.execute("TRUNCATE TABLE maille")
    cursor.execute("TRUNCATE TABLE univers")
    cursor.execute("TRUNCATE TABLE maille_univers")
    cursor.execute("TRUNCATE TABLE famille")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    print("✅ Tables vidées")

def insert_familles(cursor, df):
    print("⏳ Insertion des familles...")
    familles = df["FAMILLE"].unique()
    famille_map = {}

    for famille in familles:
        cursor.execute(
            "INSERT INTO famille (famille) VALUES (%s)",
            (famille,)
        )
        famille_map[famille] = cursor.lastrowid

    print(f"✅ {len(famille_map)} familles insérées")
    return famille_map

def insert_univers(cursor, df, famille_map):
    print("⏳ Insertion des univers...")
    univers_uniques = df[["UNIVERS", "FAMILLE"]].drop_duplicates()
    univers_map = {}

    for _, row in univers_uniques.iterrows():
        cursor.execute(
            "INSERT INTO univers (univers, famille_id) VALUES (%s, %s)",
            (row["UNIVERS"], famille_map[row["FAMILLE"]])
        )
        univers_map[row["UNIVERS"]] = cursor.lastrowid

    print(f"✅ {len(univers_map)} univers insérés")
    return univers_map

def insert_mailles(cursor, df, univers_map):
    print("⏳ Insertion des mailles...")
    mailles_uniques = df["MAILLE"].unique()
    maille_map = {}

    for maille in mailles_uniques:
        cursor.execute(
            "INSERT INTO maille (maille) VALUES (%s)",
            (maille,)
        )
        maille_map[maille] = cursor.lastrowid

    print(f"✅ {len(maille_map)} mailles insérées")

    print("⏳ Insertion des relations maille/univers...")
    maille_univers = df[["MAILLE", "UNIVERS"]].drop_duplicates()
    data = [
        (maille_map[row["MAILLE"]], univers_map[row["UNIVERS"]])
        for _, row in maille_univers.iterrows()
    ]

    cursor.executemany(
        "INSERT INTO maille_univers (maille_id, univers_id) VALUES (%s, %s)",
        data
    )
    print(f"✅ {len(data)} relations maille/univers insérées")

    return maille_map

def insert_clients(cursor, df):
    print("⏳ Insertion des clients...")
    clients = df["CLI_ID"].unique()

    for client in clients:
        cursor.execute(
            "INSERT INTO client (id) VALUES (%s)",
            (str(client),)
        )

    print(f"✅ {len(clients)} clients insérés")

def insert_produits(cursor, df, maille_map):
    print("⏳ Insertion des produits...")
    produits_uniques = df[["LIBELLE", "MAILLE"]].drop_duplicates()
    produit_map = {}

    for _, row in produits_uniques.iterrows():
        cursor.execute(
            "INSERT INTO produit (libelle, maille_id) VALUES (%s, %s)",
            (row["LIBELLE"], maille_map[row["MAILLE"]])
        )
        produit_map[row["LIBELLE"]] = cursor.lastrowid

    print(f"✅ {len(produit_map)} produits insérés")
    return produit_map

def insert_tickets(cursor, df):
    print("⏳ Insertion des tickets...")
    tickets_uniques = df[["TICKET_ID", "CLI_ID", "MOIS_VENTE"]].drop_duplicates()
    total = len(tickets_uniques)

    data = [
        (str(row["TICKET_ID"]), str(row["CLI_ID"]), int(row["MOIS_VENTE"]))
        for _, row in tickets_uniques.iterrows()
    ]

    for i in range(0, len(data), BATCH_SIZE):
        batch = data[i:i + BATCH_SIZE]
        cursor.executemany(
            "INSERT INTO ticket (id, client_id, mois_vente) VALUES (%s, %s, %s)",
            batch
        )
        print(f"  → {min(i + BATCH_SIZE, total)}/{total} tickets insérés")

    print(f"✅ {total} tickets insérés")

def insert_ticket_produits(cursor, df, produit_map):
    print("⏳ Insertion des ticket_produits...")
    total = len(df)

    data = [
        (str(row["TICKET_ID"]), produit_map[row["LIBELLE"]], float(row["PRIX_NET"]))
        for _, row in df.iterrows()
    ]

    for i in range(0, len(data), BATCH_SIZE):
        batch = data[i:i + BATCH_SIZE]
        cursor.executemany(
            "INSERT INTO ticket_produits (ticket_id, produit_id, prix_net) VALUES (%s, %s, %s)",
            batch
        )
        print(f"  → {min(i + BATCH_SIZE, total)}/{total} ticket_produits insérés")

    print(f"✅ {total} ticket_produits insérés")

def main():
    from database import create_connection, close_connection
    connection = create_connection()
    cursor = connection.cursor()

    csv_path = Path(__file__).parent.parent / "data" / "KaDo.csv"
    print("📂 Chargement du CSV...")
    df = pd.read_csv(csv_path)
    df = df.drop_duplicates()
    print(f"✅ {len(df)} lignes chargées")

    truncate_tables(cursor)
    famille_map = insert_familles(cursor, df)
    univers_map = insert_univers(cursor, df, famille_map)
    maille_map = insert_mailles(cursor, df, univers_map)
    insert_clients(cursor, df)
    produit_map = insert_produits(cursor, df, maille_map)
    insert_tickets(cursor, df)
    insert_ticket_produits(cursor, df, produit_map)

    connection.commit()
    close_connection(connection, cursor)
    print("🎉 Insertion terminée !")

if __name__ == "__main__":
    main()
