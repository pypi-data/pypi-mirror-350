import sqlite3
import os
from .table import Table

class Database:
    """Represents a SQLite database connection."""

    def __init__(self, path: str) -> None:
        """
        Initializes the database connection.

        Args:
            path (str): Path to the SQLite database file.
        
        Example:
        # In memory
        db = Database(":memory:")

        # On disk
        db = Database("my_database.db")
        """
        self.path = path
        self.connection = sqlite3.connect(path)

    def table(self, name: str) -> Table:
        """
        Returns a Table object for interacting with a specific table.

        Args:
            name (str): Name of the table.

        Returns:
            Table: A Table object for interacting with the specified table.
        """
        return Table(self.connection, name)

    def vacuum(self) -> None:
        """Optimizes the database by running the VACUUM command."""
        self.connection.execute("VACUUM")

    def close(self) -> None:
        """Closes the database connection."""
        self.connection.close()

    def connect(self) -> None:
        """Reconnects to the database."""
        self.connection = sqlite3.connect(self.path)

    def reset(self, confirm: bool = False) -> None:
        """
        Resets the database by deleting all tables and data.

        Args:
            confirm (bool): If True, skips confirmation prompt.
        """
        if not confirm:
            raise ValueError("Confirmation required to reset the database.")

        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
        self.connection.commit()

    def delete(self, confirm: bool = False) -> None:
        """
        Deletes the database file.

        Args:
            confirm (bool): If True, skips confirmation prompt.
        """
        if not confirm:
            raise ValueError("Confirmation required to delete the database file.")

        self.close()
        if os.path.exists(self.path):
            os.remove(self.path)
        else:
            raise FileNotFoundError("Database file does not exist.")
    
    def execute_sql(self, sql: str) -> None:
        """
        Executes a raw SQL command.

        Args:
            sql (str): The SQL command to execute.
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()