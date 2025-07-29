import pandas as pd
import sqlite3
from .profile import Profiler

class ProbeManager:
    def __init__(self):
        self.profiler = Profiler()
        self.profile_df = None  # Store latest profile here

    def profile(self, df: pd.DataFrame) -> pd.DataFrame:
        self.profile_df = self.profiler.profile(df)
        return self.profile_df

    def summarize(self, null_threshold: float = 20.0, unique_threshold: int = 5) -> pd.DataFrame:
        if self.profile_df is None:
            raise ValueError("No profile found. Please run profile() first.")
        return self.profiler.summarize(self.profile_df, null_threshold, unique_threshold)

    def store_to_sqlite(
        self,
        database: str,
        schema: str,
        table: str,
        db_path: str = "profiles.db"
    ) -> None:
        """
        Store the last profiling dataframe (self.profile_df) to SQLite with metadata.
        """

        if self.profile_df is None:
            raise ValueError("No profile found. Please run profile() first.")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                database TEXT,
                schema TEXT,
                table_name TEXT,
                column_name TEXT,
                dtype TEXT,
                non_null_count INTEGER,
                null_count INTEGER,
                null_percentage REAL,
                unique_count INTEGER,
                sample_value TEXT,
                mean REAL,
                std REAL,
                min REAL,
                max REAL,
                profile_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        for _, row in self.profile_df.iterrows():
            cursor.execute("""
                INSERT INTO profiles (
                    database, schema, table_name, column_name, dtype,
                    non_null_count, null_count, null_percentage, unique_count,
                    sample_value, mean, std, min, max
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                database,
                schema,
                table,
                row.get("column_name"),
                row.get("dtype"),
                row.get("non_null_count"),
                row.get("null_count"),
                row.get("null_percentage"),
                row.get("unique_count"),
                str(row.get("sample_value")) if row.get("sample_value") is not None else None,
                row.get("mean"),
                row.get("std"),
                row.get("min"),
                row.get("max")
            ))

        conn.commit()
        conn.close()
