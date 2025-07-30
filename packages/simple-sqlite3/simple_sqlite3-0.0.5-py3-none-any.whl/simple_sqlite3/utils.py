from datetime import datetime
from collections import defaultdict
import csv
import json

class QueryResultsProcessor:
    """
    Processes query results and provides various data transformation utilities.

    This class is designed to handle query results represented as a list of dictionaries
    and provides methods to transform the data into different formats, such as matrix or grouped formats.
    It also includes utilities for converting datetime columns to and from string representations.
    """

    def __init__(self, results):
        """
        Initializes the QueryResultsProcessor.

        Args:
            results (list[dict]): A list of dictionaries representing query results.
        """
        self.results = results

    def infer_format_and_column(self, pivoted_data):
        """
        Infers the input format and datetime column from the pivoted data.

        Args:
            pivoted_data (dict): The pivoted data.

        Returns:
            tuple: A tuple containing the input format ("matrix" or "grouped") and the datetime column.

        Raises:
            ValueError: If the input format or datetime column cannot be inferred.
        """
        if "values" in pivoted_data and "index" in pivoted_data:
            return "matrix", "index"
        elif "index" in pivoted_data:
            return "grouped", "index"
        else:
            raise ValueError("Unable to infer input format or datetime column.")

    def to_matrix_format(self, index_key, group_key, value_key, transpose=False):
        """
        Converts the list of dictionaries into a matrix-like format.

        Args:
            index_key (str): The key to use as the index (e.g., "date").
            group_key (str): The key to use as the columns (e.g., "id").
            value_key (str): The key to use as the values (e.g., "x").
            transpose (bool): Whether to transpose the values (rows become columns and vice versa).

        Returns:
            dict: A dictionary with keys: "index", "columns", and "values".
        """
        grouped_data = defaultdict(lambda: defaultdict(lambda: None))
        unique_indices = set()
        unique_columns = set()

        for row in self.results:
            index = row[index_key]
            column = row[group_key]
            value = row[value_key]
            grouped_data[index][column] = value
            unique_indices.add(index)
            unique_columns.add(column)

        sorted_indices = sorted(unique_indices)
        sorted_columns = sorted(unique_columns)

        values = [
            [grouped_data[index].get(column, None) for column in sorted_columns]
            for index in sorted_indices
        ]

        if transpose:
            values = list(map(list, zip(*values)))

        return {
            "index": sorted_indices,
            "columns": sorted_columns,
            "values": values,
        }

    def to_grouped_format(self, index_key, group_key, value_key, transpose=False):
        """
        Converts the list of dictionaries into a grouped format.

        Args:
            index_key (str): The key to use as the index (e.g., "date").
            group_key (str): The key to use as the groups (e.g., "id").
            value_key (str): The key to use as the values (e.g., "x").
            transpose (bool): Whether to transpose the values (rows become columns and vice versa).

        Returns:
            dict: A dictionary with keys: "index" and one key for each group.
        """
        grouped_data = defaultdict(lambda: [])
        unique_indices = set()

        for row in self.results:
            index = row[index_key]
            group = row[group_key]
            value = row[value_key]
            grouped_data[group].append((index, value))
            unique_indices.add(index)

        sorted_indices = sorted(unique_indices)
        grouped_result = {"index": sorted_indices}

        for group, values in grouped_data.items():
            group_values = {index: value for index, value in values}
            grouped_result[group] = [
                group_values.get(index, None) for index in sorted_indices
            ]

        if transpose:
            transposed_values = list(map(list, zip(*[grouped_result[group] for group in grouped_result if group != "index"])))
            grouped_result = {"index": sorted_indices}
            for i, group in enumerate(grouped_result.keys() - {"index"}):
                grouped_result[group] = transposed_values[i]

        return grouped_result

    def to_datetime(self, pivoted_data=None, column=None, input_format=None):
        """
        Converts specified column(s) to datetime objects.

        Args:
            pivoted_data (dict, optional): The pivoted data (either in "matrix" or "grouped" format). Defaults to None.
            column (str, optional): The column to convert. Defaults to None.
            input_format (str, optional): The format of the pivoted data ("matrix" or "grouped"). Defaults to None.

        Returns:
            dict: The pivoted data with the specified column(s) converted to datetime.

        Raises:
            ValueError: If the input format is invalid.
        """
        if pivoted_data is None:
            pivoted_data = self.results
        if input_format is None or column is None:
            input_format, column = self.infer_format_and_column(pivoted_data)

        if input_format == "matrix":
            pivoted_data[column] = [datetime.fromisoformat(value) for value in pivoted_data[column]]
        elif input_format == "grouped":
            pivoted_data[column] = [datetime.fromisoformat(value) for value in pivoted_data[column]]
        else:
            raise ValueError("Invalid input_format. Use 'matrix' or 'grouped'.")
        return pivoted_data

    def revert_datetime(self, pivoted_data=None, column=None, input_format=None):
        """
        Converts datetime objects back to strings in YYYY-MM-DD HH:MM:SS format.

        Args:
            pivoted_data (dict, optional): The pivoted data (either in "matrix" or "grouped" format). Defaults to None.
            column (str, optional): The column to convert. Defaults to None.
            input_format (str, optional): The format of the pivoted data ("matrix" or "grouped"). Defaults to None.

        Returns:
            dict: The pivoted data with the specified column(s) converted back to strings.

        Raises:
            ValueError: If the input format is invalid.
        """
        if pivoted_data is None:
            pivoted_data = self.results
        if input_format is None or column is None:
            input_format, column = self.infer_format_and_column(pivoted_data)

        if input_format == "matrix":
            pivoted_data[column] = [value.isoformat(sep=" ") for value in pivoted_data[column]]
        elif input_format == "grouped":
            pivoted_data[column] = [value.isoformat(sep=" ") for value in pivoted_data[column]]
        else:
            raise ValueError("Invalid input_format. Use 'matrix' or 'grouped'.")
        return pivoted_data
    
    def to_csv(self, file_path: str) -> None:
        """
        Exports the query results to a CSV file.

        Args:
            file_path (str): Path to the CSV file.
        """
        if not self.results:
            return
        columns = list(self.results[0].keys())
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(self.results)

    def to_json(self, file_path: str) -> None:
        """
        Exports the query results to a JSON file.

        Args:
            file_path (str): Path to the JSON file.
        """
        with open(file_path, mode="w", encoding="utf-8") as file:
            json.dump(self.results, file, ensure_ascii=False, indent=4)

    def to_txt(self, file_path: str) -> None:
        """
        Exports the query results to a text file (tab-separated).

        Args:
            file_path (str): Path to the text file.
        """
        if not self.results:
            return
        columns = list(self.results[0].keys())
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write("\t".join(columns) + "\n")
            for row in self.results:
                file.write("\t".join(str(row.get(col, "")) for col in columns) + "\n")