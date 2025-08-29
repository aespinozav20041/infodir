"""Create Delta Lake tables for curated and features datasets.

The script writes sample data to Delta format partitioned by period (YYYY-MM) and
applies Z-Ordering by the ``term`` column. Paths and table names are provided as
function arguments for reuse in different environments.
"""
from pyspark.sql import SparkSession


def create_table(table_name: str, path: str) -> None:
    """Create a Delta table with period partitioning and Z-Order by term.

    Parameters
    ----------
    table_name:
        Name of the table to register in the metastore.
    path:
        Storage location for the Delta table.
    """
    spark = (
        SparkSession.builder.appName("DeltaSetup")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .getOrCreate()
    )

    data = [
        ("alpha", "2024-01", 1),
        ("beta", "2024-02", 2),
    ]
    df = spark.createDataFrame(data, ["term", "period", "value"])

    (
        df.write.format("delta")
        .mode("overwrite")
        .partitionBy("period")
        .save(path)
    )

    spark.sql(
        f"CREATE TABLE IF NOT EXISTS {table_name} USING DELTA LOCATION '{path}'"
    )
    spark.sql(f"OPTIMIZE {table_name} ZORDER BY (term)")


def main() -> None:
    """Create curated and features tables using local paths."""
    create_table("curated", "s3://example-bucket/curated")
    create_table("features", "s3://example-bucket/features")


if __name__ == "__main__":
    main()
