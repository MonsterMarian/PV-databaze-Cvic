"""
Data Import Module for E-commerce Application
Implements data import from CSV, XML, and JSON formats to at least 2 tables
"""
import csv
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from config.config_manager import Config
from repositories.base_repository import BaseRepository
from models.entities import Customer, Product


class DataImportService:
    """Service class for importing data from various formats to database tables"""
    
    def __init__(self, config: Config):
        self.config = config
        self.base_repo = BaseRepository(config.get_database_connection_string())
    
    def import_customers_from_csv(self, file_path: str) -> int:
        """
        Import customers from CSV file to Customers table
        """
        imported_count = 0
        
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # Prepare data for insertion
                    first_name = row.get('FirstName', '').strip()
                    last_name = row.get('LastName', '').strip()
                    email = row.get('Email', '').strip()
                    
                    # Skip if required fields are missing
                    if not first_name or not last_name or not email:
                        continue
                    
                    # Check if customer already exists
                    existing_customer = self.base_repo._execute_scalar(
                        "SELECT CustomerID FROM Customers WHERE Email = ?", 
                        (email,)
                    )
                    
                    if existing_customer:
                        continue  # Skip if customer already exists
                    
                    # Extract optional fields
                    date_of_birth = row.get('DateOfBirth', None)
                    credit_limit_str = row.get('CreditLimit', '0')
                    try:
                        credit_limit = float(credit_limit_str) if credit_limit_str else 0.0
                    except ValueError:
                        credit_limit = 0.0
                    
                    # Insert customer
                    query = """
                    INSERT INTO Customers (FirstName, LastName, Email, DateOfBirth, CreditLimit)
                    VALUES (?, ?, ?, ?, ?)
                    """
                    
                    self.base_repo._execute_non_query(query, (
                        first_name,
                        last_name,
                        email,
                        date_of_birth if date_of_birth else None,
                        credit_limit
                    ))
                    
                    imported_count += 1
                except Exception as e:
                    print(f"Error importing customer from row: {row}, Error: {e}")
                    continue
        
        return imported_count
    
    def import_products_from_csv(self, file_path: str) -> int:
        """
        Import products from CSV file to Products table
        """
        imported_count = 0
        
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # Prepare data for insertion
                    product_name = row.get('ProductName', '').strip()
                    description = row.get('Description', '').strip()
                    
                    # Skip if required fields are missing
                    if not product_name:
                        continue
                    
                    # Extract other fields
                    price_str = row.get('Price', '0')
                    try:
                        price = float(price_str) if price_str else 0.0
                    except ValueError:
                        price = 0.0
                    
                    category_id_str = row.get('CategoryID', '1')  # Default to 1 if not specified
                    try:
                        category_id = int(category_id_str) if category_id_str else 1
                    except ValueError:
                        category_id = 1
                    
                    in_stock = row.get('InStock', '1').lower() in ['1', 'true', 'yes', 't', 'y']
                    product_status = row.get('ProductStatus', 'active')
                    
                    # Check if product already exists
                    existing_product = self.base_repo._execute_scalar(
                        "SELECT ProductID FROM Products WHERE ProductName = ?", 
                        (product_name,)
                    )
                    
                    if existing_product:
                        continue  # Skip if product already exists
                    
                    # Insert product
                    query = """
                    INSERT INTO Products (ProductName, Description, Price, CategoryID, InStock, ProductStatus)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """
                    
                    self.base_repo._execute_non_query(query, (
                        product_name,
                        description,
                        price,
                        category_id,
                        in_stock,
                        product_status
                    ))
                    
                    imported_count += 1
                except Exception as e:
                    print(f"Error importing product from row: {row}, Error: {e}")
                    continue
        
        return imported_count
    
    def import_customers_from_json(self, file_path: str) -> int:
        """
        Import customers from JSON file to Customers table
        """
        imported_count = 0
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # If data is a single object, convert to list
            if isinstance(data, dict):
                data = [data]
            
            for customer_data in data:
                try:
                    # Prepare data for insertion
                    first_name = customer_data.get('FirstName', '').strip()
                    last_name = customer_data.get('LastName', '').strip()
                    email = customer_data.get('Email', '').strip()
                    
                    # Skip if required fields are missing
                    if not first_name or not last_name or not email:
                        continue
                    
                    # Extract optional fields
                    date_of_birth = customer_data.get('DateOfBirth', None)
                    credit_limit = customer_data.get('CreditLimit', 0.0)
                    
                    # Check if customer already exists
                    existing_customer = self.base_repo._execute_scalar(
                        "SELECT CustomerID FROM Customers WHERE Email = ?", 
                        (email,)
                    )
                    
                    if existing_customer:
                        continue  # Skip if customer already exists
                    
                    # Insert customer
                    query = """
                    INSERT INTO Customers (FirstName, LastName, Email, DateOfBirth, CreditLimit)
                    VALUES (?, ?, ?, ?, ?)
                    """
                    
                    self.base_repo._execute_non_query(query, (
                        first_name,
                        last_name,
                        email,
                        date_of_birth,
                        credit_limit
                    ))
                    
                    imported_count += 1
                except Exception as e:
                    print(f"Error importing customer from data: {customer_data}, Error: {e}")
                    continue
        
        return imported_count
    
    def import_products_from_json(self, file_path: str) -> int:
        """
        Import products from JSON file to Products table
        """
        imported_count = 0
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # If data is a single object, convert to list
            if isinstance(data, dict):
                data = [data]
            
            for product_data in data:
                try:
                    # Prepare data for insertion
                    product_name = product_data.get('ProductName', '').strip()
                    description = product_data.get('Description', '').strip()
                    
                    # Skip if required fields are missing
                    if not product_name:
                        continue
                    
                    # Extract other fields
                    price = product_data.get('Price', 0.0)
                    category_id = product_data.get('CategoryID', 1)
                    in_stock = product_data.get('InStock', True)
                    product_status = product_data.get('ProductStatus', 'active')
                    
                    # Check if product already exists
                    existing_product = self.base_repo._execute_scalar(
                        "SELECT ProductID FROM Products WHERE ProductName = ?", 
                        (product_name,)
                    )
                    
                    if existing_product:
                        continue  # Skip if product already exists
                    
                    # Insert product
                    query = """
                    INSERT INTO Products (ProductName, Description, Price, CategoryID, InStock, ProductStatus)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """
                    
                    self.base_repo._execute_non_query(query, (
                        product_name,
                        description,
                        price,
                        category_id,
                        in_stock,
                        product_status
                    ))
                    
                    imported_count += 1
                except Exception as e:
                    print(f"Error importing product from data: {product_data}, Error: {e}")
                    continue
        
        return imported_count
    
    def import_customers_from_xml(self, file_path: str) -> int:
        """
        Import customers from XML file to Customers table
        """
        imported_count = 0
        
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Look for customer elements (try different possible root tags)
        customer_elements = root.findall('.//Customer') or root.findall('.//customer') or [root]
        
        for customer_elem in customer_elements:
            try:
                # Extract customer data from XML
                first_name_elem = customer_elem.find('FirstName') or customer_elem.find('first_name')
                last_name_elem = customer_elem.find('LastName') or customer_elem.find('last_name')
                email_elem = customer_elem.find('Email') or customer_elem.find('email')
                
                first_name = (first_name_elem.text if first_name_elem is not None else '').strip()
                last_name = (last_name_elem.text if last_name_elem is not None else '').strip()
                email = (email_elem.text if email_elem is not None else '').strip()
                
                # Skip if required fields are missing
                if not first_name or not last_name or not email:
                    continue
                
                # Extract optional fields
                date_of_birth_elem = customer_elem.find('DateOfBirth') or customer_elem.find('date_of_birth')
                date_of_birth = date_of_birth_elem.text if date_of_birth_elem is not None else None
                
                credit_limit_elem = customer_elem.find('CreditLimit') or customer_elem.find('credit_limit')
                credit_limit = float(credit_limit_elem.text) if credit_limit_elem is not None and credit_limit_elem.text else 0.0
                
                # Check if customer already exists
                existing_customer = self.base_repo._execute_scalar(
                    "SELECT CustomerID FROM Customers WHERE Email = ?", 
                    (email,)
                )
                
                if existing_customer:
                    continue  # Skip if customer already exists
                
                # Insert customer
                query = """
                INSERT INTO Customers (FirstName, LastName, Email, DateOfBirth, CreditLimit)
                VALUES (?, ?, ?, ?, ?)
                """
                
                self.base_repo._execute_non_query(query, (
                    first_name,
                    last_name,
                    email,
                    date_of_birth,
                    credit_limit
                ))
                
                imported_count += 1
            except Exception as e:
                print(f"Error importing customer from XML element: {customer_elem.tag}, Error: {e}")
                continue
        
        return imported_count
    
    def import_products_from_xml(self, file_path: str) -> int:
        """
        Import products from XML file to Products table
        """
        imported_count = 0
        
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Look for product elements (try different possible root tags)
        product_elements = root.findall('.//Product') or root.findall('.//product') or [root]
        
        for product_elem in product_elements:
            try:
                # Extract product data from XML
                product_name_elem = product_elem.find('ProductName') or product_elem.find('product_name')
                description_elem = product_elem.find('Description') or product_elem.find('description')
                
                product_name = (product_name_elem.text if product_name_elem is not None else '').strip()
                description = (description_elem.text if description_elem is not None else '').strip()
                
                # Skip if required fields are missing
                if not product_name:
                    continue
                
                # Extract other fields
                price_elem = product_elem.find('Price') or product_elem.find('price')
                price = float(price_elem.text) if price_elem is not None and price_elem.text else 0.0
                
                category_id_elem = product_elem.find('CategoryID') or product_elem.find('category_id')
                category_id = int(category_id_elem.text) if category_id_elem is not None and category_id_elem.text else 1
                
                in_stock_elem = product_elem.find('InStock') or product_elem.find('in_stock')
                in_stock = in_stock_elem.text.lower() in ['1', 'true', 'yes', 't', 'y'] if in_stock_elem is not None and in_stock_elem.text else True
                
                status_elem = product_elem.find('ProductStatus') or product_elem.find('product_status')
                product_status = status_elem.text if status_elem is not None and status_elem.text else 'active'
                
                # Check if product already exists
                existing_product = self.base_repo._execute_scalar(
                    "SELECT ProductID FROM Products WHERE ProductName = ?", 
                    (product_name,)
                )
                
                if existing_product:
                    continue  # Skip if product already exists
                
                # Insert product
                query = """
                INSERT INTO Products (ProductName, Description, Price, CategoryID, InStock, ProductStatus)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                
                self.base_repo._execute_non_query(query, (
                    product_name,
                    description,
                    price,
                    category_id,
                    in_stock,
                    product_status
                ))
                
                imported_count += 1
            except Exception as e:
                print(f"Error importing product from XML element: {product_elem.tag}, Error: {e}")
                continue
        
        return imported_count
    
    def import_from_file(self, file_path: str, table_name: str) -> int:
        """
        Generic import method that determines format from file extension
        """
        if file_path.lower().endswith('.csv'):
            if table_name.lower() == 'customers':
                return self.import_customers_from_csv(file_path)
            elif table_name.lower() == 'products':
                return self.import_products_from_csv(file_path)
        elif file_path.lower().endswith('.json'):
            if table_name.lower() == 'customers':
                return self.import_customers_from_json(file_path)
            elif table_name.lower() == 'products':
                return self.import_products_from_json(file_path)
        elif file_path.lower().endswith('.xml'):
            if table_name.lower() == 'customers':
                return self.import_customers_from_xml(file_path)
            elif table_name.lower() == 'products':
                return self.import_products_from_xml(file_path)
        
        raise ValueError(f"Unsupported file format or table name: {file_path}, {table_name}")