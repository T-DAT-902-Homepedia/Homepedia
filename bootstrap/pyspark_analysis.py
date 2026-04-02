from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, regexp_replace

# --- Création de la session Spark ---
# C'est le point d'entrée de PySpark
# master("local[*]") = utilise tous les cœurs de ton PC
spark = SparkSession.builder \
    .appName("Homepedia Immobilier") \
    .master("local[*]") \
    .getOrCreate()

# Réduit les logs pour ne voir que les erreurs
spark.sparkContext.setLogLevel("ERROR")

print("✅ Session Spark démarrée")

# --- Chargement du fichier ---
# header=True = première ligne = noms des colonnes
# inferSchema=True = Spark devine les types automatiquement
# sep="," = séparateur virgule
df = spark.read.csv(
    "france_total_real_estate_sales_2022.csv",
    header=True,
    inferSchema=True,
    sep=","
)

print(f"✅ Fichier chargé")

# --- Exploration des données ---
print("\n📊 Schéma du fichier (colonnes et types) :")
df.printSchema()

print("\n📊 5 premières lignes :")
df.show(5)

print(f"\n📊 Nombre total de ventes : {df.count()}")

# --- Nettoyage de la colonne prix ---
# Le prix est en format français "55000,00" avec une virgule
# On remplace la virgule par un point pour en faire un vrai nombre
df = df.withColumn(
    "prix",
    regexp_replace(col("Valeur fonciere"), ",", ".").cast("double")
)

# --- Analyse 1 : Prix moyen par département ---
print("\n📊 Prix moyen par département (top 10 plus chers) :")
df.groupBy("Code departement") \
  .agg(avg("prix").alias("prix_moyen")) \
  .orderBy("prix_moyen", ascending=False) \
  .show(10)

# --- Analyse 2 : Nombre de ventes par type de bien ---
print("\n📊 Nombre de ventes par type de bien :")
df.groupBy("Type local") \
  .agg(count("*").alias("nb_ventes")) \
  .orderBy("nb_ventes", ascending=False) \
  .show()

# --- Analyse 3 : Prix moyen par type de bien ---
print("\n📊 Prix moyen par type de bien :")
df.groupBy("Type local") \
  .agg(avg("prix").alias("prix_moyen")) \
  .orderBy("prix_moyen", ascending=False) \
  .show()

# --- Utilisation de SQL avec Spark ---
print("\n📊 Requête SQL avec Spark :")

# On enregistre le dataframe comme une table SQL temporaire
df.createOrReplaceTempView("ventes")

# On fait une vraie requête SQL dessus !
result = spark.sql("""
    SELECT 
        `Code departement`,
        `Type local`,
        COUNT(*) as nb_ventes,
        ROUND(AVG(prix), 2) as prix_moyen
    FROM ventes
    WHERE `Type local` IS NOT NULL
    AND prix IS NOT NULL
    GROUP BY `Code departement`, `Type local`
    ORDER BY nb_ventes DESC
    LIMIT 10
""")
result.show()

# --- map() et reduceByKey() avec les RDD ---
# RDD = Resilient Distributed Dataset
# C'est la structure de base de Spark, avant les DataFrames
print("\n📊 Utilisation de map() et reduceByKey() :")

# On convertit le DataFrame en RDD
rdd = df.select("Code departement", "prix").rdd

# map() : transforme chaque ligne en tuple (departement, prix)
rdd_mapped = rdd.map(lambda row: (row[0], row[1] if row[1] else 0))

# reduceByKey() : additionne les prix par département
rdd_total = rdd_mapped.reduceByKey(lambda a, b: a + b)

# sortByKey() : trie par département
rdd_sorted = rdd_total.sortByKey()

print("Total des ventes par département (5 premiers) :")
for dept, total in rdd_sorted.take(5):
    print(f"  Département {dept} : {round(total, 2)} €")

spark.stop()
print("\n✅ Terminé !")