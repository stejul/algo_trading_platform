import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from src.infrastructure.persistence.data_writer import DataWriter
from src.infrastructure.logging import get_logger

logger = get_logger(__name__)


class JsonWriter(DataWriter):
    """
    Implementation of DataWriter for JSON format.
    """
    
    def write(self, data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]], 
              destination: Union[str, Path], **kwargs) -> bool:
        """
        Write data to a JSON file.
        
        Args:
            data: DataFrame or dictionary/list to write
            destination: File path
            **kwargs: Additional parameters for json.dump() or pd.DataFrame.to_json()
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            dest_path = Path(destination)
            os.makedirs(dest_path.parent, exist_ok=True)
            
            if isinstance(data, pd.DataFrame):
                data.to_json(destination, orient=kwargs.pop('orient', 'records'), **kwargs)
            else:
                with open(destination, 'w') as f:
                    json.dump(data, f, **kwargs)
            
            logger.info(f"Successfully wrote data to {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write data to {destination}: {str(e)}")
            return False
    
    def append(self, data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]], 
               destination: Union[str, Path], **kwargs) -> bool:
        """
        Append data to an existing JSON file.
        For JSON files, this assumes the file contains a list of records.
        
        Args:
            data: DataFrame or dictionary/list to append
            destination: File path
            **kwargs: Additional parameters for json.dump()
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            dest_path = Path(destination)
            
            # Convert data to list of records if it's a DataFrame
            if isinstance(data, pd.DataFrame):
                data_to_append = data.to_dict(orient='records')
            elif isinstance(data, dict):
                data_to_append = [data]
            else:
                data_to_append = data
            
            if dest_path.exists():
                with open(destination, 'r') as f:
                    existing_data = json.load(f)
                
                # Ensure existing data is a list
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
                
                combined_data = existing_data + data_to_append
            else:
                combined_data = data_to_append
                os.makedirs(dest_path.parent, exist_ok=True)
            
            with open(destination, 'w') as f:
                json.dump(combined_data, f, **kwargs)
            
            logger.info(f"Successfully appended data to {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to append data to {destination}: {str(e)}")
            return False
