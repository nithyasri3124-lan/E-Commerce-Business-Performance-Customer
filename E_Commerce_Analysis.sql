select*from customers_details;
select*from order_items;
select*from orders;
select*from payments;
select*from products;
select*from returns;
select*from marketing_campaigns;
describe orders;
select Customer_ID,Order_Total from orders order by Order_Total desc limit 10;
select Order_Status, SUM(Order_Total) as Total_Revenue from orders group by Order_Status;
select avg(Order_Total)as Avg_order_value from orders;
select count(Order_ID)as Num_of_orders from orders;
SELECT Order_Status,
      sum(Order_Total)  as Total_Revenue from orders
group by Order_Status 
having Sum(Order_Total)>10000000;
Select c.Customer_ID,c.Customer_Name,o.Order_ID from customers_details c Inner join  orders o  on c.Customer_ID=o.Customer_ID;

select c.Customer_ID,c.Customer_Name,o.Order_ID from customers_details c Left Join orders o on C.Customer_ID=o.Customer_ID;

select  Order_ID,Customer_ID,Order_Total from orders where Order_Total > (Select Avg(Order_Total) from orders);

with Customer_Revenue as(
   select  c.Customer_ID ,c.Customer_Name,sum(o.Order_Total) 
   as Total_Revenue from customers_details c 
   inner join orders o on c.Customer_ID= o.Customer_ID
   group by Customer_ID,Customer_Name
   )
   select Customer_ID ,Customer_Name ,Round(Total_Revenue,2)as Total_Revenue from Customer_Revenue
   order by Total_Revenue desc
   limit 10;
   
select Order_ID,Order_Total,
case 
 when Order_Total >=50000 then "High Value"
 when Order_Total >= 20000 then "Medium Value"
 else "Low Value"
 end as Order_category
from orders;

WITH Monthly_Revenue AS (
    SELECT
        DATE_FORMAT(Order_Date, '%Y-%m') AS Month,
        SUM(Order_Total) AS Monthly_Revenue
    FROM Orders
    GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
)
SELECT
    Month,
    Monthly_Revenue,
    LAG(Monthly_Revenue) OVER (
        ORDER BY Month
    ) AS Previous_Month_Revenue
FROM Monthly_Revenue
ORDER BY Month;

SELECT p.Product_ID,
       p.Product_Name,
       SUM(oi.Net_Amount) AS Total_Revenue,
       RANK() OVER (
           ORDER BY SUM(oi.Net_Amount) DESC
       ) AS Product_Rank
FROM Products p
INNER JOIN Order_Items oi
    ON p.Product_ID = oi.Product_ID
GROUP BY p.Product_ID, p.Product_Name
ORDER BY Product_Rank
LIMIT 10;

WITH Monthly_Revenue AS (
    SELECT
        DATE_FORMAT(Order_Date, '%Y-%m') AS Month,
        SUM(Order_Total) AS Monthly_Revenue
    FROM Orders
    GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
)
SELECT
    Month,
    Monthly_Revenue,
    SUM(Monthly_Revenue) OVER (
        ORDER BY Month
    ) AS Running_Revenue
FROM Monthly_Revenue
ORDER BY Month;

WITH Monthly_Revenue AS (
    SELECT
        DATE_FORMAT(Order_Date, '%Y-%m') AS Month,
        SUM(Order_Total) AS Monthly_Revenue
    FROM Orders
    GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
),
MoM_Analysis AS (
    SELECT
        Month,
        Monthly_Revenue,
        LAG(Monthly_Revenue) OVER (
            ORDER BY Month
        ) AS Previous_Month_Revenue
    FROM Monthly_Revenue
)
SELECT
    Month,
    Monthly_Revenue,
    Previous_Month_Revenue,
    ROUND(
        ((Monthly_Revenue - Previous_Month_Revenue)
        / Previous_Month_Revenue) * 100,
        2
    ) AS MoM_Growth_Percent
FROM MoM_Analysis
ORDER BY Month;
SELECT
    c.Customer_ID,
    c.Customer_Name,
    MAX(o.Order_Date) AS Last_Order_Date
FROM customers_details c
LEFT JOIN orders o
    ON c.Customer_ID = o.Customer_ID
GROUP BY
    c.Customer_ID,
    c.Customer_Name
HAVING MAX(o.Order_Date) < (
    SELECT DATE_SUB(MAX(Order_Date), INTERVAL 6 MONTH)
    FROM orders
)
OR MAX(o.Order_Date) IS NULL
ORDER BY Last_Order_Date;

WITH Customer_Orders AS (
    SELECT
        Customer_ID,
        COUNT(Order_ID) AS Order_Count
    FROM Orders
    GROUP BY Customer_ID
)
SELECT
    COUNT(*) AS Total_Customers,
    SUM(CASE WHEN Order_Count > 1 THEN 1 ELSE 0 END) AS Repeat_Customers,
    ROUND(
        SUM(CASE WHEN Order_Count > 1 THEN 1 ELSE 0 END)
        / COUNT(*) * 100,
        2
    ) AS Repeat_Purchase_Rate
FROM Customer_Orders;
SELECT
    p.Product_ID,
    p.Product_Name,
    SUM(oi.Profit) AS Total_Profit
FROM Products p
INNER JOIN Order_Items oi
    ON p.Product_ID = oi.Product_ID
GROUP BY
    p.Product_ID,
    p.Product_Name
ORDER BY Total_Profit DESC
LIMIT 10;

WITH Product_Performance AS (
    SELECT
        p.Product_ID,
        p.Product_Name,
        SUM(oi.Net_Amount) AS Total_Revenue,
        SUM(oi.Profit) AS Total_Profit,
        ROUND(
            SUM(oi.Profit) / SUM(oi.Net_Amount) * 100,
            2
        ) AS Profit_Margin
    FROM Products p
    INNER JOIN Order_Items oi
        ON p.Product_ID = oi.Product_ID
    GROUP BY
        p.Product_ID,
        p.Product_Name
)
SELECT *
FROM Product_Performance
WHERE Total_Revenue > (
    SELECT AVG(Total_Revenue)
    FROM Product_Performance
)
AND Profit_Margin < 20
ORDER BY Total_Revenue DESC;
SELECT
    p.Product_ID,
    p.Product_Name,
    SUM(oi.Net_Amount) AS Total_Revenue
FROM Products p
INNER JOIN Order_Items oi
    ON p.Product_ID = oi.Product_ID
GROUP BY
    p.Product_ID,
    p.Product_Name
ORDER BY Total_Revenue DESC
LIMIT 10;

select Round(sum(Order_Total),2)as Total_Revenue from orders;
select round(sum(Profit),2) as Total_Profit from order_items;
select round(sum(Profit)/sum(Net_Amount) *100,2) as Overall_Profit_Margin from order_items;
SELECT
    p.Category,
    ROUND(SUM(oi.Net_Amount), 2) AS Total_Revenue,
    ROUND(SUM(oi.Profit), 2) AS Total_Profit,
    ROUND(
        SUM(oi.Profit) / SUM(oi.Net_Amount) * 100,
        2
    ) AS Profit_Margin
FROM Products p
INNER JOIN Order_Items oi
    ON p.Product_ID = oi.Product_ID
GROUP BY p.Category
ORDER BY Total_Profit ASC;

SELECT
    c.State AS Region,
    ROUND(SUM(o.Order_Total), 2) AS Total_Revenue
FROM customers_details c
INNER JOIN Orders o
    ON c.Customer_ID = o.Customer_ID
GROUP BY c.State
ORDER BY Total_Revenue DESC;

