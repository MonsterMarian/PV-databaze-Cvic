"""
Reporting Module for E-commerce Application
Generates aggregated reports from 3+ tables as required by the assignment
"""
from typing import List, Dict, Any
from config.config_manager import Config
from repositories.base_repository import BaseRepository


class ReportService:
    """Service class for generating various business reports"""
    
    def __init__(self, config: Config):
        self.config = config
        self.base_repo = BaseRepository(config.get_database_connection_string())
    
    def generate_sales_summary_report(self) -> Dict[str, Any]:
        """
        Generate a sales summary report using data from Customers, Orders, and OrderItems tables
        """
        query = """
        SELECT 
            COUNT(DISTINCT c.CustomerID) AS TotalCustomers,
            COUNT(o.OrderID) AS TotalOrders,
            SUM(o.TotalAmount) AS TotalRevenue,
            AVG(o.TotalAmount) AS AverageOrderValue,
            MIN(o.OrderDate) AS FirstOrderDate,
            MAX(o.OrderDate) AS LastOrderDate
        FROM Customers c
        LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
        WHERE o.OrderStatus != 'cancelled'
        """
        
        result = self.base_repo._execute_query(query)
        if result:
            row = result[0]
            return {
                'total_customers': row[0] or 0,
                'total_orders': row[1] or 0,
                'total_revenue': float(row[2]) if row[2] else 0.0,
                'average_order_value': float(row[3]) if row[3] else 0.0,
                'first_order_date': row[4],
                'last_order_date': row[5]
            }
        return {}
    
    def generate_top_products_report(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Generate a report of top selling products using data from Products, OrderItems, and Orders tables
        """
        query = """
        SELECT 
            p.ProductID,
            p.ProductName,
            p.Price,
            SUM(oi.Quantity) AS TotalQuantitySold,
            SUM(oi.Quantity * oi.UnitPrice) AS TotalRevenue,
            COUNT(DISTINCT oi.OrderID) AS NumberOfOrders
        FROM Products p
        JOIN OrderItems oi ON p.ProductID = oi.ProductID
        JOIN Orders o ON oi.OrderID = o.OrderID
        WHERE o.OrderStatus != 'cancelled'
        GROUP BY p.ProductID, p.ProductName, p.Price
        ORDER BY TotalRevenue DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        results = self.base_repo._execute_query(query)
        products_report = []
        for row in results:
            products_report.append({
                'product_id': row[0],
                'product_name': row[1],
                'price': float(row[2]),
                'total_quantity_sold': row[3],
                'total_revenue': float(row[4]),
                'number_of_orders': row[5]
            })
        return products_report
    
    def generate_customer_order_report(self) -> List[Dict[str, Any]]:
        """
        Generate a report of customers with their order summaries using data from Customers, Orders, and OrderItems tables
        """
        query = """
        SELECT 
            c.CustomerID,
            c.FirstName,
            c.LastName,
            c.Email,
            COUNT(o.OrderID) AS TotalOrders,
            SUM(o.TotalAmount) AS TotalSpent,
            AVG(o.TotalAmount) AS AverageOrderValue,
            MAX(o.OrderDate) AS LastOrderDate,
            MIN(o.OrderDate) AS FirstOrderDate
        FROM Customers c
        LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
        WHERE o.OrderStatus != 'cancelled' OR o.OrderID IS NULL
        GROUP BY c.CustomerID, c.FirstName, c.LastName, c.Email
        ORDER BY TotalSpent DESC
        """
        
        results = self.base_repo._execute_query(query)
        customer_report = []
        for row in results:
            customer_report.append({
                'customer_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'total_orders': row[4],
                'total_spent': float(row[5]) if row[5] else 0.0,
                'average_order_value': float(row[6]) if row[6] else 0.0,
                'last_order_date': row[7],
                'first_order_date': row[8]
            })
        return customer_report
    
    def generate_inventory_report(self) -> List[Dict[str, Any]]:
        """
        Generate an inventory report using data from Products, Categories, and OrderItems tables
        """
        query = """
        SELECT 
            p.ProductID,
            p.ProductName,
            p.Price,
            p.InStock,
            c.CategoryName,
            SUM(COALESCE(oi.Quantity, 0)) AS TotalSold,
            COUNT(DISTINCT oi.OrderID) AS TimesOrdered
        FROM Products p
        LEFT JOIN Categories c ON p.CategoryID = c.CategoryID
        LEFT JOIN OrderItems oi ON p.ProductID = oi.ProductID
        LEFT JOIN Orders o ON oi.OrderID = o.OrderID AND o.OrderStatus != 'cancelled'
        GROUP BY p.ProductID, p.ProductName, p.Price, p.InStock, c.CategoryName
        ORDER BY p.ProductName
        """
        
        results = self.base_repo._execute_query(query)
        inventory_report = []
        for row in results:
            inventory_report.append({
                'product_id': row[0],
                'product_name': row[1],
                'price': float(row[2]),
                'in_stock': bool(row[3]),
                'category_name': row[4],
                'total_sold': row[5],
                'times_ordered': row[6]
            })
        return inventory_report
    
    def generate_monthly_sales_report(self) -> List[Dict[str, Any]]:
        """
        Generate a monthly sales report using data from Orders, OrderItems, and Customers tables
        """
        query = """
        SELECT 
            YEAR(o.OrderDate) AS Year,
            MONTH(o.OrderDate) AS Month,
            COUNT(o.OrderID) AS TotalOrders,
            COUNT(DISTINCT o.CustomerID) AS UniqueCustomers,
            SUM(o.TotalAmount) AS MonthlyRevenue,
            AVG(o.TotalAmount) AS AverageOrderValue
        FROM Orders o
        JOIN Customers c ON o.CustomerID = c.CustomerID
        WHERE o.OrderStatus != 'cancelled'
        GROUP BY YEAR(o.OrderDate), MONTH(o.OrderDate)
        ORDER BY YEAR(o.OrderDate), MONTH(o.OrderDate)
        """
        
        results = self.base_repo._execute_query(query)
        monthly_report = []
        for row in results:
            monthly_report.append({
                'year': row[0],
                'month': row[1],
                'total_orders': row[2],
                'unique_customers': row[3],
                'monthly_revenue': float(row[4]),
                'average_order_value': float(row[5])
            })
        return monthly_report
    
    def generate_category_performance_report(self) -> List[Dict[str, Any]]:
        """
        Generate a report on category performance using data from Categories, Products, OrderItems, and Orders tables
        """
        query = """
        SELECT 
            c.CategoryID,
            c.CategoryName,
            COUNT(DISTINCT p.ProductID) AS TotalProducts,
            SUM(oi.Quantity) AS TotalItemsSold,
            SUM(oi.Quantity * oi.UnitPrice) AS TotalRevenue,
            AVG(oi.UnitPrice) AS AverageSellingPrice
        FROM Categories c
        LEFT JOIN Products p ON c.CategoryID = p.CategoryID
        LEFT JOIN OrderItems oi ON p.ProductID = oi.ProductID
        LEFT JOIN Orders o ON oi.OrderID = o.OrderID
        WHERE o.OrderStatus != 'cancelled' OR o.OrderID IS NULL
        GROUP BY c.CategoryID, c.CategoryName
        ORDER BY TotalRevenue DESC
        """
        
        results = self.base_repo._execute_query(query)
        category_report = []
        for row in results:
            category_report.append({
                'category_id': row[0],
                'category_name': row[1],
                'total_products': row[2],
                'total_items_sold': row[3],
                'total_revenue': float(row[4]) if row[4] else 0.0,
                'average_selling_price': float(row[5]) if row[5] else 0.0
            })
        return category_report
    
    def export_report_to_dict(self, report_type: str) -> Dict[str, Any]:
        """
        Export any report as a dictionary for further processing
        """
        if report_type == 'sales_summary':
            return {
                'report_type': 'sales_summary',
                'data': self.generate_sales_summary_report(),
                'generated_at': __import__('datetime').datetime.now()
            }
        elif report_type == 'top_products':
            return {
                'report_type': 'top_products',
                'data': self.generate_top_products_report(),
                'generated_at': __import__('datetime').datetime.now()
            }
        elif report_type == 'customer_orders':
            return {
                'report_type': 'customer_orders',
                'data': self.generate_customer_order_report(),
                'generated_at': __import__('datetime').datetime.now()
            }
        elif report_type == 'inventory':
            return {
                'report_type': 'inventory',
                'data': self.generate_inventory_report(),
                'generated_at': __import__('datetime').datetime.now()
            }
        elif report_type == 'monthly_sales':
            return {
                'report_type': 'monthly_sales',
                'data': self.generate_monthly_sales_report(),
                'generated_at': __import__('datetime').datetime.now()
            }
        elif report_type == 'category_performance':
            return {
                'report_type': 'category_performance',
                'data': self.generate_category_performance_report(),
                'generated_at': __import__('datetime').datetime.now()
            }
        else:
            raise ValueError(f"Unknown report type: {report_type}")