"""
Concrete Repository Implementations for E-commerce Application
"""
from typing import List, Optional
from repositories.interfaces import ICustomerRepository, IProductRepository, IOrderRepository
from repositories.base_repository import BaseRepository
from models.entities import Customer, Product, Order, OrderItem, Category, Supplier


class CustomerRepository(BaseRepository, ICustomerRepository):
    """Customer Repository Implementation"""
    
    def add(self, customer: Customer) -> Customer:
        query = """
        INSERT INTO Customers (FirstName, LastName, Email, DateOfBirth, IsActive, CreditLimit)
        VALUES (?, ?, ?, ?, ?, ?);
        SELECT SCOPE_IDENTITY();
        """
        params = (
            customer.first_name, customer.last_name, customer.email,
            customer.date_of_birth, customer.is_active, customer.credit_limit
        )
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            new_id = int(cursor.fetchone()[0])
            conn.commit()
            customer.customer_id = new_id
            return customer
    
    def update(self, customer: Customer) -> Customer:
        query = """
        UPDATE Customers
        SET FirstName = ?, LastName = ?, Email = ?, DateOfBirth = ?, IsActive = ?, CreditLimit = ?
        WHERE CustomerID = ?
        """
        params = (
            customer.first_name, customer.last_name, customer.email,
            customer.date_of_birth, customer.is_active, customer.credit_limit, customer.customer_id
        )
        self._execute_non_query(query, params)
        return customer
    
    def delete(self, customer_id: int) -> bool:
        query = "DELETE FROM Customers WHERE CustomerID = ?"
        rows_affected = self._execute_non_query(query, (customer_id,))
        return rows_affected > 0
    
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        query = "SELECT CustomerID, FirstName, LastName, Email, DateOfBirth, IsActive, RegistrationDate, CreditLimit FROM Customers WHERE CustomerID = ?"
        results = self._execute_query(query, (customer_id,))
        if results:
            row = results[0]
            return Customer(
                customer_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                date_of_birth=row[4],
                is_active=bool(row[5]),
                registration_date=row[6],
                credit_limit=row[7]
            )
        return None
    
    def get_all(self) -> List[Customer]:
        query = "SELECT CustomerID, FirstName, LastName, Email, DateOfBirth, IsActive, RegistrationDate, CreditLimit FROM Customers"
        results = self._execute_query(query)
        customers = []
        for row in results:
            customers.append(Customer(
                customer_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                date_of_birth=row[4],
                is_active=bool(row[5]),
                registration_date=row[6],
                credit_limit=row[7]
            ))
        return customers
    
    def get_customers_with_orders(self) -> List[Customer]:
        query = """
        SELECT DISTINCT c.CustomerID, c.FirstName, c.LastName, c.Email, 
               c.DateOfBirth, c.IsActive, c.RegistrationDate, c.CreditLimit
        FROM Customers c
        INNER JOIN Orders o ON c.CustomerID = o.CustomerID
        """
        results = self._execute_query(query)
        customers = []
        for row in results:
            customers.append(Customer(
                customer_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                date_of_birth=row[4],
                is_active=bool(row[5]),
                registration_date=row[6],
                credit_limit=row[7]
            ))
        return customers
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        query = "SELECT CustomerID, FirstName, LastName, Email, DateOfBirth, IsActive, RegistrationDate, CreditLimit FROM Customers WHERE Email = ?"
        results = self._execute_query(query, (email,))
        if results:
            row = results[0]
            return Customer(
                customer_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                date_of_birth=row[4],
                is_active=bool(row[5]),
                registration_date=row[6],
                credit_limit=row[7]
            )
        return None


