Test Scenario Document: Customer and Product Management Functions
================================================================

Document ID: TS-FUNC-001
Version: 1.0
Date: December 2025
Author: Test Team

1. PURPOSE
-----------
This document describes the test scenario for verifying customer and product management functions in the E-commerce Application. This includes CRUD operations on customers and products.

2. PREREQUISITES
----------------
- Application setup completed successfully
- Database connection established
- Basic database schema in place
- Application configuration verified

3. TEST STEPS
-------------
3.1 Customer Management Tests
- Start the application console UI
- Navigate to Customer Management menu (Option 1)
- Test 1: List all customers
  - Expected: Shows existing customers or "No customers found"
- Test 2: Add new customer
  - Enter: First Name: John, Last Name: Doe, Email: john.doe@test.com
  - Expected: Customer added successfully with new ID
- Test 3: View customer details
  - Enter existing customer ID
  - Expected: Customer details displayed correctly
- Test 4: Update customer
  - Select existing customer, update email
  - Expected: Customer updated successfully
- Test 5: Delete customer
  - Select created customer, confirm deletion
  - Expected: Customer deleted successfully

3.2 Product Management Tests
- Navigate to Product Management menu (Option 2)
- Test 6: List all products
  - Expected: Shows existing products or "No products found"
- Test 7: Add new product
  - Enter: Product Name: Test Product, Description: Test, Price: 29.99
  - Expected: Product added successfully with new ID
- Test 8: View product details
  - Enter existing product ID
  - Expected: Product details displayed with category and order information
- Test 9: Update product
  - Select existing product, update price
  - Expected: Product updated successfully
- Test 10: Delete product
  - Select created product, confirm deletion
  - Expected: Product deleted successfully

3.3 Data Validation Tests
- Test 11: Add customer with invalid email
  - Enter: Email without @ symbol
  - Expected: Validation error message displayed
- Test 12: Add product with negative price
  - Enter: Price: -10.00
  - Expected: Validation error message displayed

4. VERIFICATION STEPS
---------------------
4.1 Database Verification
- After each create/update/delete operation, verify database reflects changes
- Check that related records are properly maintained

4.2 UI Response Verification
- Confirm all operations provide appropriate feedback
- Verify error messages are clear and actionable

5. SUCCESS CRITERIA
-------------------
- All CRUD operations complete successfully
- Data validation works correctly
- Database changes are persisted
- UI provides clear feedback
- Error handling works as expected

6. FAILURE CONDITIONS
---------------------
- CRUD operations fail
- Validation doesn't work properly
- Database operations cause errors
- UI doesn't respond appropriately
- Error messages are unclear

7. ERROR HANDLING
-----------------
- If customer creation fails, verify all required fields are provided
- If product creation fails, verify price is positive number
- If database operations fail, check connection and permissions
- If validation doesn't work, verify error handling implementation

8. POST-CONDITIONS
------------------
- Customer and product data integrity maintained
- All operations properly validated
- Error conditions handled gracefully
- Database consistency preserved