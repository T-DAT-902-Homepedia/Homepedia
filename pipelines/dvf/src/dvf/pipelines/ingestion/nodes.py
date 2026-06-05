"""Nodes du pipeline d'ingestion (couche Bronze).

Bronze = copie 1:1 typée du CSV brut, matérialisée en Parquet sur MinIO. Aucune
règle métier ici : seulement le typage et la mise en forme pour exploitation
parallèle (le gzip source est non-splittable -> un seul cœur sinon).
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def to_bronze(geo_dvf_raw: DataFrame, repartitions: int) -> DataFrame:
    """Type la date et repartitionne pour débloquer le parallélisme aval.

    Le DataFrame d'entrée est déjà chargé avec le schéma explicite (catalog).
    On convertit ``date_mutation`` (String ISO ``yyyy-MM-dd``) en DateType ;
    tout le reste est conservé tel quel (Bronze = brut typé, non filtré).
    """
    return geo_dvf_raw.withColumn(
        "date_mutation", F.to_date("date_mutation", "yyyy-MM-dd")
    ).repartition(repartitions)
