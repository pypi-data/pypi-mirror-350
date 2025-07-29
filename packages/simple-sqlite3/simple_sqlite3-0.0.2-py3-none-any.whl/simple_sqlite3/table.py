import sqlite3
import json
import csv
import re
from typing import Any, Iterable, Optional, Union
from .exceptions import TableNotFoundError, InvalidDataError, SchemaMismatchError
import logging
from datetime import datetime
from collections import defaultdict

# Set up a logger for the Table class
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # Default log level is WARNING

# Optional: Add a console handler only if explicitly enabled
if not logger.hasHandlers():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)


def enable_debug_logging():
    """
    Enables debug-level logging for the Table class.
    """
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setLevel(logging.DEBUG)

def _validate_identifier(identifier: str) -> str:
    """
    Validates that the identifier (table/column name) is safe for SQL usage.
    Only allows alphanumeric characters and underscores, and must not start with a digit.
    Raises ValueError if invalid.
    """
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', identifier):
        raise ValueError(f"Invalid SQL identifier: {identifier}")
    return identifier

def validate_cli_identifier(identifier: str) -> str:
    """Validate identifier for CLI usage (table/column names)."""
    return _validate_identifier(identifier)

def _parse_dates_recursive(obj):
    if isinstance(obj, dict):
        return {k: _parse_dates_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_parse_dates_recursive(v) for v in obj]
    elif isinstance(obj, str):
        try:
            return datetime.fromisoformat(obj)
        except ValueError:
            return obj
    else:
        return obj

