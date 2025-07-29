import pandas as pd
from .manager import ProbeManager

# Create some dummy data
data = {
    "age": [25, 30, 22, None, 40, 40, 40],
    "salary": [50000, 60000, 52000, 58000, None, 60000, 60000],
    "department": ["HR", "IT", "IT", "HR", "Finance", None, "Finance"],
    "constant_col": [1, 1, 1, 1, 1, 1, 1],  # constant value column
    "nulls_col": [None, None, None, None, None, None, None],  # all nulls
}

df = pd.DataFrame(data)

# Initialize ProbeManager
probe = ProbeManager()

# Profile the dataframe
profile_df = probe.profile(df)
print("Profile Report:")
print(profile_df)

# Summarize anomalies
summary_df = probe.summarize(null_threshold=20, unique_threshold=2)
print("\nAnomaly Summary:")
print(summary_df)

# Store the profile in SQLite DB with metadata
probe.store_to_sqlite(database="dummy_db", schema="public", table="employee_data")

print("\nProfile stored in SQLite database 'profiles.db'")
