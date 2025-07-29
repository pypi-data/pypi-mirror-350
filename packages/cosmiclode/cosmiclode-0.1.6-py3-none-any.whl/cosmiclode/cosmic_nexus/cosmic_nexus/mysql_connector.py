import mysql.connector
from .db_connector import DBConnector
from .exceptions import ConnectionError

class MySQLConnector(DBConnector):
    """
    Database connector for MySQL.
    """
    def __init__(self, config: dict):
        super().__init__(config)

    def validate_config(self):
        super().validate_config()
        if self.config['type'].lower() != 'mysql':
            raise ValueError(f"Invalid database type. Expected 'mysql', got '{self.config['type']}'")

    def _connect(self):
        """
        Establishes a connection to a MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                port=self.config.get('port', 3306),  # Default MySQL port
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password']
            )
        except mysql.connector.Error as e:
            raise ConnectionError(f"Failed to connect to MySQL: {e}")