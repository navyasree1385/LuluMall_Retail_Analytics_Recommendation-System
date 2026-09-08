USE lulu_mall_analytics;
-- Unique Customers
SELECT
    COUNT(DISTINCT Customer_ID) AS Total_Customers
FROM sales;

-- Customer Spending
SELECT
    Customer_ID,
    SUM(Revenue) AS Total_Revenue
FROM sales
GROUP BY Customer_ID
ORDER BY Total_Revenue DESC;

-- top 10 customers
SELECT
    Customer_ID,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Quantity) AS Total_Quantity,
    SUM(Revenue) AS Total_Revenue
FROM sales
GROUP BY Customer_ID
ORDER BY Total_Revenue DESC
LIMIT 10;

-- customer AOV
SELECT
    Customer_ID,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Revenue) AS Total_Revenue,
    ROUND(
        SUM(Revenue) / COUNT(DISTINCT Order_ID),
        2
    ) AS Average_Order_Value
FROM sales
GROUP BY Customer_ID
ORDER BY Total_Revenue DESC;

-- customers by gender
SELECT
    Customer_Gender,
    COUNT(DISTINCT Customer_ID) AS Total_Customers
FROM sales
GROUP BY Customer_Gender;

-- customer revenue by gender
SELECT
    Customer_Gender,
    COUNT(DISTINCT Customer_ID) AS Customers,
    SUM(Revenue) AS Total_Revenue,
    ROUND(
        SUM(Revenue) * 100 /
        (SELECT SUM(Revenue) FROM sales),
        2
    ) AS Revenue_Percentage
FROM sales
GROUP BY Customer_Gender;

-- customer purschase frequency
SELECT
    Customer_ID,
    COUNT(DISTINCT Order_ID) AS Purchase_Frequency,
    SUM(Revenue) AS Total_Revenue
FROM sales
GROUP BY Customer_ID
ORDER BY Purchase_Frequency DESC;

-- customer segmentation
SELECT
    Customer_ID,
    SUM(Revenue) AS Total_Revenue,

    CASE
        WHEN SUM(Revenue) >= 50000
            THEN 'High Value'

        WHEN SUM(Revenue) >= 25000
            THEN 'Regular'

        WHEN SUM(Revenue) >= 10000
            THEN 'Occasional'

        ELSE 'Low Value'
    END AS Customer_Segment

FROM sales

GROUP BY Customer_ID

ORDER BY Total_Revenue DESC;