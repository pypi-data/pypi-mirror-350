import pyodbc
from .db_connector import DBConnector
from .exceptions import ConnectionError

class SQLServerConnector(DBConnector):
    """
    Database connector for SQL Server.
    """
    def __init__(self, config: dict):
        super().__init__(config)

    def validate_config(self):
        super().validate_config()
        if self.config['type'].lower() not in ('sqlserver', 'mssql'):
            raise ValueError(f"Invalid database type. Expected 'sqlserver' or 'mssql', got '{self.config['type']}'")

    def _connect(self):
        """
        Establishes a connection to a SQL Server database.
        """
        try:
            connection_string = f"""
                DRIVER={{ODBC Driver 17 for SQL Server}};  # Or another suitable driver
                SERVER={self.config['host']},{self.config.get('port', 1433)};  # Default SQL Server port
                DATABASE={self.config['database']};
                UID={self.config['user']};
                PWD={self.config['password']};
                TrustServerCertificate=yes; # For local dev environments.  DO NOT USE IN PRODUCTION
            """
            self.connection = pyodbc.connect(connection_string)
        except pyodbc.Error as e:
            raise ConnectionError(f"Failed to connect to SQL Server: {e}")
