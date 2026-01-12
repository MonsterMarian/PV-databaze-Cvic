"""
Entity Models for E-commerce Application
"""


class Customer:
    def __init__(self, customer_id=None, first_name=None, last_name=None, email=None, 
                 date_of_birth=None, is_active=True, registration_date=None, credit_limit=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.is_active = is_active
        self.registration_date = registration_date
        self.credit_limit = credit_limit

    def __str__(self):
        return f"Customer(ID: {self.customer_id}, Name: {self.first_name} {self.last_name}, Email: {self.email})"


class Product:
    def __init__(self, product_id=None, product_name=None, description=None, price=None,
                 category_id=None, in_stock=True, created_date=None, product_status='active'):
        self.product_id = product_id
        self.product_name = product_name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.in_stock = in_stock
        self.created_date = created_date
        self.product_status = product_status

    def __str__(self):
        return f"Product(ID: {self.product_id}, Name: {self.product_name}, Price: {self.price})"


class Order:
    def __init__(self, order_id=None, customer_id=None, order_date=None, total_amount=None,
                 order_status='pending', is_priority=False):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date
        self.total_amount = total_amount
        self.order_status = order_status
        self.is_priority = is_priority

    def __str__(self):
        return f"Order(ID: {self.order_id}, CustomerID: {self.customer_id}, Total: {self.total_amount})"


class OrderItem:
    def __init__(self, order_item_id=None, order_id=None, product_id=None, quantity=None, unit_price=None):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

    def __str__(self):
        return f"OrderItem(ID: {self.order_item_id}, OrderID: {self.order_id}, ProductID: {self.product_id}, Qty: {self.quantity})"


class Category:
    def __init__(self, category_id=None, category_name=None, description=None):
        self.category_id = category_id
        self.category_name = category_name
        self.description = description

    def __str__(self):
        return f"Category(ID: {self.category_id}, Name: {self.category_name})"


class Supplier:
    def __init__(self, supplier_id=None, company_name=None, contact_name=None, contact_email=None,
                 phone=None, address=None, is_active=True):
        self.supplier_id = supplier_id
        self.company_name = company_name
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.phone = phone
        self.address = address
        self.is_active = is_active

    def __str__(self):
        return f"Supplier(ID: {self.supplier_id}, Company: {self.company_name})"