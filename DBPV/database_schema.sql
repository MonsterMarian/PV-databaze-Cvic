-- Database Schema for E-commerce Application
-- Requirements: 5+ tables, 2 views, 1 M:N relationship, required data types

-- Table 1: Customers
CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    DateOfBirth DATE, -- DATETIME type
    IsActive BIT NOT NULL DEFAULT 1, -- BOOLEAN type
    RegistrationDate DATETIME2 DEFAULT GETDATE(), -- DATETIME type
    CreditLimit DECIMAL(10,2) -- REAL/FLOAT type
);

-- Table 2: Categories
CREATE TABLE Categories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName NVARCHAR(50) NOT NULL,
    Description NVARCHAR(255)
);

-- Table 3: Products
CREATE TABLE Products (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    ProductName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500),
    Price DECIMAL(10,2) NOT NULL, -- REAL/FLOAT type
    CategoryID INT,
    InStock BIT NOT NULL DEFAULT 1, -- BOOLEAN type
    CreatedDate DATETIME2 DEFAULT GETDATE(), -- DATETIME type
    ProductStatus VARCHAR(20) CHECK (ProductStatus IN ('active', 'inactive', 'discontinued')), -- ENUM type
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- Table 4: Orders
CREATE TABLE Orders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATETIME2 DEFAULT GETDATE(), -- DATETIME type
    TotalAmount DECIMAL(10,2), -- REAL/FLOAT type
    OrderStatus VARCHAR(20) CHECK (OrderStatus IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')), -- ENUM type
    IsPriority BIT DEFAULT 0, -- BOOLEAN type
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Table 5: OrderItems (Junction table for M:N relationship between Orders and Products)
CREATE TABLE OrderItems (
    OrderItemID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2), -- REAL/FLOAT type
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Additional table 6: Suppliers (to meet 5+ table requirement)
CREATE TABLE Suppliers (
    SupplierID INT IDENTITY(1,1) PRIMARY KEY,
    CompanyName NVARCHAR(100) NOT NULL,
    ContactName NVARCHAR(100),
    ContactEmail NVARCHAR(100),
    Phone NVARCHAR(20),
    Address NVARCHAR(255),
    IsActive BIT DEFAULT 1 -- BOOLEAN type
);

-- Junction table for M:N relationship between Products and Suppliers
CREATE TABLE ProductSuppliers (
    ProductSupplierID INT IDENTITY(1,1) PRIMARY KEY,
    ProductID INT NOT NULL,
    SupplierID INT NOT NULL,
    SupplyPrice DECIMAL(10,2), -- REAL/FLOAT type
    SupplyDate DATETIME2 DEFAULT GETDATE(), -- DATETIME type
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

-- View 1: Customer Order Summary
CREATE VIEW CustomerOrderSummary AS
SELECT 
    c.CustomerID,
    c.FirstName,
    c.LastName,
    c.Email,
    COUNT(o.OrderID) AS TotalOrders,
    SUM(o.TotalAmount) AS TotalSpent,
    MAX(o.OrderDate) AS LastOrderDate
FROM Customers c
LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.FirstName, c.LastName, c.Email;

-- View 2: Product Sales Summary
CREATE VIEW ProductSalesSummary AS
SELECT 
    p.ProductID,
    p.ProductName,
    p.Price,
    SUM(oi.Quantity) AS TotalQuantitySold,
    SUM(oi.Quantity * oi.UnitPrice) AS TotalRevenue,
    COUNT(DISTINCT oi.OrderID) AS NumberOfOrders
FROM Products p
LEFT JOIN OrderItems oi ON p.ProductID = oi.ProductID
GROUP BY p.ProductID, p.ProductName, p.Price;

-- Insert sample data to test the schema

-- Categories
INSERT INTO Categories (CategoryName, Description) VALUES 
('Electronics', 'Electronic devices and accessories'),
('Books', 'Physical and digital books'),
('Clothing', 'Apparel and accessories');

-- Customers
INSERT INTO Customers (FirstName, LastName, Email, DateOfBirth, CreditLimit) VALUES 
('John', 'Doe', 'john.doe@email.com', '1985-06-15', 5000.00),
('Jane', 'Smith', 'jane.smith@email.com', '1990-03-22', 3000.00),
('Bob', 'Johnson', 'bob.johnson@email.com', '1978-11-30', 4500.00);

-- Products
INSERT INTO Products (ProductName, Description, Price, CategoryID, ProductStatus) VALUES 
('Laptop', 'High-performance laptop', 1299.99, 1, 'active'),
('Programming Book', 'Learn Python Programming', 39.99, 2, 'active'),
('T-Shirt', 'Cotton t-shirt', 19.99, 3, 'active'),
('Smartphone', 'Latest model smartphone', 899.99, 1, 'active');

-- Suppliers
INSERT INTO Suppliers (CompanyName, ContactName, ContactEmail, Phone, Address) VALUES 
('Tech Supplies Inc.', 'Mike Wilson', 'mike@techsupplies.com', '+1234567890', '123 Tech Street'),
('Book Distributors Ltd.', 'Sarah Brown', 'sarah@books.com', '+0987654321', '456 Book Avenue');

-- Product suppliers (M:N relationship)
INSERT INTO ProductSuppliers (ProductID, SupplierID, SupplyPrice) VALUES 
(1, 1, 1000.00), -- Laptop supplied by Tech Supplies
(2, 2, 25.00),   -- Programming Book supplied by Book Distributors
(4, 1, 700.00);  -- Smartphone supplied by Tech Supplies

-- Orders
INSERT INTO Orders (CustomerID, TotalAmount, OrderStatus) VALUES 
(1, 1339.98, 'delivered'), -- John ordered laptop and book
(2, 19.99, 'shipped'),     -- Jane ordered t-shirt
(3, 899.99, 'processing'); -- Bob ordered smartphone

-- Order items (M:N relationship between Orders and Products)
INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice) VALUES 
(1, 1, 1, 1299.99), -- John's order: 1 laptop
(1, 2, 1, 39.99),   -- John's order: 1 book
(2, 3, 1, 19.99),   -- Jane's order: 1 t-shirt
(3, 4, 1, 899.99);  -- Bob's order: 1 smartphone