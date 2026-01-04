"""
Service Layer for Multi-Table Operations
Handles operations that span multiple tables as required by the assignment
"""
from typing import List, Optional
from models.entities import Customer, Product, Order, OrderItem
from repositories.repository_factory import RepositoryFactory
from config.config_manager import Config


class OrderService:
    """Service class for handling orders that span multiple tables"""
    
    def __init__(self, config: Config):
        self.config = config
        self.repository_factory = RepositoryFactory(config.get_database_connection_string())
        self.customer_repo = self.repository_factory.create_customer_repository()
        self.product_repo = self.repository_factory.create_product_repository()
        self.order_repo = self.repository_factory.create_order_repository()
    
    def create_order_with_items(self, customer_id: int, order_items_data: List[dict]) -> Optional[Order]:
        """
        Create an order with multiple items - spans Customers, Orders, and OrderItems tables
        """
        # Validate customer exists
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} does not exist")
        
        # Validate products and calculate total
        total_amount = 0
        for item_data in order_items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            
            product = self.product_repo.get_by_id(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} does not exist")
            
            if not product.in_stock:
                raise ValueError(f"Product {product.product_name} is out of stock")
            
            total_amount += product.price * quantity
        
        # Create the order
        order = Order(
            customer_id=customer_id,
            total_amount=total_amount,
            order_status='pending'
        )
        order = self.order_repo.add(order)
        
        # Create order items
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.order_id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=self.product_repo.get_by_id(item_data['product_id']).price
            )
            
            # Insert order item directly using a query since we don't have an OrderItem repository
            query = """
            INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)
            VALUES (?, ?, ?, ?)
            """
            from repositories.base_repository import BaseRepository
            base_repo = BaseRepository(self.config.get_database_connection_string())
            base_repo._execute_non_query(query, (
                order_item.order_id,
                order_item.product_id,
                order_item.quantity,
                order_item.unit_price
            ))
        
        # Update the order with the calculated total
        order.total_amount = total_amount
        order = self.order_repo.update(order)
        
        return order
    
    def get_order_with_details(self, order_id: int) -> dict:
        """
        Retrieve an order with its items and customer information - spans multiple tables
        """
        # Get order
        order = self.order_repo.get_by_id(order_id)
        if not order:
            return None
        
        # Get customer
        customer = self.customer_repo.get_by_id(order.customer_id)
        
        # Get order items
        query = """
        SELECT oi.OrderItemID, oi.OrderID, oi.ProductID, oi.Quantity, oi.UnitPrice,
               p.ProductName, p.Description
        FROM OrderItems oi
        JOIN Products p ON oi.ProductID = p.ProductID
        WHERE oi.OrderID = ?
        """
        from repositories.base_repository import BaseRepository
        base_repo = BaseRepository(self.config.get_database_connection_string())
        order_items_data = base_repo._execute_query(query, (order_id,))
        
        order_items = []
        for row in order_items_data:
            order_items.append({
                'order_item_id': row[0],
                'order_id': row[1],
                'product_id': row[2],
                'quantity': row[3],
                'unit_price': row[4],
                'product_name': row[5],
                'product_description': row[6]
            })
        
        return {
            'order': order,
            'customer': customer,
            'order_items': order_items
        }
    
    def update_order_status(self, order_id: int, new_status: str) -> bool:
        """
        Update order status - single table operation but part of multi-table workflow
        """
        order = self.order_repo.get_by_id(order_id)
        if not order:
            return False
        
        order.order_status = new_status
        updated_order = self.order_repo.update(order)
        return updated_order is not None
    
    def delete_order(self, order_id: int) -> bool:
        """
        Delete an order and its associated items - spans Orders and OrderItems tables
        """
        # First delete order items
        query = "DELETE FROM OrderItems WHERE OrderID = ?"
        from repositories.base_repository import BaseRepository
        base_repo = BaseRepository(self.config.get_database_connection_string())
        base_repo._execute_non_query(query, (order_id,))
        
        # Then delete the order
        return self.order_repo.delete(order_id)


