class SimpleSQLiteError(Exception):
    """Base class for all exceptions in the simple_sqlite package."""
    pass


class TableNotFoundError(SimpleSQLiteError):
    """Raised when a table does not exist in the database."""
    pass


class InvalidDataError(SimpleSQLiteError):
    """Raised when invalid data is provided for an operation."""
    pass


class SchemaMismatchError(SimpleSQLiteError):
    """Raised when there is a mismatch in the table schema."""
    pass