-- Total revenue
SELECT 
    SUM(Revenue) AS Total_Revenue
FROM sales;

-- Total Orders
SELECT
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales;

-- Customers
SELECT
    COUNT(DISTINCT Customer_ID) AS Total_Customers
FROM sales;

-- Revenue by category
SELECT
    Product_Category,
    SUM(Revenue) AS Total_Revenue
FROM sales
GROUP BY Product_Category
ORDER BY Total_Revenue DESC;