class CustomerService:
    """Service class for handling customer operations that may span multiple tables"""
    
    def __init__(self, config: Config):
        self.config = config
        self.repository_factory = RepositoryFactory(config.get_database_connection_string())
        self.customer_repo = self.repository_factory.create_customer_repository()
        self.order_repo = self.repository_factory.create_order_repository()
    
    def create_customer_with_first_order(self, customer_data: dict, order_items_data: List[dict]) -> tuple:
        """
        Create a new customer and their first order - spans Customers, Orders, and OrderItems tables
        """
        # Create customer
        customer = Customer(
            first_name=customer_data['first_name'],
            last_name=customer_data['last_name'],
            email=customer_data['email'],
            date_of_birth=customer_data.get('date_of_birth'),
            credit_limit=customer_data.get('credit_limit', 0)
        )
        customer = self.customer_repo.add(customer)
        
        # Create order for the customer using OrderService
        order_service = OrderService(self.config)
        order = order_service.create_order_with_items(customer.customer_id, order_items_data)
        
        return customer, order
    
    def get_customer_with_orders(self, customer_id: int) -> dict:
        """
        Get customer with all their orders and order details - spans multiple tables
        """
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            return None
        
        orders = self.order_repo.get_orders_by_customer(customer_id)
        
        # For each order, get its details
        order_details = []
        order_service = OrderService(self.config)
        for order in orders:
            order_detail = order_service.get_order_with_details(order.order_id)
            if order_detail:
                order_details.append(order_detail)
        
        return {
            'customer': customer,
            'orders': order_details
        }
    
    def update_customer_and_associated_data(self, customer: Customer) -> Customer:
        """
        Update customer information - single table but may affect related operations
        """
        return self.customer_repo.update(customer)
    
    def delete_customer(self, customer_id: int) -> bool:
        """
        Delete customer and their associated orders - spans Customers and Orders tables
        """
        # First delete all orders for this customer (which also removes order items)
        orders = self.order_repo.get_orders_by_customer(customer_id)
        order_service = OrderService(self.config)
        
        for order in orders:
            order_service.delete_order(order.order_id)
        
        # Then delete the customer
        return self.customer_repo.delete(customer_id)


class ProductService:
    """Service class for handling product operations that may span multiple tables"""
    
    def __init__(self, config: Config):
        self.config = config
        self.repository_factory = RepositoryFactory(config.get_database_connection_string())
        self.product_repo = self.repository_factory.create_product_repository()
    
    def get_product_with_category_and_orders(self, product_id: int) -> dict:
        """
        Get product with its category and order information - spans Products, Categories, OrderItems, and Orders tables
        """
        product = self.product_repo.get_by_id(product_id)
        if not product:
            return None
        
        # Get category
        category_query = "SELECT CategoryID, CategoryName, Description FROM Categories WHERE CategoryID = ?"
        from repositories.base_repository import BaseRepository
        base_repo = BaseRepository(self.config.get_database_connection_string())
        category_data = base_repo._execute_query(category_query, (product.category_id,))
        
        category = None
        if category_data:
            cat_row = category_data[0]
            from models.entities import Category
            category = Category(
                category_id=cat_row[0],
                category_name=cat_row[1],
                description=cat_row[2]
            )
        
        # Get order information for this product
        order_query = """
        SELECT o.OrderID, o.OrderDate, o.TotalAmount, o.OrderStatus,
               c.FirstName, c.LastName, c.Email
        FROM OrderItems oi
        JOIN Orders o ON oi.OrderID = o.OrderID
        JOIN Customers c ON o.CustomerID = c.CustomerID
        WHERE oi.ProductID = ?
        """
        order_data = base_repo._execute_query(order_query, (product_id,))
        
        orders = []
        for row in order_data:
            from models.entities import Order, Customer
            order = Order(
                order_id=row[0],
                order_date=row[1],
                total_amount=row[2],
                order_status=row[3]
            )
            customer = Customer(
                first_name=row[4],
                last_name=row[5],
                email=row[6]
            )
            orders.append({
                'order': order,
                'customer': customer
            })
        
        return {
            'product': product,
            'category': category,
            'orders': orders
        }
    
    def update_product_and_related_data(self, product: Product) -> Product:
        """
        Update product information - single table but may affect related operations
        """
        return self.product_repo.update(product)
    
    def delete_product(self, product_id: int) -> bool:
        """
        Delete product and its associations - spans Products and related junction tables
        """
        # Remove from OrderItems where it appears (this would require setting orders to cancelled)
        # For this implementation, we'll assume we can only delete products that aren't in any orders
        query = "SELECT COUNT(*) FROM OrderItems WHERE ProductID = ?"
        from repositories.base_repository import BaseRepository
        base_repo = BaseRepository(self.config.get_database_connection_string())
        count = base_repo._execute_scalar(query, (product_id,))
        
        if count > 0:
            raise ValueError("Cannot delete product that is part of existing orders")
        
        # Delete from ProductSuppliers junction table
        delete_ps_query = "DELETE FROM ProductSuppliers WHERE ProductID = ?"
        base_repo._execute_non_query(delete_ps_query, (product_id,))
        
        # Then delete the product
        return self.product_repo.delete(product_id)