"""Pipeline d'ingestion : geo_dvf_raw (CSV.gz local) -> Bronze (Parquet MinIO)."""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import to_bronze


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=to_bronze,
                inputs=["geo_dvf_raw", "params:bronze_repartitions"],
                outputs="bronze_geo_dvf",
                name="to_bronze",
            ),
        ]
    )
