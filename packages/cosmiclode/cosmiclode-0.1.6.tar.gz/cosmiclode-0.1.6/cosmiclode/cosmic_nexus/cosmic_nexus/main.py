import logging
from .db_connector_factory import DBConnectorFactory # Import from .db_connector_factory
from .exceptions import ConnectionError, QueryError # Import from .exceptions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to demonstrate the usage of the database connectors.
    """
    # PostgreSQL Example
    postgresql_config = {
        "type": "postgresql",
        "host": "localhost",
        "database": "your_postgresql_database",
        "user": "your_postgresql_user",
        "password": "your_postgresql_password",
        "port": 5432,
    }

    # MySQL Example
    mysql_config = {
        "type": "mysql",
        "host": "localhost",
        "database": "your_mysql_database",
        "user": "your_mysql_user",
        "password": "your_mysql_password",
    }

    # SQL Server Example
    sqlserver_config = {
        "type": "sqlserver",
        "connection_string": "DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_user;PWD=your_password",
    }

    # Using the Factory to create connectors
    try:
        postgres_connector = DBConnectorFactory.create_connector(postgresql_config)
        with postgres_connector as db:
            df = db.execute_query("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            logging.info(f"PostgreSQL Tables:\n{df}")

        mysql_connector = DBConnectorFactory.create_connector(mysql_config)
        with mysql_connector as db:
            df = db.execute_query("SHOW TABLES;")
            logging.info(f"MySQL Tables:\n{df}")

        sqlserver_connector = DBConnectorFactory.create_connector(sqlserver_config)
        with sqlserver_connector as db:
            df = db.execute_query("SELECT table_name FROM information_schema.tables;")
            logging.info(f"SQL Server Tables:\n{df}")

    except (ConnectionError, QueryError) as e:
        logging.error(f"An error occurred: {e}")
    except ValueError as e:
        logging.error(f"Configuration error: {e}")

if __name__ == "__main__":
    main()