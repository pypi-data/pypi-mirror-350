# Cosmic Nexus 🚀

**Cosmic Nexus** is a Python package under the `cosmiclode` monorepo designed to provide robust and efficient database connectivity. It simplifies working with PostgreSQL, MySQL, and SQL Server by offering a unified interface with context management, error handling, and Pandas integration.

---

## ✨ Features

- **Database Abstraction**: Consistent interface across supported databases.
- **Connection Management**: Automatic connection handling and pooling (if supported).
- **Factory Pattern**: Easily create connectors using `DBConnectorFactory`.
- **Context Management**: Ensures clean resource management with `with` blocks.
- **Error Handling**: Custom exceptions for clear debugging.
- **Pandas Integration**: Query results are returned as DataFrames.

---

## 📦 Installation

```bash
pip install cosmiclode.cosmic-nexus
```
To install database-specific extras:

```bash
pip install "cosmiclode.cosmic-nexus[postgresql]"
pip install "cosmiclode.cosmic-nexus[mysql]"
pip install "cosmiclode.cosmic-nexus[sqlserver]"
```

## 🚀 Quick Start

```python
from cosmiclode.cosmic_nexus import DBConnectorFactory
from cosmiclode.cosmic_nexus.exceptions import ConnectionError, QueryError

config = {
    "type": "postgresql",
    "host": "localhost",
    "database": "my_db",
    "user": "user",
    "password": "pass",
    "port": 5432
}

try:
    connector = DBConnectorFactory.create_connector(config)
    with connector as db:
        df = db.execute_query("SELECT * FROM my_table;")
        print(df)
except (ConnectionError, QueryError) as e:
    print(f"Error: {e}")
```

## 📚 Usage Notes

- Use `%s` placeholders for parameters to avoid SQL injection.
- SQL Server requires a full ODBC connection string in the config.

```python
sqlserver_config = {
    "type": "sqlserver",
    "connection_string": "DRIVER={ODBC Driver 17 for SQL Server};SERVER=...;UID=...;PWD=..."
}
```


## 📝 License  
This project is licensed under the MIT License.

---

## ✨ Author  
**Vinod Yerrapureddy**  
📧 yerrapureddyvinodreddy@gmail.com  
🌐 [vinodreddy.netlify.app](https://vinodreddy.netlify.app)  
🔗 [LinkedIn](https://linkedin.com/in/your-profile)  
🍥 Anime fan | 💻 Data engineer | 🛠️ Systems hacker
