import abc
import logging
from typing import Optional, Tuple, Dict, Any
import pandas as pd
from .exceptions import ConnectionError, QueryError  # Import from .exceptions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DBConnector(abc.ABC):
    """
    Abstract base class for database connectors.
    """
    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the database connector with configuration.

        Args:
            config (dict): A dictionary containing database connection parameters.
        """
        self.config = config
        self.connection = None
        self._validate_config()

    def _validate_config(self) -> None:
        """
        Validates the database configuration.
        """
        required_keys = ["host", "database", "user", "password"]
        if not all(key in self.config for key in required_keys):
            raise ValueError(f"Missing required configuration keys: {required_keys}")
        if 'type' not in self.config:
            raise ValueError("Missing 'type' in configuration.  Must specify the database type.")

    def connect(self) -> None:
        """
        Establishes a database connection.
        """
        if self.connection is not None:
            return  # Already connected
        try:
            self._connect()  # Call the subclass-specific connect method
            logging.info(f"Connected to {self.config.get('type', 'database')} database at {self.config.get('host', 'localhost')}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    @abc.abstractmethod
    def _connect(self) -> None:
        """
        Internal method to establish a database connection.
        """
        pass

    def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = None, fetch: bool = True) -> Optional[pd.DataFrame]:
        """
        Executes a SQL query and returns the result as a Pandas DataFrame.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to pass to the query. Defaults to None.
            fetch (bool, optional): Whether to fetch the results. Defaults to True.

        Returns:
            Optional[pd.DataFrame]: The query results as a Pandas DataFrame, or None if fetch is False.

        Raises:
            QueryError: If there is an error executing the query.
        """
        self.connect()  # Ensure connection is established
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    results = cursor.fetchall()
                    if results:
                        # Get column names
                        columns = [desc[0] for desc in cursor.description]
                        # Create the DataFrame
                        df = pd.DataFrame(results, columns=columns)
                        return df
                    else:
                        return pd.DataFrame() # Return empty DataFrame
                else:
                    return None
        except Exception as e:
            logging.error(f"Error executing query: {query} with params: {params}. Error: {e}")
            raise QueryError(f"Error executing query: {e}")

    def commit(self) -> None:
        """
        Commits the current transaction.
        """
        if self.connection is None:
            raise ConnectionError("No active database connection.")
        try:
            self.connection.commit()
        except Exception as e:
            logging.error(f"Error committing transaction: {e}")
            raise QueryError(f"Error committing transaction: {e}")

    def close(self) -> None:
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            logging.info("Database connection closed.")

    def __enter__(self) -> 'DBConnector':
        """
        Context manager entry method.
        """
        self.connect()
        return self

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: type) -> None:
        """
        Context manager exit method.
        """
        self.close()