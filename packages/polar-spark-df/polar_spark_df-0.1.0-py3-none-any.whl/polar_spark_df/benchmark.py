"""
Benchmarking utilities for the DataFrameConverter.

This module provides functions to benchmark the performance of conversions
between PySpark and Polars DataFrames.
"""

import time
from typing import Dict, Any, Callable, Tuple
import polars as pl
from pyspark.sql import DataFrame as SparkDataFrame, SparkSession
from pyspark.sql.types import StructType
import gc
import psutil
import os

from polar_spark_df.converter import DataFrameConverter


def measure_memory_usage() -> float:
    """
    Measure the current memory usage of the process.
    
    Returns:
        float: Memory usage in MB
    """
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)  # Convert to MB


def benchmark_conversion(
    func: Callable, 
    *args, 
    **kwargs
) -> Tuple[Any, float, float]:
    """
    Benchmark a conversion function.
    
    Args:
        func: The function to benchmark
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Tuple containing:
            - The result of the function
            - Execution time in seconds
            - Memory usage in MB
    """
    # Force garbage collection before measuring
    gc.collect()
    
    # Measure initial memory
    initial_memory = measure_memory_usage()
    
    # Measure execution time
    start_time = time.time()
    result = func(*args, **kwargs)
    execution_time = time.time() - start_time
    
    # Force garbage collection again
    gc.collect()
    
    # Measure final memory
    final_memory = measure_memory_usage()
    memory_used = final_memory - initial_memory
    
    return result, execution_time, memory_used


def benchmark_spark_to_polars(
    spark_df: SparkDataFrame,
    batch_sizes: list = [10000, 50000, 100000],
    use_arrow: list = [True, False]
) -> Dict[str, Dict[str, float]]:
    """
    Benchmark conversion from PySpark to Polars with different configurations.
    
    Args:
        spark_df: The PySpark DataFrame to convert
        batch_sizes: List of batch sizes to test
        use_arrow: List of boolean values for using Arrow
        
    Returns:
        Dict: Results of benchmarks with different configurations
    """
    results = {}
    
    for arrow in use_arrow:
        for batch_size in batch_sizes:
            config_name = f"arrow={arrow},batch_size={batch_size}"
            
            def conversion_func():
                return (
                    DataFrameConverter()
                    .with_spark_df(spark_df)
                    .with_batch_size(batch_size)
                    .with_use_arrow(arrow)
                    .to_polars()
                )
            
            _, execution_time, memory_used = benchmark_conversion(conversion_func)
            
            results[config_name] = {
                "execution_time": execution_time,
                "memory_used": memory_used
            }
    
    return results


def benchmark_polars_to_spark(
    polars_df: pl.DataFrame,
    spark_session: SparkSession,
    schema: StructType = None,
    batch_sizes: list = [10000, 50000, 100000],
    use_arrow: list = [True, False]
) -> Dict[str, Dict[str, float]]:
    """
    Benchmark conversion from Polars to PySpark with different configurations.
    
    Args:
        polars_df: The Polars DataFrame to convert
        spark_session: The SparkSession to use
        schema: Optional schema for the PySpark DataFrame
        batch_sizes: List of batch sizes to test
        use_arrow: List of boolean values for using Arrow
        
    Returns:
        Dict: Results of benchmarks with different configurations
    """
    results = {}
    
    for arrow in use_arrow:
        for batch_size in batch_sizes:
            config_name = f"arrow={arrow},batch_size={batch_size}"
            
            def conversion_func():
                converter = (
                    DataFrameConverter()
                    .with_polars_df(polars_df)
                    .with_spark_session(spark_session)
                    .with_batch_size(batch_size)
                    .with_use_arrow(arrow)
                )
                
                if schema is not None:
                    converter = converter.with_schema(schema)
                
                return converter.to_spark()
            
            _, execution_time, memory_used = benchmark_conversion(conversion_func)
            
            results[config_name] = {
                "execution_time": execution_time,
                "memory_used": memory_used
            }
    
    return results


def print_benchmark_results(results: Dict[str, Dict[str, float]]) -> None:
    """
    Print benchmark results in a formatted table.
    
    Args:
        results: Dictionary of benchmark results
    """
    print(f"{'Configuration':<30} | {'Time (s)':<10} | {'Memory (MB)':<12}")
    print("-" * 56)
    
    for config, metrics in results.items():
        time_str = f"{metrics['execution_time']:.4f}"
        memory_str = f"{metrics['memory_used']:.2f}"
        print(f"{config:<30} | {time_str:<10} | {memory_str:<12}")