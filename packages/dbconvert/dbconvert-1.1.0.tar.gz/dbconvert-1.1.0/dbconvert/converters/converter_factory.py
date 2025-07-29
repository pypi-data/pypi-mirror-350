from typing import Optional
from dbconvert.converters.base_converter import BaseConverter
from dbconvert.converters.postgres_converter import PostgresConverter
from dbconvert.converters.mysql_converter import MySQLConverter
from dbconvert.core.enums import DatabaseType

class ConverterFactory:
    registry = {
        DatabaseType.POSTGRES.value: PostgresConverter,
        DatabaseType.MYSQL.value: MySQLConverter
    }
    
    @staticmethod
    def create_converter(db_type: str, conn_str: str) -> Optional[BaseConverter]:
        converter_cls = ConverterFactory.registry.get(db_type)
        if not converter_cls:
            raise ValueError(f"Unsupported database type: {db_type}") 
        return converter_cls(conn_str)