# filepath: simple_sqlite/__init__.py
from .database import Database
from .table import Table

# from .table import enable_debug_logging
# enable_debug_logging()

__all__ = ["Database", "Table"]