class ProductRepository(BaseRepository, IProductRepository):
    """Product Repository Implementation"""
    
    def add(self, product: Product) -> Product:
        query = """
        INSERT INTO Products (ProductName, Description, Price, CategoryID, InStock, ProductStatus)
        VALUES (?, ?, ?, ?, ?, ?);
        SELECT SCOPE_IDENTITY();
        """
        params = (
            product.product_name, product.description, product.price,
            product.category_id, product.in_stock, product.product_status
        )
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            new_id = int(cursor.fetchone()[0])
            conn.commit()
            product.product_id = new_id
            return product
    
    def update(self, product: Product) -> Product:
        query = """
        UPDATE Products
        SET ProductName = ?, Description = ?, Price = ?, CategoryID = ?, InStock = ?, ProductStatus = ?
        WHERE ProductID = ?
        """
        params = (
            product.product_name, product.description, product.price,
            product.category_id, product.in_stock, product.product_status, product.product_id
        )
        self._execute_non_query(query, params)
        return product
    
    def delete(self, product_id: int) -> bool:
        query = "DELETE FROM Products WHERE ProductID = ?"
        rows_affected = self._execute_non_query(query, (product_id,))
        return rows_affected > 0
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        query = "SELECT ProductID, ProductName, Description, Price, CategoryID, InStock, CreatedDate, ProductStatus FROM Products WHERE ProductID = ?"
        results = self._execute_query(query, (product_id,))
        if results:
            row = results[0]
            return Product(
                product_id=row[0],
                product_name=row[1],
                description=row[2],
                price=row[3],
                category_id=row[4],
                in_stock=bool(row[5]),
                created_date=row[6],
                product_status=row[7]
            )
        return None
    
    def get_all(self) -> List[Product]:
        query = "SELECT ProductID, ProductName, Description, Price, CategoryID, InStock, CreatedDate, ProductStatus FROM Products"
        results = self._execute_query(query)
        products = []
        for row in results:
            products.append(Product(
                product_id=row[0],
                product_name=row[1],
                description=row[2],
                price=row[3],
                category_id=row[4],
                in_stock=bool(row[5]),
                created_date=row[6],
                product_status=row[7]
            ))
        return products
    
    def get_products_by_category(self, category_id: int) -> List[Product]:
        query = "SELECT ProductID, ProductName, Description, Price, CategoryID, InStock, CreatedDate, ProductStatus FROM Products WHERE CategoryID = ?"
        results = self._execute_query(query, (category_id,))
        products = []
        for row in results:
            products.append(Product(
                product_id=row[0],
                product_name=row[1],
                description=row[2],
                price=row[3],
                category_id=row[4],
                in_stock=bool(row[5]),
                created_date=row[6],
                product_status=row[7]
            ))
        return products
    
    def get_products_in_stock(self) -> List[Product]:
        query = "SELECT ProductID, ProductName, Description, Price, CategoryID, InStock, CreatedDate, ProductStatus FROM Products WHERE InStock = 1"
        results = self._execute_query(query)
        products = []
        for row in results:
            products.append(Product(
                product_id=row[0],
                product_name=row[1],
                description=row[2],
                price=row[3],
                category_id=row[4],
                in_stock=bool(row[5]),
                created_date=row[6],
                product_status=row[7]
            ))
        return products


class OrderRepository(BaseRepository, IOrderRepository):
    """Order Repository Implementation"""
    
    def add(self, order: Order) -> Order:
        query = """
        INSERT INTO Orders (CustomerID, TotalAmount, OrderStatus, IsPriority)
        VALUES (?, ?, ?, ?);
        SELECT SCOPE_IDENTITY();
        """
        params = (
            order.customer_id, order.total_amount,
            order.order_status, order.is_priority
        )
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            new_id = int(cursor.fetchone()[0])
            conn.commit()
            order.order_id = new_id
            return order
    
    def update(self, order: Order) -> Order:
        query = """
        UPDATE Orders
        SET CustomerID = ?, TotalAmount = ?, OrderStatus = ?, IsPriority = ?
        WHERE OrderID = ?
        """
        params = (
            order.customer_id, order.total_amount,
            order.order_status, order.is_priority, order.order_id
        )
        self._execute_non_query(query, params)
        return order
    
    def delete(self, order_id: int) -> bool:
        query = "DELETE FROM Orders WHERE OrderID = ?"
        rows_affected = self._execute_non_query(query, (order_id,))
        return rows_affected > 0
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        query = "SELECT OrderID, CustomerID, OrderDate, TotalAmount, OrderStatus, IsPriority FROM Orders WHERE OrderID = ?"
        results = self._execute_query(query, (order_id,))
        if results:
            row = results[0]
            return Order(
                order_id=row[0],
                customer_id=row[1],
                order_date=row[2],
                total_amount=row[3],
                order_status=row[4],
                is_priority=bool(row[5])
            )
        return None
    
    def get_all(self) -> List[Order]:
        query = "SELECT OrderID, CustomerID, OrderDate, TotalAmount, OrderStatus, IsPriority FROM Orders"
        results = self._execute_query(query)
        orders = []
        for row in results:
            orders.append(Order(
                order_id=row[0],
                customer_id=row[1],
                order_date=row[2],
                total_amount=row[3],
                order_status=row[4],
                is_priority=bool(row[5])
            ))
        return orders
    
    def get_orders_by_customer(self, customer_id: int) -> List[Order]:
        query = "SELECT OrderID, CustomerID, OrderDate, TotalAmount, OrderStatus, IsPriority FROM Orders WHERE CustomerID = ?"
        results = self._execute_query(query, (customer_id,))
        orders = []
        for row in results:
            orders.append(Order(
                order_id=row[0],
                customer_id=row[1],
                order_date=row[2],
                total_amount=row[3],
                order_status=row[4],
                is_priority=bool(row[5])
            ))
        return orders
    
    def get_orders_by_status(self, status: str) -> List[Order]:
        query = "SELECT OrderID, CustomerID, OrderDate, TotalAmount, OrderStatus, IsPriority FROM Orders WHERE OrderStatus = ?"
        results = self._execute_query(query, (status,))
        orders = []
        for row in results:
            orders.append(Order(
                order_id=row[0],
                customer_id=row[1],
                order_date=row[2],
                total_amount=row[3],
                order_status=row[4],
                is_priority=bool(row[5])
            ))
        return orders