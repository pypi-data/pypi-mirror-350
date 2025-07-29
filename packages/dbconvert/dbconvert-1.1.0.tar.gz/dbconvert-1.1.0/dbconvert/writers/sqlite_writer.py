import sqlite3
from typing import Dict, Any
from rich.progress import Progress
from rich.console import Console

console = Console()

class SQLiteWriter:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def write_all_tables(self, tables: Dict[str, Dict[str, Any]]):
        """Write all tables and their data to SQLite database."""
        cursor = self.conn.cursor()
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Writing tables...", total=len(tables))
            
            for table_name, meta in tables.items():
                console.print(f"[yellow]Creating table: {table_name}[/yellow]")
                
                # Create table with columns
                columns = meta["columns"]
                col_defs = []
                
                # Add primary key constraints
                pk_columns = meta.get("primary_keys", {}).get("constrained_columns", [])
                
                for col in columns:
                    col_name = col["name"]
                    col_type = str(col["type"])
                    nullable = "NOT NULL" if not col.get("nullable", True) else ""
                    is_pk = col_name in pk_columns
                    pk_constraint = "PRIMARY KEY" if is_pk else ""
                    
                    col_def = f"{col_name} {col_type} {nullable} {pk_constraint}".strip()
                    col_defs.append(col_def)
                
                # Create table
                create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(col_defs)})"
                cursor.execute(create_sql)
                
                # Insert data
                if meta["data"]:
                    placeholders = ", ".join(["?"] * len(columns))
                    insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                    
                    # Batch insert for better performance
                    cursor.executemany(insert_sql, meta["data"])
                
                progress.advance(task)
        
        # Add foreign key constraints
        for table_name, meta in tables.items():
            for fk in meta.get("foreign_keys", []):
                fk_sql = f"""
                ALTER TABLE {table_name}
                ADD CONSTRAINT fk_{table_name}_{fk['constrained_columns'][0]}
                FOREIGN KEY ({', '.join(fk['constrained_columns'])})
                REFERENCES {fk['referred_table']} ({', '.join(fk['referred_columns'])})
                """
                try:
                    cursor.execute(fk_sql)
                except sqlite3.OperationalError as e:
                    console.print(f"[red]Warning: Could not add foreign key constraint: {str(e)}[/red]")
        
        self.conn.commit()
        self.conn.close()
        
        console.print(f"[green]Successfully wrote database to: {self.db_path}[/green]") 