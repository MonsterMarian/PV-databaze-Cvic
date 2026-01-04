"""
Repository Pattern Implementation for E-commerce Application
This implements the Repository pattern (D1 requirement) with interfaces and concrete implementations
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any
import pyodbc


class IRepository(ABC):
    """Generic Repository Interface"""
    
    @abstractmethod
    def add(self, entity: Any) -> Any:
        pass
    
    @abstractmethod
    def update(self, entity: Any) -> Any:
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[Any]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Any]:
        pass


class ICustomerRepository(IRepository):
    """Customer Repository Interface"""
    
    @abstractmethod
    def get_customers_with_orders(self) -> List[Any]:
        pass
    
    @abstractmethod
    def get_customer_by_email(self, email: str) -> Optional[Any]:
        pass


class IProductRepository(IRepository):
    """Product Repository Interface"""
    
    @abstractmethod
    def get_products_by_category(self, category_id: int) -> List[Any]:
        pass
    
    @abstractmethod
    def get_products_in_stock(self) -> List[Any]:
        pass


class IOrderRepository(IRepository):
    """Order Repository Interface"""
    
    @abstractmethod
    def get_orders_by_customer(self, customer_id: int) -> List[Any]:
        pass
    
    @abstractmethod
    def get_orders_by_status(self, status: str) -> List[Any]:
        pass