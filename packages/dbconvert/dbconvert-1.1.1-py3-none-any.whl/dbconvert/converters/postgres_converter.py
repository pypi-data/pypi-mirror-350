from dbconvert.converters.base_converter import BaseConverter

class PostgresConverter(BaseConverter):
    def map_column_type(self, col_type: str) -> str:
        """Override type mapping for PostgreSQL-specific types."""
        type_str = str(col_type).lower()
        
        # Handle PostgreSQL-specific types
        if "json" in type_str or "jsonb" in type_str:
            return "TEXT"  # Store JSON as text in SQLite
        elif "array" in type_str:
            return "TEXT"  # Store arrays as text in SQLite
        elif "uuid" in type_str:
            return "TEXT"  # Store UUID as text in SQLite
        elif "interval" in type_str:
            return "TEXT"  # Store interval as text in SQLite
        elif "bytea" in type_str:
            return "BLOB"  # Store binary data as BLOB in SQLite
            
        # Use base class mapping for other types
        return super().map_column_type(col_type) 