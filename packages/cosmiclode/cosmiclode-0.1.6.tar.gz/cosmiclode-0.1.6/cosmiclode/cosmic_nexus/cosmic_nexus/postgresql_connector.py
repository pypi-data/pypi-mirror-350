import psycopg2
from .db_connector import DBConnector # Import the abstract class
from .exceptions import ConnectionError # Import custom exception

class PostgreSQLConnector(DBConnector):
    """
    Database connector for PostgreSQL.
    """
    def __init__(self, config: dict):
        super().__init__(config)

    def validate_config(self):
        super().validate_config()
        if self.config['type'].lower() != 'postgresql':
            raise ValueError(f"Invalid database type. Expected 'postgresql', got '{self.config['type']}'")

    def _connect(self):
        """
        Establishes a connection to a PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.config['host'],
                port=self.config.get('port', 5432),  # Default PostgreSQL port
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password']
            )
        except psycopg2.Error as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {e}")