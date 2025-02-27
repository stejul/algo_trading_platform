import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from src.infrastructure.persistence.data_writer import DataWriter
from src.infrastructure.logging import get_logger

logger = get_logger(__name__)


class ParquetWriter(DataWriter):
    """
    Implementation of DataWriter for Parquet format.
    """
    
    def write(self, data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]], 
              destination: Union[str, Path], **kwargs) -> bool:
        """
        Write data to a parquet file.
        
        Args:
            data: DataFrame or dictionary/list to write
            destination: File path
            **kwargs: Additional parameters for pd.DataFrame.to_parquet()
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            dest_path = Path(destination)
            os.makedirs(dest_path.parent, exist_ok=True)
            
            # Convert to DataFrame if needed
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            
            # Write to parquet
            data.to_parquet(destination, **kwargs)
            logger.info(f"Successfully wrote data to {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write data to {destination}: {str(e)}")
            return False
    
    def append(self, data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]], 
               destination: Union[str, Path], **kwargs) -> bool:
        """
        Append data to an existing parquet file.
        Note: This is a bit tricky with parquet as it's not designed for appending.
        The implementation reads the existing file, appends the new data, and rewrites.
        
        Args:
            data: DataFrame or dictionary/list to append
            destination: File path
            **kwargs: Additional parameters for pd.DataFrame.to_parquet()
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            dest_path = Path(destination)
            
            # Convert new data to DataFrame if needed
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            
            # If file exists, read it and append
            if dest_path.exists():
                existing_data = pd.read_parquet(destination)
                combined_data = pd.concat([existing_data, data], ignore_index=True)
            else:
                combined_data = data
                # Create directory if it doesn't exist
                os.makedirs(dest_path.parent, exist_ok=True)
            
            # Write combined data
            combined_data.to_parquet(destination, **kwargs)
            logger.info(f"Successfully appended data to {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to append data to {destination}: {str(e)}")
            return False
