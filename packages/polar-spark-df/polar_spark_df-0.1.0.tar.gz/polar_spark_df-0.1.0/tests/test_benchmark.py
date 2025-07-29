"""
Benchmark tests for the DataFrameConverter.
"""

import pytest
import polars as pl
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import numpy as np

from polar_spark_df.converter import DataFrameConverter
from polar_spark_df.benchmark import (
    benchmark_spark_to_polars,
    benchmark_polars_to_spark,
    print_benchmark_results
)


@pytest.fixture(scope="module")
def spark_session():
    """Create a SparkSession for testing."""
    return (
        SparkSession.builder
        .master("local[2]")
        .appName("polar-spark-df-benchmarks")
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .getOrCreate()
    )


@pytest.fixture(scope="module")
def large_spark_df(spark_session):
    """Create a larger PySpark DataFrame for benchmarking."""
    # Create a schema
    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), True),
        StructField("value1", DoubleType(), True),
        StructField("value2", DoubleType(), True),
        StructField("value3", DoubleType(), True)
    ])
    
    # Generate random data
    num_rows = 100000
    data = []
    for i in range(num_rows):
        name = f"name_{i}"
        value1 = float(np.random.rand())
        value2 = float(np.random.rand() * 100)
        value3 = float(np.random.rand() * 1000)
        data.append((i, name, value1, value2, value3))
    
    return spark_session.createDataFrame(data, schema)


@pytest.fixture(scope="module")
def large_polars_df():
    """Create a larger Polars DataFrame for benchmarking."""
    # Generate random data
    num_rows = 100000
    
    return pl.DataFrame({
        "id": range(num_rows),
        "name": [f"name_{i}" for i in range(num_rows)],
        "value1": np.random.rand(num_rows),
        "value2": np.random.rand(num_rows) * 100,
        "value3": np.random.rand(num_rows) * 1000
    })


@pytest.mark.benchmark
def test_benchmark_spark_to_polars(spark_session, large_spark_df):
    """Benchmark conversion from PySpark to Polars."""
    # Run benchmarks with different configurations
    results = benchmark_spark_to_polars(
        large_spark_df,
        batch_sizes=[10000, 50000, 100000],
        use_arrow=[True, False]
    )
    
    # Print results
    print("\nBenchmark: PySpark to Polars")
    print_benchmark_results(results)
    
    # Verify that all configurations produced valid results
    assert len(results) == 6  # 3 batch sizes * 2 arrow options


@pytest.mark.benchmark
def test_benchmark_polars_to_spark(spark_session, large_polars_df):
    """Benchmark conversion from Polars to PySpark."""
    # Create a schema
    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), True),
        StructField("value1", DoubleType(), True),
        StructField("value2", DoubleType(), True),
        StructField("value3", DoubleType(), True)
    ])
    
    # Run benchmarks with different configurations
    results = benchmark_polars_to_spark(
        large_polars_df,
        spark_session,
        schema=schema,
        batch_sizes=[10000, 50000, 100000],
        use_arrow=[True, False]
    )
    
    # Print results
    print("\nBenchmark: Polars to PySpark")
    print_benchmark_results(results)
    
    # Verify that all configurations produced valid results
    assert len(results) == 6  # 3 batch sizes * 2 arrow options