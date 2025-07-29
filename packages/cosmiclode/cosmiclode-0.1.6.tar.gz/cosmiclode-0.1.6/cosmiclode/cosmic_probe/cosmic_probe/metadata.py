from dataclasses import dataclass

@dataclass
class DatasetMetadata:
    database: str
    schema: str
    table: str

    def to_id(self) -> str:
        return f"{self.database}.{self.schema}.{self.table}"
