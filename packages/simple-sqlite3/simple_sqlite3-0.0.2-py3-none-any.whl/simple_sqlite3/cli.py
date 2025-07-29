import json
import argparse
import sqlite3
import os
from simple_sqlite3.table import Table, validate_cli_identifier
from typing import Optional

def main():
    parser = argparse.ArgumentParser(description="Command-line interface for SQLite database manipulation.")

    subparsers = parser.add_subparsers(dest="action", required=True, help="Database actions")

    # Subparser for inserting data
    insert_parser = subparsers.add_parser("insert", help="Insert data into a table from a file")
    insert_parser.add_argument("-database", required=True, help="Path to the SQLite database")
    insert_parser.add_argument("-table", required=True, help="Name of the table")
    insert_parser.add_argument("-file", required=True, help="Input file path (.csv or .json)")

    # Subparser for querying records
    query_parser = subparsers.add_parser("query", help="Query records from a table")
    query_parser.add_argument("-database", required=True, help="Path to the SQLite database")
    query_parser.add_argument("-table", required=True, help="Name of the table")
    query_parser.add_argument("-sql", required=True, help="SQL query to execute")

    # Subparser for deleting a database or a table
    delete_parser = subparsers.add_parser("delete", help="Delete a database or a specific table")
    delete_parser.add_argument("-database", required=True, help="Path to the SQLite database")
    delete_parser.add_argument("-table", help="Name of the table to delete (optional)")

    # Subparser for renaming a column
    rename_column_parser = subparsers.add_parser("rename_column", help="Rename a column in a table")
    rename_column_parser.add_argument("-database", required=True, help="Path to the SQLite database")
    rename_column_parser.add_argument("-table", required=True, help="Name of the table")
    rename_column_parser.add_argument("old_name", help="Current name of the column")
    rename_column_parser.add_argument("new_name", help="New name for the column")

    # Subparser for deleting a column
    delete_column_parser = subparsers.add_parser("delete_column", help="Delete a column from a table")
    delete_column_parser.add_argument("-database", required=True, help="Path to the SQLite database")
    delete_column_parser.add_argument("-table", required=True, help="Name of the table")
    delete_column_parser.add_argument("column", help="Name of the column to delete")

    # Subparser for renaming a table
    rename_table_parser = subparsers.add_parser("rename_table", help="Rename a table")
    rename_table_parser.add_argument("-database", required=True, help="Path to the SQLite database")
    rename_table_parser.add_argument("-table", required=True, help="Name of the table")
    rename_table_parser.add_argument("new_name", help="New name for the table")

    # Subparser for dropping duplicates
    delet_duplicates_parser = subparsers.add_parser("delete_duplicates", help="Drop duplicate rows from a table")
    delet_duplicates_parser.add_argument("-database", required=True, help="Path to the SQLite database")
    delet_duplicates_parser.add_argument("-table", required=True, help="Name of the table")
    delet_duplicates_parser.add_argument("-by", nargs="+", help="Columns to check for duplicates (optional)")

    # Subparser for exporting data
    export_parser = subparsers.add_parser("export", help="Export table data to a file")
    export_parser.add_argument("-database", required=True, help="Path to the SQLite database")
    export_parser.add_argument("-table", required=True, help="Name of the table")
    export_parser.add_argument("-output", required=True, help="Output file path")

    args = parser.parse_args()

    if args.action == "query":
        query_records(args.database, args.table, args.sql)
    elif args.action == "delete":
        if args.table:
            delete_table(args.database, args.table)
        else:
            delete_database(args.database)
    elif args.action == "rename_column":
        rename_column(args.database, args.table, args.old_name, args.new_name)
    elif args.action == "delete_column":
        delete_column(args.database, args.table, args.column)
    elif args.action == "rename_table":
        rename_table(args.database, args.table, args.new_name)
    elif args.action == "delete_duplicates":
        delete_duplicates(args.database, args.table, args.by)
    elif args.action == "export":
        ext = os.path.splitext(args.output)[1].lower()
        if ext == ".csv":
            export_format = "csv"
        elif ext == ".json":
            export_format = "json"
        elif ext == ".txt":
            export_format = "txt"
        else:
            print("Could not detect format from file extension. Please use .csv, .json, or .txt.")
            return
        export_table(args.database, args.table, export_format, args.output)
    elif args.action == "insert":
        ext = os.path.splitext(args.file)[1].lower()
        if ext == ".csv":
            insert_format = "csv"
        elif ext == ".json":
            insert_format = "json"
        elif ext == ".txt":
            insert_format = "txt"
        else:
            print("Could not detect format from file extension. Please use .csv, .json, or .txt.")
            return
        insert_into_table(args.database, args.table, insert_format, args.file)
    else:
        parser.print_help()

