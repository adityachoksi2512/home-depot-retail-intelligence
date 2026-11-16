# Databricks notebook source

from pyspark.sql import functions as F

BASE_PATH = "/Volumes/workspace/retail_intelligence/raw_files"

train_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{BASE_PATH}/train.csv")
)

print("Training records:", train_df.count())

train_df.printSchema()

display(train_df.limit(10))

# COMMAND ----------

from pyspark.sql import functions as F

bronze_df = (
    train_df
    .withColumn("ingestion_timestamp", F.current_timestamp())
    .withColumn("source_file", F.lit("train.csv"))
)

bronze_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.retail_intelligence.bronze_search")

# COMMAND ----------

bronze = spark.table(
    "workspace.retail_intelligence.bronze_search"
)

print("Bronze records:", bronze.count())

display(bronze.limit(5))

# COMMAND ----------

from pyspark.sql import functions as F

BASE_PATH = "/Volumes/workspace/retail_intelligence/raw_files"

# Load product descriptions
descriptions_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{BASE_PATH}/product_descriptions.csv")
)

print("Product descriptions:", descriptions_df.count())
descriptions_df.printSchema()

# Standardize search terms and titles
cleaned_df = (
    bronze
    .withColumn("search_term", F.trim(F.lower(F.col("search_term"))))
    .withColumn("product_title", F.trim(F.col("product_title")))
)

# Flag invalid records
validated_df = cleaned_df.withColumn(
    "is_valid",
    F.col("id").isNotNull()
    & F.col("product_uid").isNotNull()
    & F.col("search_term").isNotNull()
    & (F.length(F.col("search_term")) > 0)
    & F.col("relevance").between(1.0, 3.0)
)

# Separate valid and invalid records
valid_df = validated_df.filter(F.col("is_valid"))
invalid_df = validated_df.filter(~F.col("is_valid"))

# Enrich valid records with product descriptions
silver_df = (
    valid_df
    .join(
        descriptions_df,
        on="product_uid",
        how="left"
    )
    .withColumn(
        "has_description",
        F.col("product_description").isNotNull()
        & (F.length(F.trim(F.col("product_description"))) > 0)
    )
)

# Save Silver and rejected records
silver_df.write.format("delta").mode("overwrite").saveAsTable(
    "workspace.retail_intelligence.silver_search"
)

invalid_df.write.format("delta").mode("overwrite").saveAsTable(
    "workspace.retail_intelligence.rejected_search"
)

print("Valid records:", valid_df.count())
print("Rejected records:", invalid_df.count())
print("Silver records:", silver_df.count())

display(silver_df.limit(5))

# COMMAND ----------

from pyspark.sql import functions as F

silver = spark.table(
    "workspace.retail_intelligence.silver_search"
)

# Aggregate search relevance by customer search term
gold_df = (
    silver
    .groupBy("search_term")
    .agg(
        F.count("*").alias("product_matches"),
        F.round(F.avg("relevance"), 3).alias("avg_relevance"),
        F.round(
            F.avg(
                F.when(F.col("relevance") < 2.0, 1.0)
                 .otherwise(0.0)
            ) * 100,
            2
        ).alias("low_relevance_pct"),
        F.sum(
            F.when(~F.col("has_description"), 1)
             .otherwise(0)
        ).alias("missing_descriptions")
    )
    .filter(F.col("product_matches") >= 5)
)

# Save the Gold Delta table
gold_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(
        "workspace.retail_intelligence.gold_search_quality"
    )

print("Search terms analyzed:", gold_df.count())

display(
    gold_df.orderBy(
        F.col("avg_relevance").asc(),
        F.col("product_matches").desc()
    ).limit(20)
)

# COMMAND ----------

gold = spark.table(
    "workspace.retail_intelligence.gold_search_quality"
)

export_path = (
    "/Volumes/workspace/retail_intelligence/"
    "raw_files/gold_export"
)

(
    gold.coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(export_path)
)

print("Export completed.")
display(dbutils.fs.ls(export_path))

# COMMAND ----------

display(dbutils.fs.ls(
    "/Volumes/workspace/retail_intelligence/raw_files/gold_export"
))
