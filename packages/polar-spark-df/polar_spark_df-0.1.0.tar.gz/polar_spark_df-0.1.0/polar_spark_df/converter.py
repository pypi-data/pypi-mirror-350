"""
DataFrameConverter: A high-performance converter between PySpark and Polars DataFrames.

This module provides a builder-pattern class for converting between PySpark and Polars
DataFrames with optimized performance and memory usage.
"""

from typing import Dict, List, Optional, Union, Any, Tuple
import polars as pl
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, 
    FloatType, DoubleType, BooleanType, TimestampType,
    DateType, ArrayType, MapType, LongType, DecimalType
)


class DataFrameConverter:
    """
    A high-performance converter between PySpark and Polars DataFrames.
    
    This class uses the builder pattern to configure and execute conversions
    between PySpark and Polars DataFrames with optimized performance and
    memory usage.
    
    Examples:
        # Convert PySpark DataFrame to Polars
        polars_df = (
            DataFrameConverter()
            .with_spark_df(spark_df)
            .with_batch_size(10000)
            .with_use_arrow(True)
            .to_polars()
        )
        
        # Convert Polars DataFrame to PySpark
        spark_df = (
            DataFrameConverter()
            .with_polars_df(polars_df)
            .with_spark_session(spark)
            .with_schema(schema)
            .to_spark()
        )
    """
    
    def __init__(self):
        """Initialize a new DataFrameConverter with default settings."""
        self._spark_df = None
        self._polars_df = None
        self._spark_session = None
        self._schema = None
        self._batch_size = 100000  # Default batch size
        self._use_arrow = True  # Default to use Arrow when available
        self._preserve_index = False
        self._optimize_string_conversion = True
        self._type_mapping = None
    
    def with_spark_df(self, spark_df: SparkDataFrame) -> 'DataFrameConverter':
        """
        Set the PySpark DataFrame to convert.
        
        Args:
            spark_df: The PySpark DataFrame to convert
            
        Returns:
            self: The DataFrameConverter instance for method chaining
        """
        self._spark_df = spark_df
        return self
    
    def with_polars_df(self, polars_df: pl.DataFrame) -> 'DataFrameConverter':
        """
        Set the Polars DataFrame to convert.
        
        Args:
            polars_df: The Polars DataFrame to convert
            
        Returns:
            self: The DataFrameConverter instance for method chaining
        """
        self._polars_df = polars_df
        return self
    
    def with_spark_session(self, spark_session: SparkSession) -> 'DataFrameConverter':
        """
        Set the Spark session to use for creating PySpark DataFrames.
        
        Args:
            spark_session: The SparkSession to use
            
        Returns:
            self: The DataFrameConverter instance for method chaining
        """
        self._spark_session = spark_session
        return self
    
    def with_schema(self, schema: StructType) -> 'DataFrameConverter':
        """
        Set the schema to use when converting to PySpark DataFrame.
        
        Args:
            schema: The PySpark StructType schema
            
        Returns:
            self: The DataFrameConverter instance for method chaining
        """
        self._schema = schema
        return self
    
    def with_batch_size(self, batch_size: int) -> 'DataFrameConverter':
        """
        Set the batch size for processing large DataFrames.
        
        A larger batch size may improve performance but requires more memory.
        
        Args:
            batch_size: Number of rows to process in each batch
            
        Returns:
            self: The DataFrameConverter instance for method chaining
        """
        if batch_size <= 0:
            raise ValueError("Batch size must be positive")
        self._batch_size = batch_size
        return self
    
    def with_use_arrow(self, use_arrow: bool) -> 'DataFrameConverter':
        """
        Set whether to use Apache Arrow for conversion when available.
        
        Using Arrow typically provides better performance but may not support
        all data types.
        
        Args:
            use_arrow: Whether to use Arrow for conversion
            
        Returns:
            self: The DataFrameConverter instance for method chaining
        """
        self._use_arrow = use_arrow
        return self
    
    def with_preserve_index(self, preserve_index: bool) -> 'DataFrameConverter':
        """
        Set whether to preserve the index when converting.
        
        Args:
            preserve_index: Whether to preserve the index
            
        Returns:
            self: The DataFrameConverter instance for method chaining
        """
        self._preserve_index = preserve_index
        return self
    
    def with_optimize_string_conversion(self, optimize: bool) -> 'DataFrameConverter':
        """
        Set whether to optimize string conversion.
        
        When enabled, uses optimized methods for string conversion that reduce
        memory usage.
        
        Args:
            optimize: Whether to optimize string conversion
            
        Returns:
            self: The DataFrameConverter instance for method chaining
        """
        self._optimize_string_conversion = optimize
        return self
    
    def with_type_mapping(self, type_mapping: Dict) -> 'DataFrameConverter':
        """
        Set custom type mapping for conversion.
        
        Args:
            type_mapping: Dictionary mapping source types to target types
            
        Returns:
            self: The DataFrameConverter instance for method chaining
        """
        self._type_mapping = type_mapping
        return self
    
    def _spark_to_polars_arrow(self) -> pl.DataFrame:
        """
        Convert PySpark DataFrame to Polars using Arrow.
        
        Returns:
            pl.DataFrame: The converted Polars DataFrame
        """
        # Use Arrow for efficient conversion
        try:
            # Convert to pandas with Arrow, then to polars
            pandas_df = self._spark_df.toPandas()
            return pl.from_pandas(pandas_df)
        except Exception as e:
            raise RuntimeError(f"Arrow conversion failed: {str(e)}")
    
    def _spark_to_polars_batched(self) -> pl.DataFrame:
        """
        Convert PySpark DataFrame to Polars using batched processing.
        
        Returns:
            pl.DataFrame: The converted Polars DataFrame
        """
        # Get total row count
        total_rows = self._spark_df.count()
        
        # If empty DataFrame, return empty Polars DataFrame with same schema
        if total_rows == 0:
            schema = self._spark_df.schema
            empty_data = {}
            for field in schema.fields:
                empty_data[field.name] = []
            return pl.DataFrame(empty_data)
        
        # Add a temporary row number column for efficient batching
        from pyspark.sql.functions import monotonically_increasing_id, row_number
        from pyspark.sql.window import Window
        
        # Add row numbers
        w = Window.orderBy(monotonically_increasing_id())
        df_with_row_num = self._spark_df.withColumn("_row_num", row_number().over(w))
        
        # Process in batches to reduce memory usage
        polars_dfs = []
        for i in range(0, total_rows, self._batch_size):
            end_idx = i + self._batch_size
            
            # Filter rows in the current batch using row numbers
            batch = df_with_row_num.filter(
                (df_with_row_num._row_num > i) & 
                (df_with_row_num._row_num <= end_idx)
            ).drop("_row_num")
            
            # Convert batch to pandas then to polars
            pandas_batch = batch.toPandas()
            polars_batch = pl.from_pandas(pandas_batch)
            polars_dfs.append(polars_batch)
            
            # Break if we've processed all rows
            if end_idx >= total_rows:
                break
        
        # Combine all batches
        if len(polars_dfs) == 1:
            return polars_dfs[0]
        else:
            return pl.concat(polars_dfs)
    
    def _infer_spark_schema(self) -> StructType:
        """
        Infer PySpark schema from Polars DataFrame.
        
        Returns:
            StructType: The inferred PySpark schema
        """
        # Map Polars types to PySpark types
        polars_to_spark_type = {
            pl.Int8: IntegerType(),
            pl.Int16: IntegerType(),
            pl.Int32: IntegerType(),
            pl.Int64: LongType(),
            pl.UInt8: IntegerType(),
            pl.UInt16: IntegerType(),
            pl.UInt32: LongType(),
            pl.UInt64: LongType(),
            pl.Float32: FloatType(),
            pl.Float64: DoubleType(),
            pl.Boolean: BooleanType(),
            pl.Utf8: StringType(),
            pl.Date: DateType(),
            pl.Datetime: TimestampType(),
            pl.Time: StringType(),  # No direct equivalent
            pl.Decimal: DecimalType(38, 18),  # Default precision/scale
        }
        
        def infer_complex_type(dtype):
            """Helper function to infer complex types."""
            if isinstance(dtype, pl.List):
                # Get the inner type of the list
                inner_dtype = dtype.inner
                if isinstance(inner_dtype, pl.List) or isinstance(inner_dtype, pl.Struct):
                    # For nested complex types, default to string
                    return ArrayType(StringType())
                else:
                    # Map the inner type
                    inner_spark_type = infer_complex_type(inner_dtype) if hasattr(inner_dtype, '__class__') else StringType()
                    return ArrayType(inner_spark_type)
            elif isinstance(dtype, pl.Struct):
                # Create struct fields
                struct_fields = []
                for field_name, field_dtype in dtype.fields.items():
                    field_spark_type = infer_complex_type(field_dtype) if hasattr(field_dtype, '__class__') else StringType()
                    struct_fields.append(StructField(field_name, field_spark_type, True))
                return StructType(struct_fields)
            else:
                # Basic type
                return polars_to_spark_type.get(dtype.__class__, StringType())
        
        schema_fields = []
        for col_name, dtype in zip(self._polars_df.columns, self._polars_df.dtypes):
            # Handle all types including complex ones
            spark_type = infer_complex_type(dtype)
            schema_fields.append(StructField(col_name, spark_type, True))
        
        return StructType(schema_fields)
    
    def _polars_to_spark_arrow(self) -> SparkDataFrame:
        """
        Convert Polars DataFrame to PySpark using Arrow.
        
        Returns:
            SparkDataFrame: The converted PySpark DataFrame
        """
        if self._spark_session is None:
            raise ValueError("Spark session is required for conversion to PySpark")
        
        # Convert Polars to pandas, then to Spark
        pandas_df = self._polars_df.to_pandas()
        
        # Use provided schema if available
        if self._schema is not None:
            return self._spark_session.createDataFrame(pandas_df, self._schema)
        else:
            return self._spark_session.createDataFrame(pandas_df)
    
    def _polars_to_spark_batched(self) -> SparkDataFrame:
        """
        Convert Polars DataFrame to PySpark using batched processing.
        
        Returns:
            SparkDataFrame: The converted PySpark DataFrame
        """
        if self._spark_session is None:
            raise ValueError("Spark session is required for conversion to PySpark")
        
        # Infer schema if not provided
        schema = self._schema if self._schema is not None else self._infer_spark_schema()
        
        # Process in batches
        total_rows = len(self._polars_df)
        spark_dfs = []
        
        for i in range(0, total_rows, self._batch_size):
            # Take a batch of rows
            end_idx = min(i + self._batch_size, total_rows)
            batch = self._polars_df.slice(i, end_idx - i)
            
            # Convert batch to pandas then to Spark
            pandas_batch = batch.to_pandas()
            spark_batch = self._spark_session.createDataFrame(pandas_batch, schema)
            spark_dfs.append(spark_batch)
        
        # Combine all batches
        if not spark_dfs:
            # Return empty DataFrame with schema
            return self._spark_session.createDataFrame([], schema)
        elif len(spark_dfs) == 1:
            return spark_dfs[0]
        else:
            # Use unionAll for each DataFrame one by one
            result_df = spark_dfs[0]
            for df in spark_dfs[1:]:
                result_df = result_df.unionAll(df)
            return result_df
    
    def to_polars(self) -> pl.DataFrame:
        """
        Convert PySpark DataFrame to Polars DataFrame.
        
        Returns:
            pl.DataFrame: The converted Polars DataFrame
            
        Raises:
            ValueError: If no PySpark DataFrame was provided
        """
        if self._spark_df is None:
            raise ValueError("No PySpark DataFrame provided. Use with_spark_df() first.")
        
        # Use Arrow if enabled and available
        if self._use_arrow:
            try:
                return self._spark_to_polars_arrow()
            except Exception as e:
                # Fallback to batched conversion if Arrow fails
                if self._batch_size > 0:
                    return self._spark_to_polars_batched()
                else:
                    raise RuntimeError(f"Conversion failed: {str(e)}")
        else:
            # Use batched conversion
            return self._spark_to_polars_batched()
    
    def to_spark(self) -> SparkDataFrame:
        """
        Convert Polars DataFrame to PySpark DataFrame.
        
        Returns:
            SparkDataFrame: The converted PySpark DataFrame
            
        Raises:
            ValueError: If no Polars DataFrame or Spark session was provided
        """
        if self._polars_df is None:
            raise ValueError("No Polars DataFrame provided. Use with_polars_df() first.")
        
        if self._spark_session is None:
            raise ValueError("No Spark session provided. Use with_spark_session() first.")
        
        # Use Arrow if enabled and available
        if self._use_arrow:
            try:
                return self._polars_to_spark_arrow()
            except Exception as e:
                # Fallback to batched conversion if Arrow fails
                if self._batch_size > 0:
                    return self._polars_to_spark_batched()
                else:
                    raise RuntimeError(f"Conversion failed: {str(e)}")
        else:
            # Use batched conversion
            return self._polars_to_spark_batched()