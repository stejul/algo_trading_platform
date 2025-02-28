import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from src.infrastructure.persistence.data_writer import DataWriter
from src.infrastructure.logging import get_logger

logger = get_logger(__name__)


class CsvWriter(DataWriter):
    """
    Implementation of DataWriter for CSV format.
    """
    
    def write(self, data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]], 
              destination: Union[str, Path], **kwargs) -> bool:
        """
        Write data to a CSV file.
        
        Args:
            data: DataFrame or dictionary/list to write
            destination: File path
            **kwargs: Additional parameters for pd.DataFrame.to_csv()
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            dest_path = Path(destination)
            os.makedirs(dest_path.parent, exist_ok=True)
            
            # Convert to DataFrame if needed
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            
            # Set default parameters
            if 'index' not in kwargs:
                kwargs['index'] = False
            
            data.to_csv(destination, **kwargs)
            logger.info(f"Successfully wrote data to {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write data to {destination}: {str(e)}")
            return False
    
    def append(self, data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]], 
               destination: Union[str, Path], **kwargs) -> bool:
        """
        Append data to an existing CSV file.
        
        Args:
            data: DataFrame or dictionary/list to append
            destination: File path
            **kwargs: Additional parameters for pd.DataFrame.to_csv()
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            dest_path = Path(destination)
            
            # Convert to DataFrame if needed
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            
            # Set default parameters
            if 'index' not in kwargs:
                kwargs['index'] = False
            
            # If file exists, append without header
            if dest_path.exists():
                # Append mode and no header if file exists
                data.to_csv(destination, mode='a', header=False, **kwargs)
            else:
                os.makedirs(dest_path.parent, exist_ok=True)
                data.to_csv(destination, **kwargs)
            
            logger.info(f"Successfully appended data to {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to append data to {destination}: {str(e)}")
            return False
