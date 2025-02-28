from typing import Any, Dict, List, Optional, Union
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.persistence.data_writer import DataWriter
from src.infrastructure.config import get_settings
from src.infrastructure.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class DatabaseWriter(DataWriter):
    """
    Implementation of DataWriter for database storage.
    Uses SQLAlchemy to interface with different database types.
    """
    
    def __init__(self, connection_url=None):
        """
        Initialize with an optional connection URL.
        If not provided, it will be fetched from config when needed.
        
        Args:
            connection_url: Database connection URL (optional)
        """
        self._connection_url = connection_url
        self._engine = None
    
    def _get_engine(self):
        """
        Get or create the SQLAlchemy engine.
        
        Returns:
            sqlalchemy.engine: Database engine
        """
        if self._engine is None:
            if self._connection_url is None:
                self._connection_url = settings.DB_URL
            self._engine = create_engine(self._connection_url)
        return self._engine
    
    def write(self, data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]], 
              destination: str, **kwargs) -> bool:
        """
        Write data to a database table.
        
        Args:
            data: DataFrame or dictionary/list to write
            destination: Table name
            **kwargs: Additional parameters for pd.DataFrame.to_sql()
                - schema: Schema name (default is None)
                - if_exists: 'fail', 'replace', or 'append' (default is 'fail')
                - index: Whether to include index (default is False)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get the engine
            engine = self._get_engine()
            
            # Set default kwargs
            if 'if_exists' not in kwargs:
                kwargs['if_exists'] = 'fail'
            if 'index' not in kwargs:
                kwargs['index'] = False
            
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            
            data.to_sql(destination, engine, **kwargs)
            logger.info(f"Successfully wrote data to table {destination}")
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"Database error writing to {destination}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Failed to write data to {destination}: {str(e)}")
            return False
    
    def append(self, data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]], 
               destination: str, **kwargs) -> bool:
        """
        Append data to an existing database table.
        
        Args:
            data: DataFrame or dictionary/list to append
            destination: Table name
            **kwargs: Additional parameters for pd.DataFrame.to_sql()
            
        Returns:
            bool: True if successful, False otherwise
        """
        # For databases, appending is just writing with if_exists='append'
        kwargs['if_exists'] = 'append'
        return self.write(data, destination, **kwargs)
