-- Total Revenue
SELECT SUM(Revenue) as total_revenue
FROM sales;

-- Monthly Revenue
SELECT 
    strftime('%Y-%m', InvoiceDate) as month,
    SUM(Revenue) as revenue
FROM sales
GROUP BY month
ORDER BY month;

-- Top Products
SELECT 
    Description,
    SUM(Revenue) as revenue
FROM sales
GROUP BY Description
ORDER BY revenue DESC
LIMIT 10;

-- Top Customers
SELECT 
    CustomerID,
    SUM(Revenue) as total_spent
FROM sales
GROUP BY CustomerID
ORDER BY total_spent DESC
LIMIT 10;

-- Revenue by Country
SELECT 
    Country,
    SUM(Revenue) as revenue
FROM sales
GROUP BY Country
ORDER BY revenue DESC
LIMIT 10;

-- Average Order Value
SELECT 
    SUM(Revenue) / COUNT(DISTINCT InvoiceNo) as avg_order_value
FROM sales;