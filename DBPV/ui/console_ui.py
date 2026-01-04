"""
Console User Interface for E-commerce Application
Provides a user-friendly interface for interacting with the application
"""
import os
import sys
from typing import List
from config.config_manager import Config
from repositories.repository_factory import RepositoryFactory
from services.multi_table_services import CustomerService, OrderService, ProductService
from transactions.transaction_manager import TransactionService
from reports.report_service import ReportService
from data_import.data_import_service import DataImportService
from error_handling.error_handler import ErrorHandler


class ConsoleUI:
    """Main console user interface for the e-commerce application"""
    
    def __init__(self):
        self.config = Config()
        self.error_handler = ErrorHandler(self.config)
        self.repository_factory = RepositoryFactory(self.config.get_database_connection_string())
        
        # Initialize services
        self.customer_service = CustomerService(self.config)
        self.order_service = OrderService(self.config)
        self.product_service = ProductService(self.config)
        self.transaction_service = TransactionService(self.config)
        self.report_service = ReportService(self.config)
        self.import_service = DataImportService(self.config)
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("E-COMMERCE APPLICATION")
        print("="*50)
        print("1. Customer Management")
        print("2. Product Management") 
        print("3. Order Management")
        print("4. Transactions")
        print("5. Reports")
        print("6. Data Import")
        print("7. Configuration")
        print("0. Exit")
        print("-"*50)
    
    def customer_menu(self):
        """Display customer management menu"""
        while True:
            print("\n--- CUSTOMER MANAGEMENT ---")
            print("1. List all customers")
            print("2. View customer details")
            print("3. Add new customer")
            print("4. Update customer")
            print("5. Delete customer")
            print("6. View customer orders")
            print("0. Back to main menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.list_customers()
            elif choice == '2':
                self.view_customer_details()
            elif choice == '3':
                self.add_customer()
            elif choice == '4':
                self.update_customer()
            elif choice == '5':
                self.delete_customer()
            elif choice == '6':
                self.view_customer_orders()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def product_menu(self):
        """Display product management menu"""
        while True:
            print("\n--- PRODUCT MANAGEMENT ---")
            print("1. List all products")
            print("2. View product details")
            print("3. Add new product")
            print("4. Update product")
            print("5. Delete product")
            print("6. Products by category")
            print("7. Products in stock")
            print("0. Back to main menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.list_products()
            elif choice == '2':
                self.view_product_details()
            elif choice == '3':
                self.add_product()
            elif choice == '4':
                self.update_product()
            elif choice == '5':
                self.delete_product()
            elif choice == '6':
                self.products_by_category()
            elif choice == '7':
                self.products_in_stock()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def order_menu(self):
        """Display order management menu"""
        while True:
            print("\n--- ORDER MANAGEMENT ---")
            print("1. List all orders")
            print("2. View order details")
            print("3. Create new order")
            print("4. Update order status")
            print("5. Cancel order")
            print("0. Back to main menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.list_orders()
            elif choice == '2':
                self.view_order_details()
            elif choice == '3':
                self.create_order()
            elif choice == '4':
                self.update_order_status()
            elif choice == '5':
                self.cancel_order()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def transaction_menu(self):
        """Display transaction menu"""
        while True:
            print("\n--- TRANSACTIONS ---")
            print("1. Transfer credit between customers")
            print("2. Place order with inventory check")
            print("3. Cancel order with refund")
            print("0. Back to main menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.transfer_credit()
            elif choice == '2':
                self.place_order_with_check()
            elif choice == '3':
                self.cancel_order_with_refund()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def report_menu(self):
        """Display report menu"""
        while True:
            print("\n--- REPORTS ---")
            print("1. Sales Summary Report")
            print("2. Top Products Report")
            print("3. Customer Order Report")
            print("4. Inventory Report")
            print("5. Monthly Sales Report")
            print("6. Category Performance Report")
            print("0. Back to main menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.sales_summary_report()
            elif choice == '2':
                self.top_products_report()
            elif choice == '3':
                self.customer_order_report()
            elif choice == '4':
                self.inventory_report()
            elif choice == '5':
                self.monthly_sales_report()
            elif choice == '6':
                self.category_performance_report()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def import_menu(self):
        """Display import menu"""
        while True:
            print("\n--- DATA IMPORT ---")
            print("1. Import customers from CSV")
            print("2. Import products from CSV")
            print("3. Import customers from JSON")
            print("4. Import products from JSON")
            print("0. Back to main menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.import_customers_csv()
            elif choice == '2':
                self.import_products_csv()
            elif choice == '3':
                self.import_customers_json()
            elif choice == '4':
                self.import_products_json()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def config_menu(self):
        """Display configuration menu"""
        while True:
            print("\n--- CONFIGURATION ---")
            print(f"Current server: {self.config.get('database.server')}")
            print(f"Current database: {self.config.get('database.database')}")
            print("1. View all configuration")
            print("2. Update database server")
            print("3. Update database name")
            print("4. Update username")
            print("5. Update password")
            print("0. Back to main menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.view_config()
            elif choice == '2':
                self.update_db_server()
            elif choice == '3':
                self.update_db_name()
            elif choice == '4':
                self.update_username()
            elif choice == '5':
                self.update_password()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def list_customers(self):
        """List all customers"""
        try:
            customers = self.customer_service.customer_repo.get_all()
            if not customers:
                print("No customers found.")
                return
            
            print(f"\n{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<25} {'Credit Limit':<15}")
            print("-" * 80)
            for customer in customers:
                print(f"{customer.customer_id:<5} {customer.first_name:<15} {customer.last_name:<15} {customer.email:<25} {customer.credit_limit:<15.2f}")
        except Exception as e:
            self.error_handler.log_error(e, "list_customers")
            print(f"Error listing customers: {e}")
    
    def view_customer_details(self):
        """View details of a specific customer"""
        try:
            customer_id = int(input("Enter customer ID: "))
            customer = self.customer_service.customer_repo.get_by_id(customer_id)
            
            if not customer:
                print(f"Customer with ID {customer_id} not found.")
                return
            
            print(f"\nCustomer Details:")
            print(f"ID: {customer.customer_id}")
            print(f"Name: {customer.first_name} {customer.last_name}")
            print(f"Email: {customer.email}")
            print(f"Date of Birth: {customer.date_of_birth}")
            print(f"Active: {customer.is_active}")
            print(f"Registration Date: {customer.registration_date}")
            print(f"Credit Limit: {customer.credit_limit}")
        except ValueError:
            print("Invalid customer ID. Please enter a number.")
        except Exception as e:
            self.error_handler.log_error(e, "view_customer_details")
            print(f"Error viewing customer details: {e}")
    
    def add_customer(self):
        """Add a new customer"""
        try:
            first_name = input("Enter first name: ").strip()
            last_name = input("Enter last name: ").strip()
            email = input("Enter email: ").strip()
            date_of_birth = input("Enter date of birth (YYYY-MM-DD, optional): ").strip() or None
            credit_limit_input = input("Enter credit limit (optional, default 0): ").strip()
            credit_limit = float(credit_limit_input) if credit_limit_input else 0.0
            
            from models.entities import Customer
            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                date_of_birth=date_of_birth,
                credit_limit=credit_limit
            )
            
            # Validate customer data
            customer_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'credit_limit': credit_limit
            }
            self.error_handler.validate_customer_data(customer_data)
            
            saved_customer = self.customer_service.customer_repo.add(customer)
            print(f"Customer {saved_customer.first_name} {saved_customer.last_name} added successfully with ID {saved_customer.customer_id}")
        except Exception as e:
            self.error_handler.log_error(e, "add_customer")
            print(f"Error adding customer: {e}")
    
    def update_customer(self):
        """Update an existing customer"""
        try:
            customer_id = int(input("Enter customer ID to update: "))
            customer = self.customer_service.customer_repo.get_by_id(customer_id)
            
            if not customer:
                print(f"Customer with ID {customer_id} not found.")
                return
            
            print(f"Updating customer: {customer.first_name} {customer.last_name}")
            first_name = input(f"Enter first name (current: {customer.first_name}, press Enter to keep): ").strip()
            last_name = input(f"Enter last name (current: {customer.last_name}, press Enter to keep): ").strip()
            email = input(f"Enter email (current: {customer.email}, press Enter to keep): ").strip()
            date_of_birth = input(f"Enter date of birth (current: {customer.date_of_birth}, press Enter to keep): ").strip()
            credit_limit_input = input(f"Enter credit limit (current: {customer.credit_limit}, press Enter to keep): ").strip()
            
            if first_name:
                customer.first_name = first_name
            if last_name:
                customer.last_name = last_name
            if email:
                customer.email = email
            if date_of_birth:
                customer.date_of_birth = date_of_birth
            if credit_limit_input:
                customer.credit_limit = float(credit_limit_input)
            
            # Validate updated customer data
            customer_data = {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'credit_limit': customer.credit_limit
            }
            self.error_handler.validate_customer_data(customer_data)
            
            updated_customer = self.customer_service.customer_repo.update(customer)
            print(f"Customer updated successfully.")
        except ValueError:
            print("Invalid input. Please enter valid values.")
        except Exception as e:
            self.error_handler.log_error(e, "update_customer")
            print(f"Error updating customer: {e}")
    
    def delete_customer(self):
        """Delete a customer"""
        try:
            customer_id = int(input("Enter customer ID to delete: "))
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete customer with ID {customer_id}? (y/N): ").lower()
            if confirm != 'y':
                print("Deletion cancelled.")
                return
            
            success = self.customer_service.delete_customer(customer_id)
            if success:
                print(f"Customer with ID {customer_id} deleted successfully.")
            else:
                print(f"Failed to delete customer with ID {customer_id}.")
        except ValueError:
            print("Invalid customer ID. Please enter a number.")
        except Exception as e:
            self.error_handler.log_error(e, "delete_customer")
            print(f"Error deleting customer: {e}")
    
    def view_customer_orders(self):
        """View orders for a specific customer"""
        try:
            customer_id = int(input("Enter customer ID: "))
            result = self.customer_service.get_customer_with_orders(customer_id)
            
            if not result:
                print(f"Customer with ID {customer_id} not found.")
                return
            
            customer = result['customer']
            orders = result['orders']
            
            print(f"\nOrders for {customer.first_name} {customer.last_name}:")
            if not orders:
                print("No orders found for this customer.")
                return
            
            for order_detail in orders:
                order = order_detail['order']
                print(f"\nOrder ID: {order.order_id}")
                print(f"Order Date: {order.order_date}")
                print(f"Total Amount: {order.total_amount}")
                print(f"Status: {order.order_status}")
                
                print("Items:")
                for item in order_detail['order_items']:
                    print(f"  - {item['product_name']}: {item['quantity']} x {item['unit_price']} = {item['quantity'] * item['unit_price']}")
        except ValueError:
            print("Invalid customer ID. Please enter a number.")
        except Exception as e:
            self.error_handler.log_error(e, "view_customer_orders")
            print(f"Error viewing customer orders: {e}")
    
    def list_products(self):
        """List all products"""
        try:
            products = self.product_service.product_repo.get_all()
            if not products:
                print("No products found.")
                return
            
            print(f"\n{'ID':<5} {'Product Name':<30} {'Price':<10} {'In Stock':<10} {'Status':<15}")
            print("-" * 75)
            for product in products:
                stock_status = "Yes" if product.in_stock else "No"
                print(f"{product.product_id:<5} {product.product_name:<30} {product.price:<10.2f} {stock_status:<10} {product.product_status:<15}")
        except Exception as e:
            self.error_handler.log_error(e, "list_products")
            print(f"Error listing products: {e}")
    
    def view_product_details(self):
        """View details of a specific product"""
        try:
            product_id = int(input("Enter product ID: "))
            result = self.product_service.get_product_with_category_and_orders(product_id)
            
            if not result:
                print(f"Product with ID {product_id} not found.")
                return
            
            product = result['product']
            category = result['category']
            
            print(f"\nProduct Details:")
            print(f"ID: {product.product_id}")
            print(f"Name: {product.product_name}")
            print(f"Description: {product.description}")
            print(f"Price: {product.price}")
            print(f"In Stock: {product.in_stock}")
            print(f"Status: {product.product_status}")
            print(f"Created Date: {product.created_date}")
            
            if category:
                print(f"Category: {category.category_name}")
            
            orders = result['orders']
            if orders:
                print(f"\nOrdered {len(orders)} times by different customers")
        except ValueError:
            print("Invalid product ID. Please enter a number.")
        except Exception as e:
            self.error_handler.log_error(e, "view_product_details")
            print(f"Error viewing product details: {e}")
    
    def add_product(self):
        """Add a new product"""
        try:
            product_name = input("Enter product name: ").strip()
            description = input("Enter product description: ").strip()
            price = float(input("Enter product price: "))
            category_id = int(input("Enter category ID: "))
            in_stock_input = input("In stock? (y/N, default y): ").strip().lower()
            in_stock = in_stock_input != 'n'
            product_status = input("Enter product status (default 'active'): ").strip() or 'active'
            
            from models.entities import Product
            product = Product(
                product_name=product_name,
                description=description,
                price=price,
                category_id=category_id,
                in_stock=in_stock,
                product_status=product_status
            )
            
            # Validate product data
            product_data = {
                'product_name': product_name,
                'price': price
            }
            self.error_handler.validate_product_data(product_data)
            
            saved_product = self.product_service.product_repo.add(product)
            print(f"Product '{saved_product.product_name}' added successfully with ID {saved_product.product_id}")
        except ValueError:
            print("Invalid input. Please enter valid values.")
        except Exception as e:
            self.error_handler.log_error(e, "add_product")
            print(f"Error adding product: {e}")
    
    def update_product(self):
        """Update an existing product"""
        try:
            product_id = int(input("Enter product ID to update: "))
            product = self.product_service.product_repo.get_by_id(product_id)
            
            if not product:
                print(f"Product with ID {product_id} not found.")
                return
            
            print(f"Updating product: {product.product_name}")
            product_name = input(f"Enter product name (current: {product.product_name}, press Enter to keep): ").strip()
            description = input(f"Enter description (current: {product.description}, press Enter to keep): ").strip()
            price_input = input(f"Enter price (current: {product.price}, press Enter to keep): ").strip()
            category_id_input = input(f"Enter category ID (current: {product.category_id}, press Enter to keep): ").strip()
            in_stock_input = input(f"In stock? (current: {product.in_stock}, y/N, press Enter to keep): ").strip().lower()
            product_status = input(f"Enter status (current: {product.product_status}, press Enter to keep): ").strip()
            
            if product_name:
                product.product_name = product_name
            if description:
                product.description = description
            if price_input:
                product.price = float(price_input)
            if category_id_input:
                product.category_id = int(category_id_input)
            if in_stock_input:
                product.in_stock = in_stock_input != 'n'
            if product_status:
                product.product_status = product_status
            
            # Validate updated product data
            product_data = {
                'product_name': product.product_name,
                'price': product.price
            }
            self.error_handler.validate_product_data(product_data)
            
            updated_product = self.product_service.product_repo.update(product)
            print(f"Product updated successfully.")
        except ValueError:
            print("Invalid input. Please enter valid values.")
        except Exception as e:
            self.error_handler.log_error(e, "update_product")
            print(f"Error updating product: {e}")
    
    def delete_product(self):
        """Delete a product"""
        try:
            product_id = int(input("Enter product ID to delete: "))
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete product with ID {product_id}? (y/N): ").lower()
            if confirm != 'y':
                print("Deletion cancelled.")
                return
            
            success = self.product_service.delete_product(product_id)
            if success:
                print(f"Product with ID {product_id} deleted successfully.")
            else:
                print(f"Failed to delete product with ID {product_id}.")
        except ValueError:
            print("Invalid product ID. Please enter a number.")
        except Exception as e:
            self.error_handler.log_error(e, "delete_product")
            print(f"Error deleting product: {e}")
    
    def products_by_category(self):
        """List products by category"""
        try:
            category_id = int(input("Enter category ID: "))
            products = self.product_service.product_repo.get_products_by_category(category_id)
            
            if not products:
                print(f"No products found in category {category_id}.")
                return
            
            print(f"\nProducts in Category {category_id}:")
            print(f"\n{'ID':<5} {'Product Name':<30} {'Price':<10} {'In Stock':<10}")
            print("-" * 60)
            for product in products:
                stock_status = "Yes" if product.in_stock else "No"
                print(f"{product.product_id:<5} {product.product_name:<30} {product.price:<10.2f} {stock_status:<10}")
        except ValueError:
            print("Invalid category ID. Please enter a number.")
        except Exception as e:
            self.error_handler.log_error(e, "products_by_category")
            print(f"Error listing products by category: {e}")
    
    def products_in_stock(self):
        """List products that are in stock"""
        try:
            products = self.product_service.product_repo.get_products_in_stock()
            
            if not products:
                print("No products in stock.")
                return
            
            print(f"\nProducts In Stock:")
            print(f"\n{'ID':<5} {'Product Name':<30} {'Price':<10}")
            print("-" * 50)
            for product in products:
                print(f"{product.product_id:<5} {product.product_name:<30} {product.price:<10.2f}")
        except Exception as e:
            self.error_handler.log_error(e, "products_in_stock")
            print(f"Error listing products in stock: {e}")
    
    def list_orders(self):
        """List all orders"""
        try:
            orders = self.order_service.order_repo.get_all()
            if not orders:
                print("No orders found.")
                return
            
            print(f"\n{'ID':<5} {'Customer ID':<12} {'Date':<20} {'Total':<10} {'Status':<12}")
            print("-" * 65)
            for order in orders:
                print(f"{order.order_id:<5} {order.customer_id:<12} {str(order.order_date):<20} {order.total_amount:<10.2f} {order.order_status:<12}")
        except Exception as e:
            self.error_handler.log_error(e, "list_orders")
            print(f"Error listing orders: {e}")
    
    def view_order_details(self):
        """View details of a specific order"""
        try:
            order_id = int(input("Enter order ID: "))
            result = self.order_service.get_order_with_details(order_id)
            
            if not result:
                print(f"Order with ID {order_id} not found.")
                return
            
            order = result['order']
            customer = result['customer']
            order_items = result['order_items']
            
            print(f"\nOrder Details:")
            print(f"Order ID: {order.order_id}")
            print(f"Customer: {customer.first_name} {customer.last_name} ({customer.email})")
            print(f"Order Date: {order.order_date}")
            print(f"Total Amount: {order.total_amount}")
            print(f"Status: {order.order_status}")
            print(f"Priority: {order.is_priority}")
            
            print(f"\nItems in Order:")
            for item in order_items:
                print(f"  - {item['product_name']}: {item['quantity']} x {item['unit_price']} = {item['quantity'] * item['unit_price']}")
        except ValueError:
            print("Invalid order ID. Please enter a number.")
        except Exception as e:
            self.error_handler.log_error(e, "view_order_details")
            print(f"Error viewing order details: {e}")
    
    def create_order(self):
        """Create a new order"""
        try:
            customer_id = int(input("Enter customer ID: "))
            
            # Verify customer exists
            customer = self.customer_service.customer_repo.get_by_id(customer_id)
            if not customer:
                print(f"Customer with ID {customer_id} not found.")
                return
            
            print(f"Creating order for {customer.first_name} {customer.last_name}")
            
            order_items = []
            while True:
                product_id = input("Enter product ID (or 'done' to finish): ").strip()
                if product_id.lower() == 'done':
                    break
                
                try:
                    product_id = int(product_id)
                    # Verify product exists
                    product = self.product_service.product_repo.get_by_id(product_id)
                    if not product:
                        print(f"Product with ID {product_id} not found.")
                        continue
                    
                    quantity = int(input(f"Enter quantity for {product.product_name}: "))
                    if quantity <= 0:
                        print("Quantity must be positive.")
                        continue
                    
                    order_items.append({
                        'product_id': product_id,
                        'quantity': quantity
                    })
                except ValueError:
                    print("Invalid product ID or quantity. Please enter numbers.")
                    continue
            
            if not order_items:
                print("No items added to order.")
                return
            
            # Validate order data
            order_data = {
                'customer_id': customer_id,
                'order_items': order_items
            }
            self.error_handler.validate_order_data(order_data)
            
            # Create the order
            order = self.order_service.create_order_with_items(customer_id, order_items)
            print(f"Order created successfully with ID {order.order_id} for total amount {order.total_amount}")
        except ValueError:
            print("Invalid input. Please enter valid values.")
        except Exception as e:
            self.error_handler.log_error(e, "create_order")
            print(f"Error creating order: {e}")
    
    def update_order_status(self):
        """Update order status"""
        try:
            order_id = int(input("Enter order ID: "))
            new_status = input("Enter new status (pending/processing/shipped/delivered/cancelled): ").strip()
            
            valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            if new_status not in valid_statuses:
                print(f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}")
                return
            
            success = self.order_service.update_order_status(order_id, new_status)
            if success:
                print(f"Order {order_id} status updated to {new_status}.")
            else:
                print(f"Failed to update order {order_id} status.")
        except ValueError:
            print("Invalid order ID. Please enter a number.")
        except Exception as e:
            self.error_handler.log_error(e, "update_order_status")
            print(f"Error updating order status: {e}")
    
    def cancel_order(self):
        """Cancel an order"""
        try:
            order_id = int(input("Enter order ID to cancel: "))
            
            # Confirm cancellation
            confirm = input(f"Are you sure you want to cancel order {order_id}? (y/N): ").lower()
            if confirm != 'y':
                print("Cancellation cancelled.")
                return
            
            success = self.order_service.delete_order(order_id)
            if success:
                print(f"Order {order_id} cancelled successfully.")
            else:
                print(f"Failed to cancel order {order_id}.")
        except ValueError:
            print("Invalid order ID. Please enter a number.")
        except Exception as e:
            self.error_handler.log_error(e, "cancel_order")
            print(f"Error cancelling order: {e}")
    
    def transfer_credit(self):
        """Transfer credit between customers"""
        try:
            from_customer_id = int(input("Enter source customer ID: "))
            to_customer_id = int(input("Enter target customer ID: "))
            amount = float(input("Enter amount to transfer: "))
            
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            success = self.transaction_service.transfer_customer_credit(from_customer_id, to_customer_id, amount)
            if success:
                print(f"Successfully transferred {amount} from customer {from_customer_id} to customer {to_customer_id}.")
            else:
                print("Transfer failed. Check customer IDs and available credit.")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except Exception as e:
            self.error_handler.log_error(e, "transfer_credit")
            print(f"Error transferring credit: {e}")
    
    def place_order_with_check(self):
        """Place an order with inventory check"""
        try:
            customer_id = int(input("Enter customer ID: "))
            
            # Verify customer exists
            customer = self.customer_service.customer_repo.get_by_id(customer_id)
            if not customer:
                print(f"Customer with ID {customer_id} not found.")
                return
            
            print(f"Placing order for {customer.first_name} {customer.last_name}")
            
            order_items = []
            while True:
                product_id = input("Enter product ID (or 'done' to finish): ").strip()
                if product_id.lower() == 'done':
                    break
                
                try:
                    product_id = int(product_id)
                    # Verify product exists
                    product = self.product_service.product_repo.get_by_id(product_id)
                    if not product:
                        print(f"Product with ID {product_id} not found.")
                        continue
                    
                    quantity = int(input(f"Enter quantity for {product.product_name}: "))
                    if quantity <= 0:
                        print("Quantity must be positive.")
                        continue
                    
                    order_items.append({
                        'product_id': product_id,
                        'quantity': quantity
                    })
                except ValueError:
                    print("Invalid product ID or quantity. Please enter numbers.")
                    continue
            
            if not order_items:
                print("No items added to order.")
                return
            
            # Validate order data
            order_data = {
                'customer_id': customer_id,
                'order_items': order_items
            }
            self.error_handler.validate_order_data(order_data)
            
            # Place the order with inventory check
            order_id = self.transaction_service.place_order_with_inventory_check(customer_id, order_items)
            print(f"Order placed successfully with ID {order_id}.")
        except ValueError:
            print("Invalid input. Please enter valid values.")
        except Exception as e:
            self.error_handler.log_error(e, "place_order_with_check")
            print(f"Error placing order: {e}")
    
    def cancel_order_with_refund(self):
        """Cancel an order with refund"""
        try:
            order_id = int(input("Enter order ID to cancel with refund: "))
            
            # Confirm cancellation with refund
            confirm = input(f"Are you sure you want to cancel order {order_id} with refund? (y/N): ").lower()
            if confirm != 'y':
                print("Cancellation with refund cancelled.")
                return
            
            success = self.transaction_service.cancel_order_with_refund(order_id)
            if success:
                print(f"Order {order_id} cancelled and refunded successfully.")
            else:
                print(f"Failed to cancel order {order_id} with refund.")
        except ValueError:
            print("Invalid order ID. Please enter a number.")
        except Exception as e:
            self.error_handler.log_error(e, "cancel_order_with_refund")
            print(f"Error cancelling order with refund: {e}")
    
    def sales_summary_report(self):
        """Generate sales summary report"""
        try:
            report = self.report_service.generate_sales_summary_report()
            print(f"\n--- SALES SUMMARY REPORT ---")
            print(f"Total Customers: {report.get('total_customers', 0)}")
            print(f"Total Orders: {report.get('total_orders', 0)}")
            print(f"Total Revenue: {report.get('total_revenue', 0.0):.2f}")
            print(f"Average Order Value: {report.get('average_order_value', 0.0):.2f}")
            print(f"First Order Date: {report.get('first_order_date')}")
            print(f"Last Order Date: {report.get('last_order_date')}")
        except Exception as e:
            self.error_handler.log_error(e, "sales_summary_report")
            print(f"Error generating sales summary report: {e}")
    
    def top_products_report(self):
        """Generate top products report"""
        try:
            limit_input = input("Enter number of top products to show (default 10): ").strip()
            limit = int(limit_input) if limit_input else 10
            
            report = self.report_service.generate_top_products_report(limit)
            print(f"\n--- TOP {limit} PRODUCTS REPORT ---")
            print(f"{'Rank':<5} {'Product Name':<30} {'Revenue':<12} {'Qty Sold':<10} {'Orders':<8}")
            print("-" * 70)
            
            for i, product in enumerate(report, 1):
                print(f"{i:<5} {product['product_name']:<30} {product['total_revenue']:<12.2f} {product['total_quantity_sold']:<10} {product['number_of_orders']:<8}")
        except ValueError:
            print("Invalid number entered.")
        except Exception as e:
            self.error_handler.log_error(e, "top_products_report")
            print(f"Error generating top products report: {e}")
    
    def customer_order_report(self):
        """Generate customer order report"""
        try:
            report = self.report_service.generate_customer_order_report()
            print(f"\n--- CUSTOMER ORDER REPORT ---")
            print(f"{'ID':<5} {'Name':<25} {'Email':<25} {'Total Spent':<12} {'Orders':<8}")
            print("-" * 80)
            
            for customer in report:
                name = f"{customer['first_name']} {customer['last_name']}"
                print(f"{customer['customer_id']:<5} {name:<25} {customer['email']:<25} {customer['total_spent']:<12.2f} {customer['total_orders']:<8}")
        except Exception as e:
            self.error_handler.log_error(e, "customer_order_report")
            print(f"Error generating customer order report: {e}")
    
    def inventory_report(self):
        """Generate inventory report"""
        try:
            report = self.report_service.generate_inventory_report()
            print(f"\n--- INVENTORY REPORT ---")
            print(f"{'ID':<5} {'Product Name':<30} {'Price':<10} {'In Stock':<10} {'Category':<15} {'Sold':<8}")
            print("-" * 85)
            
            for product in report:
                in_stock = "Yes" if product['in_stock'] else "No"
                print(f"{product['product_id']:<5} {product['product_name']:<30} {product['price']:<10.2f} {in_stock:<10} {product['category_name']:<15} {product['total_sold']:<8}")
        except Exception as e:
            self.error_handler.log_error(e, "inventory_report")
            print(f"Error generating inventory report: {e}")
    
    def monthly_sales_report(self):
        """Generate monthly sales report"""
        try:
            report = self.report_service.generate_monthly_sales_report()
            print(f"\n--- MONTHLY SALES REPORT ---")
            print(f"{'Year':<6} {'Month':<6} {'Orders':<8} {'Customers':<12} {'Revenue':<12} {'Avg Order':<10}")
            print("-" * 60)
            
            for month in report:
                print(f"{month['year']:<6} {month['month']:<6} {month['total_orders']:<8} {month['unique_customers']:<12} {month['monthly_revenue']:<12.2f} {month['average_order_value']:<10.2f}")
        except Exception as e:
            self.error_handler.log_error(e, "monthly_sales_report")
            print(f"Error generating monthly sales report: {e}")
    
    def category_performance_report(self):
        """Generate category performance report"""
        try:
            report = self.report_service.generate_category_performance_report()
            print(f"\n--- CATEGORY PERFORMANCE REPORT ---")
            print(f"{'ID':<5} {'Category':<20} {'Products':<10} {'Revenue':<12} {'Avg Price':<10}")
            print("-" * 65)
            
            for category in report:
                print(f"{category['category_id']:<5} {category['category_name']:<20} {category['total_products']:<10} {category['total_revenue']:<12.2f} {category['average_selling_price']:<10.2f}")
        except Exception as e:
            self.error_handler.log_error(e, "category_performance_report")
            print(f"Error generating category performance report: {e}")
    
    def import_customers_csv(self):
        """Import customers from CSV"""
        try:
            file_path = input("Enter path to CSV file: ").strip()
            if not os.path.exists(file_path):
                print("File does not exist.")
                return
            
            count = self.import_service.import_customers_from_csv(file_path)
            print(f"Successfully imported {count} customers from CSV.")
        except Exception as e:
            self.error_handler.log_error(e, "import_customers_csv")
            print(f"Error importing customers from CSV: {e}")
    
    def import_products_csv(self):
        """Import products from CSV"""
        try:
            file_path = input("Enter path to CSV file: ").strip()
            if not os.path.exists(file_path):
                print("File does not exist.")
                return
            
            count = self.import_service.import_products_from_csv(file_path)
            print(f"Successfully imported {count} products from CSV.")
        except Exception as e:
            self.error_handler.log_error(e, "import_products_csv")
            print(f"Error importing products from CSV: {e}")
    
    def import_customers_json(self):
        """Import customers from JSON"""
        try:
            file_path = input("Enter path to JSON file: ").strip()
            if not os.path.exists(file_path):
                print("File does not exist.")
                return
            
            count = self.import_service.import_customers_from_json(file_path)
            print(f"Successfully imported {count} customers from JSON.")
        except Exception as e:
            self.error_handler.log_error(e, "import_customers_json")
            print(f"Error importing customers from JSON: {e}")
    
    def import_products_json(self):
        """Import products from JSON"""
        try:
            file_path = input("Enter path to JSON file: ").strip()
            if not os.path.exists(file_path):
                print("File does not exist.")
                return
            
            count = self.import_service.import_products_from_json(file_path)
            print(f"Successfully imported {count} products from JSON.")
        except Exception as e:
            self.error_handler.log_error(e, "import_products_json")
            print(f"Error importing products from JSON: {e}")
    
    def view_config(self):
        """View all configuration settings"""
        print("\n--- CURRENT CONFIGURATION ---")
        import json
        print(json.dumps(self.config.settings, indent=2, ensure_ascii=False, default=str))
    
    def update_db_server(self):
        """Update database server in configuration"""
        try:
            current_server = self.config.get('database.server')
            new_server = input(f"Enter new database server (current: {current_server}): ").strip()
            
            if new_server:
                self.config.set('database.server', new_server)
                print(f"Database server updated to: {new_server}")
            else:
                print("Update cancelled.")
        except Exception as e:
            self.error_handler.log_error(e, "update_db_server")
            print(f"Error updating database server: {e}")
    
    def update_db_name(self):
        """Update database name in configuration"""
        try:
            current_db = self.config.get('database.database')
            new_db = input(f"Enter new database name (current: {current_db}): ").strip()
            
            if new_db:
                self.config.set('database.database', new_db)
                print(f"Database name updated to: {new_db}")
            else:
                print("Update cancelled.")
        except Exception as e:
            self.error_handler.log_error(e, "update_db_name")
            print(f"Error updating database name: {e}")
    
    def update_username(self):
        """Update database username in configuration"""
        try:
            current_user = self.config.get('database.username')
            new_user = input(f"Enter new username (current: {current_user}): ").strip()
            
            if new_user:
                self.config.set('database.username', new_user)
                print(f"Username updated to: {new_user}")
            else:
                print("Update cancelled.")
        except Exception as e:
            self.error_handler.log_error(e, "update_username")
            print(f"Error updating username: {e}")
    
    def update_password(self):
        """Update database password in configuration"""
        try:
            import getpass
            current_password = self.config.get('database.password')
            print(f"Current password is set (length: {len(current_password)})")
            new_password = getpass.getpass("Enter new password: ")
            
            if new_password:
                self.config.set('database.password', new_password)
                print("Password updated successfully.")
            else:
                print("Update cancelled.")
        except Exception as e:
            self.error_handler.log_error(e, "update_password")
            print(f"Error updating password: {e}")
    
    def run(self):
        """Run the console application"""
        print("Welcome to the E-commerce Application!")
        
        # Test database connection
        try:
            conn = self.repository_factory.create_customer_repository()._get_connection()
            conn.close()
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")
            print("Please check your configuration.")
            return
        
        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.customer_menu()
            elif choice == '2':
                self.product_menu()
            elif choice == '3':
                self.order_menu()
            elif choice == '4':
                self.transaction_menu()
            elif choice == '5':
                self.report_menu()
            elif choice == '6':
                self.import_menu()
            elif choice == '7':
                self.config_menu()
            elif choice == '0':
                print("Thank you for using the E-commerce Application!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = ConsoleUI()
    app.run()