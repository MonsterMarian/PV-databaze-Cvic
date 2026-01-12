"""
Comprehensive Error Handling for E-commerce Application
Implements error handling for all operations as required by the assignment
"""
import logging
import functools
from typing import Any, Callable
from config.config_manager import Config


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)


class AppError(Exception):
    """Base application error class"""
    pass


class DatabaseConnectionError(AppError):
    """Raised when there's an issue connecting to the database"""
    pass


class ValidationError(AppError):
    """Raised when data validation fails"""
    pass


class ConfigurationError(AppError):
    """Raised when there's an issue with application configuration"""
    pass


class DataNotFoundError(AppError):
    """Raised when requested data is not found"""
    pass


class TransactionError(AppError):
    """Raised when a transaction fails"""
    pass


def handle_exceptions(error_map: dict = None):
    """
    Decorator for handling exceptions in a consistent way
    """
    if error_map is None:
        error_map = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log the error
                logging.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                
                # Map specific exceptions if needed
                for exc_type, mapped_error in error_map.items():
                    if isinstance(e, exc_type):
                        raise mapped_error(str(e)) from e
                
                # Re-raise the original exception if not mapped
                raise e
        return wrapper
    return decorator


class ErrorHandler:
    """Centralized error handling service"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def handle_database_error(self, error: Exception, operation: str = "database operation"):
        """Handle database-related errors"""
        self.logger.error(f"Database error during {operation}: {str(error)}")
        
        # Different handling based on error type
        if "timeout" in str(error).lower():
            raise DatabaseConnectionError(f"Database connection timeout during {operation}")
        elif "access denied" in str(error).lower() or "login failed" in str(error).lower():
            raise DatabaseConnectionError(f"Database authentication failed during {operation}")
        elif "does not exist" in str(error).lower() or "invalid object name" in str(error).lower():
            raise DatabaseConnectionError(f"Database object does not exist during {operation}")
        else:
            raise DatabaseConnectionError(f"Database error during {operation}: {str(error)}")
    
    def handle_validation_error(self, error: Exception, field: str = "unknown field"):
        """Handle data validation errors"""
        self.logger.warning(f"Validation error for {field}: {str(error)}")
        raise ValidationError(f"Validation failed for {field}: {str(error)}")
    
    def handle_config_error(self, error: Exception, config_key: str = "unknown config"):
        """Handle configuration errors"""
        self.logger.error(f"Configuration error for {config_key}: {str(error)}")
        raise ConfigurationError(f"Configuration error for {config_key}: {str(error)}")
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        if not email:
            raise ValidationError("Email is required")
        
        # Simple email validation
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValidationError(f"Invalid email format: {email}")
        
        return True
    
    def validate_customer_data(self, customer_data: dict) -> None:
        """Validate customer data"""
        required_fields = ['first_name', 'last_name', 'email']
        
        for field in required_fields:
            if field not in customer_data or not customer_data[field]:
                raise ValidationError(f"Required field '{field}' is missing or empty")
        
        # Validate email format
        self.validate_email(customer_data['email'])
        
        # Validate optional fields
        if 'credit_limit' in customer_data:
            try:
                credit_limit = float(customer_data['credit_limit'])
                if credit_limit < 0:
                    raise ValidationError("Credit limit cannot be negative")
            except (ValueError, TypeError):
                raise ValidationError("Credit limit must be a valid number")
    
    def validate_product_data(self, product_data: dict) -> None:
        """Validate product data"""
        required_fields = ['product_name', 'price']
        
        for field in required_fields:
            if field not in product_data or not product_data[field]:
                raise ValidationError(f"Required field '{field}' is missing or empty")
        
        # Validate price
        try:
            price = float(product_data['price'])
            if price < 0:
                raise ValidationError("Price cannot be negative")
        except (ValueError, TypeError):
            raise ValidationError("Price must be a valid number")
    
    def validate_order_data(self, order_data: dict) -> None:
        """Validate order data"""
        required_fields = ['customer_id', 'order_items']
        
        for field in required_fields:
            if field not in order_data or not order_data[field]:
                raise ValidationError(f"Required field '{field}' is missing or empty")
        
        # Validate customer_id
        try:
            customer_id = int(order_data['customer_id'])
            if customer_id <= 0:
                raise ValidationError("Customer ID must be a positive integer")
        except (ValueError, TypeError):
            raise ValidationError("Customer ID must be a valid integer")
        
        # Validate order items
        order_items = order_data['order_items']
        if not isinstance(order_items, list) or len(order_items) == 0:
            raise ValidationError("Order items must be a non-empty list")
        
        for i, item in enumerate(order_items):
            if not isinstance(item, dict):
                raise ValidationError(f"Order item at index {i} must be a dictionary")
            
            if 'product_id' not in item or 'quantity' not in item:
                raise ValidationError(f"Order item at index {i} must have 'product_id' and 'quantity'")
            
            try:
                product_id = int(item['product_id'])
                quantity = int(item['quantity'])
                
                if product_id <= 0:
                    raise ValidationError(f"Product ID at index {i} must be a positive integer")
                if quantity <= 0:
                    raise ValidationError(f"Quantity at index {i} must be a positive integer")
            except (ValueError, TypeError):
                raise ValidationError(f"Product ID and quantity at index {i} must be valid integers")
    
    def log_error(self, error: Exception, context: str = "general"):
        """Log error with context"""
        self.logger.error(f"[{context}] Error: {str(error)}", exc_info=True)
    
    def safe_execute(self, operation: Callable, *args, error_context: str = "operation", **kwargs):
        """Safely execute an operation with error handling"""
        try:
            return operation(*args, **kwargs)
        except ValidationError as e:
            self.log_error(e, f"validation_{error_context}")
            raise
        except DatabaseConnectionError as e:
            self.log_error(e, f"database_{error_context}")
            raise
        except ConfigurationError as e:
            self.log_error(e, f"config_{error_context}")
            raise
        except Exception as e:
            self.log_error(e, error_context)
            raise AppError(f"Unexpected error during {error_context}: {str(e)}") from e


# Example usage of error handling in repositories
class SafeCustomerRepository:
    """Customer Repository with comprehensive error handling"""
    
    def __init__(self, connection_string: str, error_handler: ErrorHandler):
        from repositories.base_repository import BaseRepository
        self.base_repo = BaseRepository(connection_string)
        self.error_handler = error_handler
    
    @handle_exceptions({
        Exception: lambda e: DatabaseConnectionError(f"Failed to connect to database: {str(e)}")
    })
    def get_by_id(self, customer_id: int):
        try:
            # Validate input
            if not isinstance(customer_id, int) or customer_id <= 0:
                raise ValidationError("Customer ID must be a positive integer")
            
            query = "SELECT CustomerID, FirstName, LastName, Email, DateOfBirth, IsActive, RegistrationDate, CreditLimit FROM Customers WHERE CustomerID = ?"
            results = self.base_repo._execute_query(query, (customer_id,))
            
            if not results:
                raise DataNotFoundError(f"Customer with ID {customer_id} not found")
            
            row = results[0]
            from models.entities import Customer
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
        except Exception as e:
            self.error_handler.handle_database_error(e, f"getting customer by ID {customer_id}")
    
    @handle_exceptions({
        Exception: lambda e: DatabaseConnectionError(f"Failed to add customer: {str(e)}")
    })
    def add(self, customer):
        try:
            # Validate customer data
            customer_data = {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email
            }
            self.error_handler.validate_customer_data(customer_data)
            
            query = """
            INSERT INTO Customers (FirstName, LastName, Email, DateOfBirth, IsActive, CreditLimit)
            VALUES (?, ?, ?, ?, ?, ?);
            SELECT SCOPE_IDENTITY();
            """
            params = (
                customer.first_name, customer.last_name, customer.email,
                customer.date_of_birth, customer.is_active, customer.credit_limit
            )
            
            with self.base_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                new_id = int(cursor.fetchone()[0])
                conn.commit()
                customer.customer_id = new_id
                return customer
        except Exception as e:
            self.error_handler.handle_database_error(e, "adding customer")