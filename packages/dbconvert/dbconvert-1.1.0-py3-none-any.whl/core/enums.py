from enum import Enum

class DatabaseType(Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    
    @classmethod
    def values(cls):
        return [db_type.value for db_type in cls] 