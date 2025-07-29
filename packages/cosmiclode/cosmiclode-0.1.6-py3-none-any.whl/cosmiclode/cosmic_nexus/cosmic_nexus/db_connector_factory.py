from typing import Dict, Any
from .db_connector import DBConnector # Import from .db_connector
from .postgresql_connector import PostgreSQLConnector # Import from .postgresql_connector
from .mysql_connector import MySQLConnector # Import from .mysql_connector
from .sqlserver_connector import SQLServerConnector # Import from .sqlserver_connector

class DBConnectorFactory:
    """
    Factory class to create database connectors.
    """
    @staticmethod
    def create_connector(config: Dict[str, Any]) -> DBConnector:
        """
        Creates a database connector based on the specified type.

        Args:
            config (dict): A dictionary containing database connection parameters,
                           including the 'type' key.

        Returns:
            DBConnector: An instance of the appropriate DBConnector subclass.

        Raises:
            ValueError: If an unsupported database type is specified.
        """
        db_type = config.get('type', '').lower()
        if db_type == 'postgresql':
            return PostgreSQLConnector(config)
        elif db_type == 'mysql':
            return MySQLConnector(config)
        elif db_type in ('sqlserver', 'mssql'):
            return SQLServerConnector(config)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")