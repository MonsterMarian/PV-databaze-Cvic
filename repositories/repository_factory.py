"""
Repository Factory for E-commerce Application
"""
from repositories.concrete_repositories import CustomerRepository, ProductRepository, OrderRepository


class RepositoryFactory:
    """Factory class to create and manage repositories"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def create_customer_repository(self):
        return CustomerRepository(self.connection_string)
    
    def create_product_repository(self):
        return ProductRepository(self.connection_string)
    
    def create_order_repository(self):
        return OrderRepository(self.connection_string)