def query_records(database_path: str, table_name: str, sql: str):
    try:
        table_name = validate_cli_identifier(table_name)
        with sqlite3.connect(database_path) as conn:
            table = Table(conn, table_name)
            results = table.query(sql)
            # Attempt to decode JSON strings in results
            for row in results:
                for k, v in row.items():
                    if isinstance(v, str):
                        try:
                            if (v.startswith("{") and v.endswith("}")) or (v.startswith("[") and v.endswith("]")):
                                row[k] = json.loads(v)
                        except Exception:
                            pass
            if results:
                formatted_results = json.dumps(results, indent=4, ensure_ascii=False)
                print(formatted_results)
            else:
                print("No results found.")
    except Exception as e:
        print(f"Error querying records: {e}")

def insert_into_table(database_path: str, table_name: str, insert_format: str, input_path: str):
    """
    Inserts data into a table from a file.
    Supports CSV, TXT (tab-delimited), and JSON formats.
    CSV and TXT formats are expected to have a header row and cannot contain nested data.
    JSON format is expected to be a list of dictionaries and can contain nested data.
    """
    table_name = validate_cli_identifier(table_name)
    with sqlite3.connect(database_path) as conn:
        table = Table(conn, table_name)
        records = None
        if insert_format == "csv":
            import csv
            with open(input_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                records = list(reader)
        elif insert_format == "txt":
            with open(input_path, 'r', encoding='utf-8') as file:
                # Tab-delimited, skip header
                lines = file.read().splitlines()
                if not lines:
                    print("TXT file is empty.")
                    return
                header = lines[0].split("\t")
                records = [dict(zip(header, row.split("\t"))) for row in lines[1:]]
        elif insert_format == "json":
            with open(input_path, 'r', encoding='utf-8') as file:
                records = json.load(file)
        else:
            print("Unsupported file format.")
            return

        if not records:
            print("No records to insert.")
            return

        # Check for nested data in non-JSON input
        if insert_format in ("csv", "txt"):
            for rec in records:
                for v in rec.values():
                    if isinstance(v, str) and (v.startswith("{") or v.startswith("[")):
                        print("Error: Nested data structures are only supported with JSON input.")
                        return

        table.insert(records)
        print(f"Data from '{input_path}' inserted into table '{table_name}'.")

def delete_database(database_path: str):
    if os.path.exists(database_path):
        os.remove(database_path)
        print(f"Database '{database_path}' deleted.")
    else:
        print(f"Database '{database_path}' does not exist.")

def delete_table(database_path: str, table_name: str):
    table_name = validate_cli_identifier(table_name)
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()
        print(f"Table '{table_name}' deleted from database.")

def rename_column(database_path: str, table_name: str, old_name: str, new_name: str):
    table_name = validate_cli_identifier(table_name)
    old_name = validate_cli_identifier(old_name)
    new_name = validate_cli_identifier(new_name)
    with sqlite3.connect(database_path) as conn:
        table = Table(conn, table_name)
        table.rename_column(old_name, new_name)
        print(f"Column '{old_name}' renamed to '{new_name}' in table '{table_name}'.")

def delete_column(database_path: str, table_name: str, column: str):
    table_name = validate_cli_identifier(table_name)
    column = validate_cli_identifier(column)
    with sqlite3.connect(database_path) as conn:
        table = Table(conn, table_name)
        table.drop_columns(column)
        print(f"Column '{column}' deleted from table '{table_name}'.")

def rename_table(database_path: str, table_name: str, new_name: str):
    table_name = validate_cli_identifier(table_name)
    new_name = validate_cli_identifier(new_name)
    with sqlite3.connect(database_path) as conn:
        table = Table(conn, table_name)
        table.rename(new_name)
        print(f"Table '{table_name}' renamed to '{new_name}'.")

def delete_duplicates(database_path: str, table_name: str, by: Optional[list[str]]):
    table_name = validate_cli_identifier(table_name)
    if by:
        by = [validate_cli_identifier(col) for col in by]
    with sqlite3.connect(database_path) as conn:
        table = Table(conn, table_name)
        table.delete_duplicates(by)
        print(f"Duplicates dropped from table '{table_name}' based on columns: {by}.")

def export_table(database_path: str, table_name: str, export_format: str, output_path: str):
    table_name = validate_cli_identifier(table_name)
    with sqlite3.connect(database_path) as conn:
        table = Table(conn, table_name)
        if export_format == "csv":
            table.export_to_csv(output_path)
        elif export_format == "json":
            table.export_to_json(output_path)
        elif export_format == "txt":
            table.export_to_txt(output_path)
        print(f"Table '{table_name}' exported to {export_format.upper()} at '{output_path}'.")

if __name__ == "__main__":
    main()