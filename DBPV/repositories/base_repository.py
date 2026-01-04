"""
Base Repository Implementation for E-commerce Application
"""
import pyodbc
from abc import ABC
from typing import List, Optional, Any
from models.entities import Customer, Product, Order, OrderItem, Category, Supplier


class BaseRepository(ABC):
    """Base Repository with common database operations"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def _get_connection(self):
        """Create and return a database connection"""
        return pyodbc.connect(self.connection_string)
    
    def _execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """Execute a SELECT query and return results"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    
    def _execute_non_query(self, query: str, params: tuple = None) -> int:
        """Execute an INSERT, UPDATE, or DELETE query and return affected rows"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
    
    def _execute_scalar(self, query: str, params: tuple = None) -> Any:
        """Execute a query that returns a single value"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result else None