class Table:
    def __init__(self, connection_or_path: Union[sqlite3.Connection, str], name: str) -> None:
        """
        Initializes the Table object.

        Args:
            connection_or_path (sqlite3.Connection | str): SQLite connection or database path.
            name (str): Name of the table.
        """
        if isinstance(connection_or_path, str):
            self.connection = sqlite3.connect(connection_or_path)
        else:
            self.connection = connection_or_path
        self.cursor = self.connection.cursor()
        self.name = _validate_identifier(name)
        # Enable WAL mode (default)
        self.cursor.execute("PRAGMA journal_mode=WAL;")
        self.connection.commit()
        logger.info("WAL mode enabled.")
    
    def insert(self, data: Union[dict, Iterable[dict]], force: bool = True, schema: Optional[dict] = None) -> None:
        """
        Inserts data into the table. Automatically creates or updates the table schema if needed.
        Handles nested data structures by serializing them into JSON strings.

        Args:
            data (dict | Iterable[dict]): Data to insert.
            force (bool): Whether to add missing columns automatically. Defaults to True.
            schema (dict, optional): Exact schema for the data. If provided, skips schema inference.
        """
        logger.debug(f"Inserting data into table '{self.name}': {data}")
        # Normalize data to a list of dicts
        if isinstance(data, dict):
            data = [data]
        data = list(data)
        if not all(isinstance(entry, dict) for entry in data):
            raise InvalidDataError("Data must be a dictionary or an iterable of dictionaries.")

        # Validate all column names before proceeding
        for entry in data:
            for key in entry.keys():
                _validate_identifier(key)

        # Serialize nested structures into JSON strings and check serializability
        def custom_serializer(obj):
            if isinstance(obj, datetime):  # Handle datetime objects
                return obj.strftime("%Y-%m-%d %H:%M:%S")  # SQLite-compatible format
            raise TypeError(f"Type {type(obj)} not serializable")

        for entry in data:
            for key, value in entry.items():
                if isinstance(value, (dict, list)):
                    try:
                        entry[key] = json.dumps(value, default=custom_serializer)
                    except TypeError as e:
                        raise InvalidDataError(f"Value for column '{key}' could not be serialized: {e}")
                else:
                    try:
                        json.dumps(value, default=custom_serializer)
                    except TypeError as e:
                        raise InvalidDataError(f"Value for column '{key}' could not be serialized: {e}")

        all_columns = {key for entry in data for key in entry.keys()}
        existing_columns = {col[1]: col[2] for col in self.cursor.execute(f"PRAGMA table_info({self.name})")}

        if schema:
            # Use provided schema to create or update the table
            if not existing_columns:
                columns_def = ', '.join(f"{col} {schema[col]}" for col in schema)
                self.cursor.execute(f"CREATE TABLE {self.name} ({columns_def})")
            elif force:
                for col in schema.keys():
                    if col not in existing_columns:
                        self.cursor.execute(f"ALTER TABLE {self.name} ADD COLUMN {col} {schema[col]}")
        else:
            # Infer schema if not provided
            if not existing_columns:
                columns_def = ', '.join(f"{col} {self._infer_sqlite_type(data[0].get(col))}" for col in all_columns)
                self.cursor.execute(f"CREATE TABLE {self.name} ({columns_def})")
            elif force:
                for col in all_columns - existing_columns.keys():
                    self.cursor.execute(f"ALTER TABLE {self.name} ADD COLUMN {col} {self._infer_sqlite_type(data[0].get(col))}")

        # Group entries by their set of columns for efficient batch insert
        grouped = defaultdict(list)
        for entry in data:
            key = tuple(sorted(entry.keys()))
            grouped[key].append(entry)

        for columns in grouped:
            columns_str = ', '.join(columns)
            placeholders = ', '.join('?' * len(columns))
            values = [tuple(entry[col] for col in columns) for entry in grouped[columns]]
            if len(values) > 1:
                self.cursor.executemany(
                    f"INSERT INTO {self.name} ({columns_str}) VALUES ({placeholders})", values
                )
            else:
                self.cursor.execute(
                    f"INSERT INTO {self.name} ({columns_str}) VALUES ({placeholders})", values[0]
                )
        self.connection.commit()
        logger.info(f"Data inserted successfully into table '{self.name}'")

    def update(self, sql_fragment: str, params: Optional[tuple] = None) -> None:
        """
        Update rows in the table using a SQL fragment, e.g. "SET age = 35 WHERE name = 'Alice'".
        Supports parameterized queries and robustly handles complex data structures.
        Complex data structures (dict, list, set, tuple) will be serialized to JSON.
    
        Args:
            sql_fragment (str): The SQL fragment after 'UPDATE <table>'.
            params (tuple, optional): Parameters for the SQL statement.
    
        Raises:
            ValueError: If the SQL fragment does not start with SET.
        """
        if not sql_fragment.strip().upper().startswith("SET"):
            raise ValueError("Update statement must start with SET")
    
        # Serialize complex data structures in params
        if params:
            def serialize(val):
                if isinstance(val, (dict, list, set, tuple)):
                    return json.dumps(val)
                return val
            params = tuple(serialize(v) for v in params)
    
        sql = f"UPDATE {self.name} {sql_fragment}"
        self.cursor.execute(sql, params or ())
        self.connection.commit()

    def query(self, query: str, params: Optional[tuple] = None, auto_parse_dates: bool = False) -> list[dict]:
        """
        Executes a query and returns the raw results from SQLite.
        Only allows parameterized queries or SELECT statements with optional WHERE clauses.
        Optionally parses date columns as datetime objects.
        """
        logger.debug(f"Executing query: {query} with params: {params}")
        if not query.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed for safety.")
        if "FROM" not in query.upper():
            parts = query.split("WHERE", 1)
            select_part = parts[0].strip()
            where_part = f"WHERE {parts[1]}" if len(parts) > 1 else ""
            if select_part.upper().startswith("SELECT"):
                query = f"{select_part} FROM {self.name} {where_part}".strip()
        if ";" in query:
            raise ValueError("Semicolons are not allowed in queries.")
        try:
            self.cursor.execute(query, params or ())
            logger.info(f"Query executed successfully: {query}")
        except sqlite3.OperationalError as e:
            logger.error(f"Query failed: {query} - Error: {e}")
            if "no such table" in str(e):
                raise TableNotFoundError(f"Table '{self.name}' does not exist.")
            raise
        rows = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        if auto_parse_dates:
            for row in results:
                for col, val in row.items():
                    # Try to decode JSON fields
                    if isinstance(val, str):
                        try:
                            if (val.startswith("{") and val.endswith("}")) or (val.startswith("[") and val.endswith("]")):
                                val = json.loads(val)
                        except Exception:
                            pass
                    # Recursively parse dates
                    row[col] = _parse_dates_recursive(val)
        return results

    def _infer_sqlite_type(self, value: Any) -> str:
        """
        Infers the SQLite data type for a given Python value.
    
        Args:
            value: The Python value to infer the type for.
    
        Returns:
            str: A string representing the SQLite data type.
        """
        if isinstance(value, bool):
            return "BOOLEAN"
        if isinstance(value, int):
            return "INTEGER"
        if isinstance(value, float):
            return "REAL"
        if isinstance(value, bytes) or isinstance(value, bytearray):
            return "BLOB"
        if isinstance(value, datetime):
            return "DATETIME"
        return "TEXT"

    def recalibrate(self, data: Optional[Union[dict, Iterable[dict]]] = None) -> None:
        """
        Recalibrates the table schema based on the provided data or existing data.

        Args:
            data (dict | Iterable[dict], optional): Optional data to infer the schema from.

        Raises:
            SchemaMismatchError: If the schema cannot be recalibrated due to conflicting types.
        """
        existing_columns = {col[1]: col[2] for col in self.cursor.execute(f"PRAGMA table_info({self.name})")}
        all_columns = set(existing_columns.keys())
        if data:
            if isinstance(data, dict):
                data = [data]
            all_columns.update(key for entry in data for key in entry.keys())

        column_types = {}
        for column in all_columns:
            values = self.cursor.execute(f"SELECT {column} FROM {self.name} WHERE {column} IS NOT NULL").fetchall()
            inferred_types = {self._infer_sqlite_type(value[0]) for value in values if value}
            column_types[column] = "TEXT" if len(inferred_types) > 1 or not inferred_types else inferred_types.pop()

        for column, inferred_type in column_types.items():
            if column not in existing_columns:
                self.cursor.execute(f"ALTER TABLE {self.name} ADD COLUMN {column} {inferred_type}")
            elif existing_columns[column] != inferred_type:
                raise SchemaMismatchError(
                    f"Column '{column}' has a conflicting type. "
                    f"Expected: {existing_columns[column]}, Found: {inferred_type}"
                )
        self.connection.commit()

    def get_schema(self) -> list[tuple]:
        """
        Retrieves the schema of the table.

        Returns:
            list[tuple]: A list of tuples representing the table schema.
        """
        return self.cursor.execute(f"PRAGMA table_info({self.name})").fetchall()

    def rename_column(self, old_name: str, new_name: str) -> None:
        """
        Renames a column in the table.

        Args:
            old_name (str): The current name of the column.
            new_name (str): The new name for the column.
        """
        old_name = _validate_identifier(old_name)
        new_name = _validate_identifier(new_name)
        existing_columns = [col[1] for col in self.cursor.execute(f"PRAGMA table_info({self.name})")]
        if old_name in existing_columns and new_name not in existing_columns:
            self.cursor.execute(f"ALTER TABLE {self.name} RENAME COLUMN {old_name} TO {new_name}")
            self.connection.commit()

    def drop_columns(self, *args: str) -> None:
        """
        Drops specified columns from the table.

        Args:
            *args (str): Column names to drop.
        """
        args = tuple(_validate_identifier(arg) for arg in args)
        existing_columns = [col[1] for col in self.cursor.execute(f"PRAGMA table_info({self.name})")]
        columns_to_keep = [col for col in existing_columns if col not in args]

        if not columns_to_keep:
            # If no columns remain, drop the table
            self.cursor.execute(f"DROP TABLE {self.name}")
            self.connection.commit()
            return

        temp_table = f"{self.name}_temp"
        temp_table = _validate_identifier(temp_table)
        column_definitions = [f"{col[1]} {col[2]}" for col in self.cursor.execute(f"PRAGMA table_info({self.name})") if col[1] in columns_to_keep]

        # Atomic operation to ensure data integrity
        try:
            self.connection.execute("BEGIN")
            self.cursor.execute(f"CREATE TABLE {temp_table} ({', '.join(column_definitions)})")
            self.cursor.execute(f"INSERT INTO {temp_table} SELECT {', '.join(columns_to_keep)} FROM {self.name}")
            self.cursor.execute(f"DROP TABLE {self.name}")
            self.cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {self.name}")
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Failed to drop columns {args} from table '{self.name}': {e}")
            raise

    def keep_columns(self, *args: str) -> None:
        """
        Keeps only the specified columns in the table, dropping all others.

        Args:
            *args (str): Column names to keep.

        Raises:
            ValueError: If no valid columns to keep are provided.
        """
        args = tuple(_validate_identifier(arg) for arg in args)
        existing_columns = [col[1] for col in self.cursor.execute(f"PRAGMA table_info({self.name})")]
        columns_to_keep = [col for col in existing_columns if col in args]

        if not columns_to_keep:
            raise ValueError("No valid columns to keep were provided.")

        temp_table = f"{self.name}_temp"
        temp_table = _validate_identifier(temp_table)
        column_definitions = [
            f"{col[1]} {col[2]}"
            for col in self.cursor.execute(f"PRAGMA table_info({self.name})")
            if col[1] in columns_to_keep
        ]

        # Atomic operation to ensure data integrity
        try:
            self.connection.execute("BEGIN")
            self.cursor.execute(f"CREATE TABLE {temp_table} ({', '.join(column_definitions)})")
            self.cursor.execute(f"INSERT INTO {temp_table} SELECT {', '.join(columns_to_keep)} FROM {self.name}")
            self.cursor.execute(f"DROP TABLE {self.name}")
            self.cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {self.name}")
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Failed to keep columns {args} in table '{self.name}': {e}")
            raise

    def delete_duplicates(self, by: Optional[list[str]] = None) -> None:
        """
        Deletes duplicate rows from the table.

        Args:
            by (list[str], optional): Optional list of column names to determine duplicates. Defaults to all columns.
        """
        if by is None:
            by = [col[1] for col in self.cursor.execute(f"PRAGMA table_info({self.name})")]
        by = [_validate_identifier(col) for col in by]
        self.cursor.execute(f"""
            DELETE FROM {self.name}
            WHERE ROWID NOT IN (
                SELECT MIN(ROWID)
                FROM {self.name}
                GROUP BY {', '.join(by)}
            )
        """)
        self.connection.commit()

    def dropna(self, how: str = 'any', axis: int = 0) -> None:
        """
        Drops rows or columns with missing values (NULL).

        Args:
            how (str): 'any' (default) drops rows/columns with any NULL values, 'all' drops rows/columns where all values are NULL.
            axis (int): 0 (default) drops rows, 1 drops columns.

        Raises:
            ValueError: If invalid values are provided for 'how' or 'axis'.
        """
        if how not in ['any', 'all']:
            raise ValueError("Invalid value for 'how'. Use 'any' or 'all'.")
        if axis not in [0, 1]:
            raise ValueError("Invalid value for 'axis'. Use 0 (rows) or 1 (columns).")

        if axis == 0:  # Drop rows
            if how == 'any':
                conditions = " OR ".join(f"{col[1]} IS NULL" for col in self.cursor.execute(f"PRAGMA table_info({self.name})"))
                self.cursor.execute(f"DELETE FROM {self.name} WHERE {conditions}")
            else:  # how == 'all'
                conditions = " AND ".join(f"{col[1]} IS NULL" for col in self.cursor.execute(f"PRAGMA table_info({self.name})"))
                self.cursor.execute(f"DELETE FROM {self.name} WHERE {conditions}")
        else:  # Drop columns
            columns = [col[1] for col in self.cursor.execute(f"PRAGMA table_info({self.name})")]
            for col in columns:
                count_query = f"SELECT COUNT(*) FROM {self.name} WHERE {col} IS NOT NULL"
                count = self.cursor.execute(count_query).fetchone()[0]
                if (how == 'any' and count == 0) or (how == 'all' and count == 0):
                    self.drop_columns(col)

        self.connection.commit()

    def execute_sql(self, sql: str, params: Optional[tuple] = None) -> None:
        """
        Executes a raw SQL query.
    
        WARNING: This method executes raw SQL. Do NOT use with untrusted input.
        Always use parameterized queries for user data and validate identifiers.
    
        Args:
            sql (str): The SQL query to execute.
            params (tuple, optional): Optional parameters for the query.
        """
        self.cursor.execute(sql, params or ())
        self.connection.commit()

    def backup(self, backup_name: str) -> None:
        """
        Creates a backup of the table by copying its data to a new table.

        Args:
            backup_name (str): The name of the backup table.
        """
        backup_name = _validate_identifier(backup_name)
        self.cursor.execute(f"CREATE TABLE {backup_name} AS SELECT * FROM {self.name}")
        self.connection.commit()

    def truncate(self) -> None:
        """Truncates the table by deleting all rows while keeping the structure intact."""
        self.cursor.execute(f"DELETE FROM {self.name}")
        self.connection.commit()

    def reset(self, confirm: bool = False) -> None:
        """
        Deletes all rows in the table while keeping the structure intact.

        Args:
            confirm (bool): If True, skips confirmation prompt. Defaults to False.

        Raises:
            ValueError: If confirmation is not provided.
        """
        if not confirm:
            logger.warning("Reset operation aborted: confirmation not provided.")
            raise ValueError("Confirmation required to reset the table. Pass confirm=True to proceed.")
        logger.info(f"Resetting table '{self.name}'")
        self.truncate()
        logger.info(f"Table '{self.name}' reset successfully")

    def delete(self, confirm: bool = False) -> None:
        """
        Deletes the table from the database.

        Args:
            confirm (bool): If True, skips confirmation prompt. Defaults to False.

        Raises:
            ValueError: If confirmation is not provided.
        """
        if not confirm:
            raise ValueError("Confirmation required to delete the table. Pass confirm=True to proceed.")
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.name}")
        self.connection.commit()
    
    def rename(self, new_name: str) -> None:
        """
        Renames the table.

        Args:
            new_name (str): The new name for the table.
        """
        new_name = _validate_identifier(new_name)
        self.cursor.execute(f"ALTER TABLE {self.name} RENAME TO {new_name}")
        self.connection.commit()
        self.name = new_name
        logger.info(f"Table renamed to '{new_name}'")

    def export_to_csv(self, file_path: str, batch_size: int = 1000) -> None:
        """
        Exports the table's data to a CSV file, with large datasets handled in batches.

        Args:
            file_path (str): Path to the CSV file.
            batch_size (int): Number of rows to fetch per batch. Defaults to 1000.
        """
        self.cursor.execute(f"SELECT * FROM {self.name}")
        columns = [description[0] for description in self.cursor.description]
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            while True:
                rows = self.cursor.fetchmany(batch_size)
                if not rows:
                    break
                writer.writerows([dict(zip(columns, row)) for row in rows])
        logger.info(f"Data exported to CSV file: {file_path}")
   
    def export_to_json(self, file_path: str, batch_size: int = 1000) -> None:
        """
        Exports the table's data to a JSON file, with large datasets handled in batches.
        Attempts to decode JSON strings back to objects for nested fields.
        """
        self.cursor.execute(f"SELECT * FROM {self.name}")
        columns = [description[0] for description in self.cursor.description]
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write("[\n")
            first = True
            while True:
                rows = self.cursor.fetchmany(batch_size)
                if not rows:
                    break
                for row in rows:
                    row_dict = dict(zip(columns, row))
                    # Attempt to decode JSON strings
                    for k, v in row_dict.items():
                        if isinstance(v, str):
                            try:
                                # Only decode if it looks like a JSON object or array
                                if (v.startswith("{") and v.endswith("}")) or (v.startswith("[") and v.endswith("]")):
                                    row_dict[k] = json.loads(v)
                            except Exception:
                                pass
                    if not first:
                        file.write(",\n")
                    json.dump(row_dict, file, ensure_ascii=False, indent=4)
                    first = False
            file.write("\n]\n")
        logger.info(f"Data exported to JSON file: {file_path}")
    
    def export_to_txt(self, file_path: str, batch_size: int = 1000) -> None:
        """
        Exports the table's data to a text file, with large datasets handled in batches.
        The first line contains column headings.
    
        Args:
            file_path (str): Path to the text file.
            batch_size (int): Number of rows to fetch per batch. Defaults to 1000.
        """
        self.cursor.execute(f"SELECT * FROM {self.name}")
        columns = [description[0] for description in self.cursor.description]
        with open(file_path, mode="w", encoding="utf-8") as file:
            # Write column headings
            file.write("\t".join(columns) + "\n")
            while True:
                rows = self.cursor.fetchmany(batch_size)
                if not rows:
                    break
                for row in rows:
                    file.write("\t".join(str(value) for value in row) + "\n")
        logger.info(f"Data exported to text file: {file_path}")
    
    def enable_wal_mode(self) -> None:
        """
        Enables Write-Ahead Logging (WAL) mode for better concurrency.
        """
        self.cursor.execute("PRAGMA journal_mode=WAL;")
        self.connection.commit()
        logger.info("WAL mode enabled for the database.")
    
    def close(self) -> None:
        """Closes the database connection."""
        self.connection.close()
        logger.info(f"Connection to database closed.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()