-- ============================================================
-- LULU MALL RETAIL ANALYTICS
-- 04 - DATA VALIDATION
-- ============================================================

USE lulu_mall_analytics;

-- Total records
SELECT COUNT(*) AS Total_Rows
FROM sales;

-- Check duplicate Order IDs
SELECT
    Order_ID,
    COUNT(*) AS Duplicate_Count
FROM sales
GROUP BY Order_ID
HAVING COUNT(*) > 1;

-- Check NULL values
SELECT
    COUNT(*) AS Total_Rows,
    SUM(Order_ID IS NULL) AS Null_Order_ID,
    SUM(Order_Date IS NULL) AS Null_Order_Date,
    SUM(Store_ID IS NULL) AS Null_Store_ID,
    SUM(Customer_ID IS NULL) AS Null_Customer_ID,
    SUM(Product_Name IS NULL) AS Null_Product_Name,
    SUM(Quantity IS NULL) AS Null_Quantity,
    SUM(Unit_Price IS NULL) AS Null_Unit_Price,
    SUM(Revenue IS NULL) AS Null_Revenue
FROM sales;

-- Validate Revenue
SELECT
    COUNT(*) AS Incorrect_Revenue_Records
FROM sales
WHERE Revenue <> Quantity * Unit_Price;

-- Check negative quantities
SELECT *
FROM sales
WHERE Quantity <= 0;

-- check data range
SELECT
    MIN(Order_Date) AS First_Order_Date,
    MAX(Order_Date) AS Last_Order_Date
FROM sales;

-- basic data summary
SELECT
    COUNT(*) AS Transactions,
    COUNT(DISTINCT Order_ID) AS Orders,
    COUNT(DISTINCT Customer_ID) AS Customers,
    COUNT(DISTINCT Store_ID) AS Stores,
    COUNT(DISTINCT Product_Name) AS Products,
    SUM(Quantity) AS Total_Quantity,
    SUM(Revenue) AS Total_Revenue
FROM sales;