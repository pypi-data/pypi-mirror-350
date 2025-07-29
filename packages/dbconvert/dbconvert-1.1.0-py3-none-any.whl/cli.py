import typer
from rich.console import Console
from dbconvert.converters.converter_factory import ConverterFactory
from dbconvert.writers.sqlite_writer import SQLiteWriter
from dbconvert.core.enums import DatabaseType
import os

app = typer.Typer()
console = Console()

@app.command(name="supported-databases")
def supported_databases():
    """
    Show supported database types for conversion.
    """
    console.print("[cyan]Supported database types:[/cyan]")
    for db_type in DatabaseType.values():
        console.print(f"  • {db_type}")

@app.command()
def convert(
    source: str = typer.Option(..., help=f"Source database type ({', '.join(DatabaseType.values())})"),
    conn: str = typer.Option(..., help="Source database connection string"),
    sqlite: str = typer.Option(..., help="Target SQLite database file path")
):
    """
    Convert a PostgreSQL or MySQL database to SQLite.
    """
    try:
        # Validate source database type
        if source not in DatabaseType.values():
            raise ValueError(f"Unsupported source database type: {source}")
        
        # Validate connection string
        if not conn:
            raise ValueError("Connection string cannot be empty")
        
        # Validate SQLite path
        sqlite_dir = os.path.dirname(sqlite)
        if sqlite_dir and not os.path.exists(sqlite_dir):
            os.makedirs(sqlite_dir)
        
        # Create converter using factory
        converter = ConverterFactory.create_converter(source, conn)
        
        # Read source database
        console.print("[cyan]Reading source database...[/cyan]")
        tables = converter.read_all_tables()
        
        # Write to SQLite
        console.print("[cyan]Writing to SQLite database...[/cyan]")
        writer = SQLiteWriter(sqlite)
        writer.write_all_tables(tables)
        
        console.print("[green]✅ Conversion completed successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()