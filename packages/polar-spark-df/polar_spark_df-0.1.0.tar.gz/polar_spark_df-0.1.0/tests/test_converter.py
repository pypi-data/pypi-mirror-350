"""
Tests for the DataFrameConverter class.
"""

import pytest
import polars as pl
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

from polar_spark_df.converter import DataFrameConverter


@pytest.fixture(scope="module")
def spark_session():
    """Create a SparkSession for testing."""
    return (
        SparkSession.builder
        .master("local[1]")
        .appName("polar-spark-df-tests")
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .getOrCreate()
    )


@pytest.fixture(scope="module")
def sample_spark_df(spark_session):
    """Create a sample PySpark DataFrame for testing."""
    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), True),
        StructField("value", DoubleType(), True)
    ])
    
    data = [
        (1, "Alice", 10.5),
        (2, "Bob", 20.0),
        (3, "Charlie", 30.7),
        (4, "David", None),
        (5, "Eve", 50.2)
    ]
    
    return spark_session.createDataFrame(data, schema)


@pytest.fixture(scope="module")
def sample_polars_df():
    """Create a sample Polars DataFrame for testing."""
    return pl.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "value": [10.5, 20.0, 30.7, None, 50.2]
    })


def test_spark_to_polars_with_arrow(spark_session, sample_spark_df):
    """Test conversion from PySpark to Polars using Arrow."""
    converter = DataFrameConverter()
    polars_df = (
        converter
        .with_spark_df(sample_spark_df)
        .with_use_arrow(True)
        .to_polars()
    )
    
    # Verify the conversion
    assert isinstance(polars_df, pl.DataFrame)
    assert polars_df.shape == (5, 3)
    assert polars_df.columns == ["id", "name", "value"]
    assert polars_df.row(0) == (1, "Alice", 10.5)


def test_spark_to_polars_without_arrow(spark_session, sample_spark_df):
    """Test conversion from PySpark to Polars without using Arrow."""
    converter = DataFrameConverter()
    polars_df = (
        converter
        .with_spark_df(sample_spark_df)
        .with_use_arrow(False)
        .to_polars()
    )
    
    # Verify the conversion
    assert isinstance(polars_df, pl.DataFrame)
    assert polars_df.shape == (5, 3)
    assert polars_df.columns == ["id", "name", "value"]
    assert polars_df.row(0) == (1, "Alice", 10.5)


def test_polars_to_spark_with_arrow(spark_session, sample_polars_df):
    """Test conversion from Polars to PySpark using Arrow."""
    converter = DataFrameConverter()
    spark_df = (
        converter
        .with_polars_df(sample_polars_df)
        .with_spark_session(spark_session)
        .with_use_arrow(True)
        .to_spark()
    )
    
    # Verify the conversion
    assert spark_df.count() == 5
    assert len(spark_df.columns) == 3
    assert spark_df.columns == ["id", "name", "value"]
    assert spark_df.first()["id"] == 1
    assert spark_df.first()["name"] == "Alice"
    assert spark_df.first()["value"] == 10.5


def test_polars_to_spark_without_arrow(spark_session, sample_polars_df):
    """Test conversion from Polars to PySpark without using Arrow."""
    converter = DataFrameConverter()
    spark_df = (
        converter
        .with_polars_df(sample_polars_df)
        .with_spark_session(spark_session)
        .with_use_arrow(False)
        .to_spark()
    )
    
    # Verify the conversion
    assert spark_df.count() == 5
    assert len(spark_df.columns) == 3
    assert spark_df.columns == ["id", "name", "value"]
    assert spark_df.first()["id"] == 1
    assert spark_df.first()["name"] == "Alice"
    assert spark_df.first()["value"] == 10.5


def test_polars_to_spark_with_schema(spark_session, sample_polars_df):
    """Test conversion from Polars to PySpark with a custom schema."""
    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), True),
        StructField("value", DoubleType(), True)
    ])
    
    converter = DataFrameConverter()
    spark_df = (
        converter
        .with_polars_df(sample_polars_df)
        .with_spark_session(spark_session)
        .with_schema(schema)
        .to_spark()
    )
    
    # Verify the conversion
    assert spark_df.count() == 5
    assert len(spark_df.columns) == 3
    assert spark_df.columns == ["id", "name", "value"]
    assert spark_df.schema == schema


def test_batch_size_validation():
    """Test validation of batch size."""
    converter = DataFrameConverter()
    
    with pytest.raises(ValueError):
        converter.with_batch_size(0)
    
    with pytest.raises(ValueError):
        converter.with_batch_size(-1)


def test_missing_spark_df():
    """Test error when no PySpark DataFrame is provided."""
    converter = DataFrameConverter()
    
    with pytest.raises(ValueError):
        converter.to_polars()


def test_missing_polars_df():
    """Test error when no Polars DataFrame is provided."""
    converter = DataFrameConverter()
    
    with pytest.raises(ValueError):
        converter.to_spark()


def test_missing_spark_session(sample_polars_df):
    """Test error when no SparkSession is provided."""
    converter = DataFrameConverter()
    converter.with_polars_df(sample_polars_df)
    
    with pytest.raises(ValueError):
        converter.to_spark()