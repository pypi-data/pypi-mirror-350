# cosmic-probe

**cosmic-probe** is a flexible Python package for profiling pandas DataFrames, supporting quick data exploration and storing profiling history with metadata. It’s designed to be simple to use yet powerful enough to handle data from databases, files, or queries.

---

## Features

- Profile any pandas DataFrame with detailed column statistics
- Summarize anomalies like high null percentages, low uniqueness, and constant columns
- Store profiling reports with metadata to SQLite by default (extensible to other databases)
- Designed as part of the cosmiclode ecosystem, easy to integrate with other cosmic packages

---

## Installation

```bash
pip install cosmic-probe
```

## Quickstart

```python
import pandas as pd
from cosmic_probe import ProbeManager

# Sample DataFrame
data = {
    "age": [25, 30, 22, None, 40],
    "salary": [50000, 60000, 52000, 58000, None],
    "department": ["HR", "IT", "IT", "HR", "Finance"],
}

df = pd.DataFrame(data)

# Initialize ProbeManager
probe = ProbeManager()

# Profile the DataFrame
profile_df = probe.profile(df)
print(profile_df)

# Summarize anomalies
summary_df = probe.summarize()
print(summary_df)

# Store profiling results
probe.store_to_sqlite(database="csv", schema="csv", table="sample_data")
```

## API

### ProbeManager

- `profile(df: pd.DataFrame) -> pd.DataFrame`: Profiles the DataFrame and stores the result internally.

- `summarize(null_threshold=20.0, unique_threshold=5) -> pd.DataFrame`: Summarizes anomalies from the last profile.

- `store_to_sqlite(database: str, schema: str, table: str, db_path: str = "profiles.db")`: Stores the latest profile to SQLite with metadata.

### Profiler

- `profile(df: pd.DataFrame) -> pd.DataFrame`: Core method to generate profile for each column.

- `summarize(profile_df: pd.DataFrame, null_threshold=20.0, unique_threshold=5) -> pd.DataFrame`: Summarizes anomalies in a given profile DataFrame.

## Contribution

Contributions and suggestions are welcome! Please open issues or pull requests on the GitHub repo.

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## ✨ Author

**Vinod Yerrapureddy**  
📧 [yerrapureddyvinodreddy@gmail.com](mailto:yerrapureddyvinodreddy@gmail.com)  
🌐 [vinodreddy.netlify.app](https://vinodreddy.netlify.app)  
🔗 [LinkedIn](https://www.linkedin.com/in/vinod-yerrapureddy-264938161/)  
🍥 Anime fan | 💻 Data engineer | 🛠️ Systems hacker
