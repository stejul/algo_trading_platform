from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import pandas as pd


class DataWriter(ABC):
    """
    Abstract base class for data writing operations.
    Defines a common interface for writing data in different formats.
    """
    
    @abstractmethod
    def write(self, data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]], 
              destination: Union[str, Path], **kwargs) -> bool:
        """
        Write data to the specified destination.
        
        Args:
            data: The data to write (DataFrame or dictionary/list of dictionaries)
            destination: File path or database identifier
            **kwargs: Additional format-specific parameters
            
        Returns:
            bool: True if write operation was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def append(self, data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]], 
               destination: Union[str, Path], **kwargs) -> bool:
        """
        Append data to an existing destination.
        
        Args:
            data: The data to append (DataFrame or dictionary/list of dictionaries)
            destination: File path or database identifier
            **kwargs: Additional format-specific parameters
            
        Returns:
            bool: True if append operation was successful, False otherwise
        """
        pass
    
    @staticmethod
    def get_writer(format_type: str) -> 'DataWriter':
        """
        Factory method to get the appropriate writer instance.
        
        Args:
            format_type: String identifier for the desired format ('parquet', 'json', 'csv', 'db')
            
        Returns:
            DataWriter: An instance of the appropriate writer class
            
        Raises:
            ValueError: If an unsupported format is requested
        """
        from src.infrastructure.persistence.parquet_writer import ParquetWriter
        from src.infrastructure.persistence.json_writer import JsonWriter
        from src.infrastructure.persistence.csv_writer import CsvWriter
        from src.infrastructure.persistence.db_writer import DatabaseWriter
        
        writers = {
            'parquet': ParquetWriter(),
            'json': JsonWriter(),
            'csv': CsvWriter(),
            'db': DatabaseWriter()
        }
        
        if format_type.lower() not in writers:
            raise ValueError(f"Unsupported format: {format_type}. Supported formats: {', '.join(writers.keys())}")
        
        return writers[format_type.lower()]
