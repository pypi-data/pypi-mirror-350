from dbconvert.converters.base_converter import BaseConverter

class MySQLConverter(BaseConverter):
    def map_column_type(self, col_type: str) -> str:
        """Override type mapping for MySQL-specific types."""
        type_str = str(col_type).lower()
        
        # Handle MySQL-specific types
        if "enum" in type_str or "set" in type_str:
            return "TEXT"  # Store ENUM and SET as text in SQLite
        elif "year" in type_str:
            return "INTEGER"  # Store YEAR as INTEGER in SQLite
        elif "bit" in type_str:
            return "BLOB"  # Store BIT as BLOB in SQLite
        elif "geometry" in type_str or "point" in type_str:
            return "BLOB"  # Store spatial types as BLOB in SQLite
            
        # Use base class mapping for other types
        return super().map_column_type(col_type) 