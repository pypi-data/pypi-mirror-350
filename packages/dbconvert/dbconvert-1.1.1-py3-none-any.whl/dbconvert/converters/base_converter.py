from sqlalchemy import create_engine, inspect, text
from typing import Dict, Any
from rich.console import Console

console = Console()

class BaseConverter:
    def __init__(self, conn_str: str):
        self.engine = create_engine(conn_str)
        self.inspector = inspect(self.engine)

    def read_all_tables(self) -> Dict[str, Dict[str, Any]]:
        """Read all tables and their data from the source database."""
        tables = {}
        with self.engine.connect() as conn:
            for table_name in self.inspector.get_table_names():
                console.print(f"[yellow]Reading table: {table_name}[/yellow]")
                
                # Get column information
                columns = self.inspector.get_columns(table_name)
                
                # Get primary keys
                primary_keys = self.inspector.get_pk_constraint(table_name)
                
                # Get foreign keys
                foreign_keys = self.inspector.get_foreign_keys(table_name)
                
                # Get table data
                data = conn.execute(text(f"SELECT * FROM {table_name}")).fetchall()
                
                tables[table_name] = {
                    "columns": columns,
                    "primary_keys": primary_keys,
                    "foreign_keys": foreign_keys,
                    "data": data
                }
                
        return tables

    def map_column_type(self, col_type: str) -> str:
        """Map source database type to SQLite type."""
        type_str = str(col_type).lower()
        
        if "int" in type_str:
            return "INTEGER"
        elif "char" in type_str or "text" in type_str:
            return "TEXT"
        elif "bool" in type_str:
            return "BOOLEAN"
        elif "float" in type_str or "double" in type_str or "numeric" in type_str:
            return "REAL"
        elif "date" in type_str or "time" in type_str:
            return "TEXT"  # SQLite doesn't have native date/time types
        else:
            return "TEXT"  # Default to TEXT for unknown types 