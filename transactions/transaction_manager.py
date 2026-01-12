"""
Transaction Management for E-commerce Application
Implements transaction functionality across multiple tables as required by the assignment
"""
import pyodbc
from typing import Callable, Any, List
from config.config_manager import Config


class TransactionManager:
    """Manages database transactions across multiple operations"""
    
    def __init__(self, config: Config):
        self.connection_string = config.get_database_connection_string()
    
    def execute_in_transaction(self, operations: List[Callable], *args) -> Any:
        """
        Execute multiple operations within a single transaction
        If any operation fails, all changes are rolled back
        """
        connection = pyodbc.connect(self.connection_string)
        connection.autocommit = False  # Enable manual transaction control
        cursor = connection.cursor()
        
        try:
            results = []
            for operation in operations:
                result = operation(cursor, *args)
                results.append(result)
            
            # If all operations succeed, commit the transaction
            connection.commit()
            return results
            
        except Exception as e:
            # If any operation fails, rollback all changes
            connection.rollback()
            raise e
            
        finally:
            # Always close the connection
            connection.close()


class TransactionService:
    """Service class that provides transaction-based operations"""
    
    def __init__(self, config: Config):
        self.config = config
        self.transaction_manager = TransactionManager(config)
    
    def transfer_customer_credit(self, from_customer_id: int, to_customer_id: int, amount: float) -> bool:
        """
        Transfer credit between customers - requires transaction to ensure data consistency
        """
        def debit_source_customer(cursor, from_id, amt):
            # Check if source customer has enough credit
            cursor.execute(
                "SELECT CreditLimit FROM Customers WHERE CustomerID = ?", 
                (from_id,)
            )
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Customer with ID {from_id} does not exist")
            
            current_credit = result[0] or 0
            if current_credit < amt:
                raise ValueError(f"Insufficient credit. Available: {current_credit}, Requested: {amt}")
            
            # Debit the source customer
            cursor.execute(
                "UPDATE Customers SET CreditLimit = CreditLimit - ? WHERE CustomerID = ?",
                (amt, from_id)
            )
        
        def credit_target_customer(cursor, to_id, amt):
            # Credit the target customer
            cursor.execute(
                "UPDATE Customers SET CreditLimit = CreditLimit + ? WHERE CustomerID = ?",
                (amt, to_id)
            )
        
        def log_transaction(cursor, from_id, to_id, amt):
            # Log the transaction (if we had a transaction log table)
            # For this example, we'll just record it in a simple way
            cursor.execute(
                """INSERT INTO TransactionLog (FromCustomerID, ToCustomerID, Amount, TransactionDate) 
                   VALUES (?, ?, ?, GETDATE())""",
                (from_id, to_id, amt)
            )
        
        # Check if TransactionLog table exists, if not, create it
        self._ensure_transaction_log_table()
        
        # Execute all operations in a single transaction
        operations = [
            lambda cursor: debit_source_customer(cursor, from_customer_id, amount),
            lambda cursor: credit_target_customer(cursor, to_customer_id, amount),
            lambda cursor: log_transaction(cursor, from_customer_id, to_customer_id, amount)
        ]
        
        try:
            self.transaction_manager.execute_in_transaction(operations)
            return True
        except Exception as e:
            print(f"Transaction failed: {e}")
            return False
    
    def place_order_with_inventory_check(self, customer_id: int, order_items_data: List[dict]) -> int:
        """
        Place an order with inventory check - requires transaction to ensure consistency
        """
        def check_inventory_and_reserve(cursor, items_data):
            for item in items_data:
                product_id = item['product_id']
                quantity = item['quantity']
                
                # Check if product exists and has enough stock
                cursor.execute(
                    "SELECT InStock, Price FROM Products WHERE ProductID = ?", 
                    (product_id,)
                )
                result = cursor.fetchone()
                if not result:
                    raise ValueError(f"Product with ID {product_id} does not exist")
                
                in_stock, price = result
                if not in_stock:
                    raise ValueError(f"Product {product_id} is out of stock")
                
                # For a complete implementation, we would also check quantity in stock
                # Here we just ensure the product is available
        
        def create_order_record(cursor, cust_id, total_amt):
            # Create the order record
            cursor.execute(
                "INSERT INTO Orders (CustomerID, TotalAmount, OrderStatus) VALUES (?, ?, ?); SELECT SCOPE_IDENTITY();",
                (cust_id, total_amt, 'processing')
            )
            order_id = int(cursor.fetchone()[0])
            return order_id
        
        def create_order_items(cursor, order_id, items_data):
            total_amount = 0
            for item in items_data:
                product_id = item['product_id']
                quantity = item['quantity']
                
                # Get product price
                cursor.execute(
                    "SELECT Price FROM Products WHERE ProductID = ?", 
                    (product_id,)
                )
                price = cursor.fetchone()[0]
                
                item_total = price * quantity
                total_amount += item_total
                
                # Create order item
                cursor.execute(
                    "INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice) VALUES (?, ?, ?, ?)",
                    (order_id, product_id, quantity, price)
                )
            
            # Update the order with the correct total
            cursor.execute(
                "UPDATE Orders SET TotalAmount = ? WHERE OrderID = ?",
                (total_amount, order_id)
            )
            
            return total_amount
        
        def update_product_inventory(cursor, items_data):
            # In a real system, we would update inventory levels
            # For this example, we'll just mark products as reserved
            for item in items_data:
                product_id = item['product_id']
                quantity = item['quantity']
                
                # This would typically reduce the available quantity
                # For our schema, we'll just ensure the product remains in stock
                cursor.execute(
                    "UPDATE Products SET InStock = CASE WHEN (SELECT SUM(oi.Quantity) FROM OrderItems oi WHERE oi.ProductID = ? AND o.OrderStatus != 'cancelled') < 100 THEN 1 ELSE 0 END FROM Products p JOIN Orders o ON o.OrderID = (SELECT OrderID FROM OrderItems WHERE ProductID = ?) WHERE ProductID = ?",
                    (product_id, product_id, product_id)
                )
        
        # Execute all operations in a single transaction
        operations = [
            lambda cursor: check_inventory_and_reserve(cursor, order_items_data),
            lambda cursor: create_order_record(cursor, customer_id, 0),  # Total will be calculated in next step
            lambda cursor: create_order_items(cursor, 0, order_items_data)  # Order ID will be passed correctly
        ]
        
        # We need a slightly different approach since operations depend on each other
        connection = pyodbc.connect(self.config.get_database_connection_string())
        connection.autocommit = False
        cursor = connection.cursor()
        
        try:
            # Step 1: Check inventory
            check_inventory_and_reserve(cursor, order_items_data)
            
            # Step 2: Create order
            cursor.execute(
                "INSERT INTO Orders (CustomerID, TotalAmount, OrderStatus) VALUES (?, 0, ?); SELECT SCOPE_IDENTITY();",
                (customer_id, 'processing')
            )
            order_id = int(cursor.fetchone()[0])
            
            # Step 3: Create order items and calculate total
            total_amount = 0
            for item in order_items_data:
                product_id = item['product_id']
                quantity = item['quantity']
                
                # Get product price
                cursor.execute(
                    "SELECT Price FROM Products WHERE ProductID = ?", 
                    (product_id,)
                )
                price = cursor.fetchone()[0]
                
                item_total = price * quantity
                total_amount += item_total
                
                # Create order item
                cursor.execute(
                    "INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice) VALUES (?, ?, ?, ?)",
                    (order_id, product_id, quantity, price)
                )
            
            # Step 4: Update order total
            cursor.execute(
                "UPDATE Orders SET TotalAmount = ? WHERE OrderID = ?",
                (total_amount, order_id)
            )
            
            # Commit the transaction
            connection.commit()
            return order_id
            
        except Exception as e:
            connection.rollback()
            raise e
            
        finally:
            connection.close()
    
    def cancel_order_with_refund(self, order_id: int) -> bool:
        """
        Cancel an order and refund the customer - requires transaction for consistency
        """
        def get_order_details(cursor, oid):
            cursor.execute(
                "SELECT CustomerID, TotalAmount, OrderStatus FROM Orders WHERE OrderID = ?",
                (oid,)
            )
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Order with ID {oid} does not exist")
            
            customer_id, total_amount, order_status = result
            if order_status == 'cancelled':
                raise ValueError("Order is already cancelled")
            
            return customer_id, total_amount
        
        def update_order_status(cursor, oid):
            cursor.execute(
                "UPDATE Orders SET OrderStatus = 'cancelled' WHERE OrderID = ?",
                (order_id,)
            )
        
        def refund_customer_credit(cursor, cust_id, amt):
            cursor.execute(
                "UPDATE Customers SET CreditLimit = CreditLimit + ? WHERE CustomerID = ?",
                (amt, cust_id)
            )
        
        def update_inventory(cursor, oid):
            # In a real system, this would restore inventory
            # For our schema, we'll just mark products as available again
            cursor.execute(
                "SELECT ProductID, Quantity FROM OrderItems WHERE OrderID = ?",
                (oid,)
            )
            items = cursor.fetchall()
            
            for item in items:
                product_id, quantity = item
                # Update product as in stock
                cursor.execute(
                    "UPDATE Products SET InStock = 1 WHERE ProductID = ?",
                    (product_id,)
                )
        
        # Execute all operations in a single transaction
        connection = pyodbc.connect(self.config.get_database_connection_string())
        connection.autocommit = False
        cursor = connection.cursor()
        
        try:
            # Step 1: Get order details
            customer_id, total_amount = get_order_details(cursor, order_id)
            
            # Step 2: Update order status
            update_order_status(cursor, order_id)
            
            # Step 3: Refund customer
            refund_customer_credit(cursor, customer_id, total_amount)
            
            # Step 4: Update inventory
            update_inventory(cursor, order_id)
            
            # Commit the transaction
            connection.commit()
            return True
            
        except Exception as e:
            connection.rollback()
            print(f"Order cancellation failed: {e}")
            return False
            
        finally:
            connection.close()
    
    def _ensure_transaction_log_table(self):
        """
        Create TransactionLog table if it doesn't exist
        """
        connection = pyodbc.connect(self.config.get_database_connection_string())
        cursor = connection.cursor()
        
        try:
            # Check if table exists
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'TransactionLog')
                BEGIN
                    CREATE TABLE TransactionLog (
                        TransactionID INT IDENTITY(1,1) PRIMARY KEY,
                        FromCustomerID INT,
                        ToCustomerID INT,
                        Amount DECIMAL(10,2),
                        TransactionDate DATETIME2 DEFAULT GETDATE(),
                        FOREIGN KEY (FromCustomerID) REFERENCES Customers(CustomerID),
                        FOREIGN KEY (ToCustomerID) REFERENCES Customers(CustomerID)
                    )
                END
            """)
            connection.commit()
        except:
            # Table may already exist, which is fine
            pass
        finally:
            connection.close()