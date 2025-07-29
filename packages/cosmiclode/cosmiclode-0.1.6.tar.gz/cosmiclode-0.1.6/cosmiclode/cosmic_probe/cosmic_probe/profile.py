import pandas as pd
import numpy as np

class Profiler:
    def profile(self, df: pd.DataFrame) -> pd.DataFrame:
        profile_data = []

        for col in df.columns:
            series = df[col]
            col_profile = {
                "column_name": col,
                "dtype": str(series.dtype),
                "non_null_count": series.notnull().sum(),
                "null_count": series.isnull().sum(),
                "null_percentage": round(series.isnull().mean() * 100, 2),
                "unique_count": series.nunique(dropna=True),
                "sample_value": series.dropna().iloc[0] if not series.dropna().empty else None,
            }

            if pd.api.types.is_numeric_dtype(series):
                col_profile.update({
                    "mean": series.mean(),
                    "std": series.std(),
                    "min": series.min(),
                    "max": series.max(),
                })
            elif pd.api.types.is_datetime64_any_dtype(series):
                col_profile.update({
                    "min": series.min(),
                    "max": series.max(),
                })

            profile_data.append(col_profile)

        return pd.DataFrame(profile_data)
