CREATE DATABASE vendor_intelligence; 
USE vendor_intelligence;  
 -- Total orders by vendor
SELECT
    Supplier,
    COUNT(PO_ID) AS Total_Orders
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Total_Orders DESC; 
-- Total spending by vendor
SELECT
    Supplier,
    SUM(Total_Spend) AS Total_Spend
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Total_Spend DESC;  
-- Total savings by vendor
SELECT
    Supplier,
    SUM(Savings) AS Total_Savings
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Total_Savings DESC;  
-- Average delivery time
SELECT
    Supplier,
    ROUND(AVG(Delivery_Days), 2) AS Avg_Delivery_Days
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Avg_Delivery_Days;  
-- Top 5 vendors by spending
SELECT
    Supplier,
    ROUND(SUM(Total_Spend), 2) AS Total_Spend
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Total_Spend DESC;
 
-- Top 5 vendors by savings
SELECT
    Supplier,
    ROUND(SUM(Savings), 2) AS Total_Savings
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Total_Savings DESC; 
-- Spending by category
SELECT
    Item_Category,
    ROUND(SUM(Total_Spend), 2) AS Total_Spend
FROM vendor_cleaned_kpi
GROUP BY Item_Category
ORDER BY Total_Spend DESC;   
-- Orders by category
SELECT
    Item_Category,
    COUNT(PO_ID) AS Total_Orders
FROM vendor_cleaned_kpi
GROUP BY Item_Category
ORDER BY Total_Orders DESC;     
-- Order status analysis
SELECT
    Order_Status,
    COUNT(PO_ID) AS Total_Orders
FROM vendor_cleaned_kpi
GROUP BY Order_Status
ORDER BY Total_Orders DESC;  
-- Vendors with highest defect rate
SELECT
    Supplier,
    ROUND(AVG(Defect_Rate), 2) AS Avg_Defect_Rate
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Avg_Defect_Rate DESC;   
-- Vendors with slowest delivery
SELECT
    Supplier,
    ROUND(AVG(Delivery_Days), 2) AS Avg_Delivery_Days
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Avg_Delivery_Days DESC;   
-- Vendor business performance
SELECT
    Supplier,
    ROUND(SUM(Total_Spend), 2) AS Total_Spend,
    ROUND(SUM(Savings), 2) AS Total_Savings,
    ROUND(AVG(Defect_Rate), 2) AS Avg_Defect_Rate
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Total_Spend DESC;
-- Vendor quality analysis
SELECT
    Supplier,
    ROUND(AVG(Defect_Rate), 2) AS Avg_Defect_Rate,
    ROUND(AVG(Quality_Rate), 2) AS Avg_Quality_Rate
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Avg_Defect_Rate;  
-- Compliance analysis
SELECT
    Supplier,
    COUNT(*) AS Total_Orders,
    SUM(
        CASE
            WHEN LOWER(Compliance) = 'compliant'
            THEN 1
            ELSE 0
        END
    ) AS Compliant_Orders
FROM vendor_cleaned_kpi  
GROUP BY Supplier;   
-- Create one Vendor Performance Summary
SELECT
    Supplier,

    COUNT(PO_ID) AS Total_Orders,

    ROUND(SUM(Total_Spend), 2) AS Total_Spend,

    ROUND(SUM(Savings), 2) AS Total_Savings,

    ROUND(AVG(Delivery_Days), 2) AS Avg_Delivery_Days,

    ROUND(AVG(Defect_Rate), 2) AS Avg_Defect_Rate,

    ROUND(AVG(Quality_Rate), 2) AS Avg_Quality_Rate,

    ROUND(
        SUM(
            CASE
                WHEN LOWER(Compliance) = 'compliant'
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS Compliance_Rate
FROM vendor_cleaned_kpi
GROUP BY Supplier
ORDER BY Total_Spend DESC;
SELECT @@SERVERNAME AS ServerName;