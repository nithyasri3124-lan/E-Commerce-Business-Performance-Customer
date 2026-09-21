#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# 1. LOAD EXCEL FILE
# =========================================================

file_path = r"C:\Users\nithy\Desktop\E-COMMERCE\E-commerce_analysis\Ecommerce_Analysis.xlsx"

customers = pd.read_excel(file_path, sheet_name="Customers")
products = pd.read_excel(file_path, sheet_name="Products")
orders = pd.read_excel(file_path, sheet_name="Orders")
order_items = pd.read_excel(file_path, sheet_name="Order_Items")
payments = pd.read_excel(file_path, sheet_name="Payments")
marketing = pd.read_excel(file_path, sheet_name="Marketing_Campaigns")
returns = pd.read_excel(file_path, sheet_name="Returns")

print("All files are loaded successfully!")


# =========================================================
#                      TASK -1 ->EDA
# =========================================================

# =========================================================
# 2. CHECK SHAPE
# =========================================================

print("\n========== DATASET SHAPES ==========")

print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Payments:", payments.shape)
print("Marketing Campaigns:", marketing.shape)
print("Returns:", returns.shape)


# =========================================================
# 3. CHECK COLUMN NAMES
# =========================================================

print("\n========== COLUMN NAMES ==========")

for name, df in {
    "Customers": customers,
    "Products": products,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Marketing Campaigns": marketing,
    "Returns": returns
}.items():

    print(f"\n{name}:")
    print(df.columns.tolist())


# =========================================================
# 4. MISSING VALUES
# =========================================================

print("\n========== MISSING VALUES ==========")

for name, df in {
    "Customers": customers,
    "Products": products,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Marketing Campaigns": marketing,
    "Returns": returns
}.items():

    print(f"\n{name} Missing Values:")
    print(df.isnull().sum())


# =========================================================
# 5. CHECK COMPLETELY EMPTY ROWS
# =========================================================

print("\n========== COMPLETELY EMPTY ROWS ==========")

for name, df in {
    "Customers": customers,
    "Products": products,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Marketing Campaigns": marketing,
    "Returns": returns
}.items():

    empty_rows = df.isnull().all(axis=1).sum()

    print(f"{name}: {empty_rows} completely empty rows")


# =========================================================
# 6. REMOVE COMPLETELY EMPTY ROWS FROM ORDER ITEMS
# =========================================================

order_items = order_items.dropna(how="all").copy()

print("\n========== ORDER ITEMS AFTER REMOVING EMPTY ROWS ==========")

print("Order Items shape:", order_items.shape)


# =========================================================
# 7. DUPLICATE COMPLETE ROWS
# =========================================================

print("\n========== DUPLICATE ROWS ==========")

for name, df in {
    "Customers": customers,
    "Products": products,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Marketing Campaigns": marketing,
    "Returns": returns
}.items():

    print(f"{name} duplicate rows:", df.duplicated().sum())


# =========================================================
# 8. DUPLICATE IDs
# =========================================================

print("\n========== DUPLICATE IDs ==========")

print(
    "Customers duplicate IDs:",
    customers["Customer_ID"].duplicated().sum()
)

print(
    "Products duplicate IDs:",
    products["Product_ID"].duplicated().sum()
)

print(
    "Orders duplicate IDs:",
    orders["Order_ID"].duplicated().sum()
)

print(
    "Order Items duplicate IDs:",
    order_items["Order_Item_ID"].duplicated().sum()
)

print(
    "Payments duplicate IDs:",
    payments["Payment_ID"].duplicated().sum()
)

print(
    "Marketing Campaigns duplicate IDs:",
    marketing["Campaign_ID"].duplicated().sum()
)

print(
    "Returns duplicate IDs:",
    returns["Return_ID"].duplicated().sum()
)


# =========================================================
# 9. DATA TYPES
# =========================================================

print("\n========== DATA TYPES ==========")

for name, df in {
    "Customers": customers,
    "Products": products,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Marketing Campaigns": marketing,
    "Returns": returns
}.items():

    print(f"\n{name} Data Types:")
    print(df.dtypes)


# =========================================================
# 10. CUSTOMER KPIs
# =========================================================

print("\n========== CUSTOMER KPIs ==========")

total_customers = customers["Customer_ID"].count()
unique_customers = customers["Customer_ID"].nunique()

print("Total Customers:", total_customers)
print("Unique Customers:", unique_customers)

print("\nCustomers by Gender:")
print(customers["Gender"].value_counts())

print("\nCustomers by Segment:")
print(customers["Customer_Segment"].value_counts())


# =========================================================
# 11. PRODUCT KPIs
# =========================================================

print("\n========== PRODUCT KPIs ==========")

total_products = products["Product_ID"].count()
unique_products = products["Product_ID"].nunique()

print("Total Products:", total_products)
print("Unique Products:", unique_products)

print("\nProducts by Category:")
print(products["Category"].value_counts())

print("\nProducts by Brand:")
print(products["Brand"].value_counts())


print(
    "\nAverage Product Price:",
    products["Unit_Price"].mean()
)

print(
    "Maximum Product Price:",
    products["Unit_Price"].max()
)

print(
    "Minimum Product Price:",
    products["Unit_Price"].min()
)


# =========================================================
# 12. ORDER KPIs
# =========================================================

print("\n========== ORDER KPIs ==========")

total_orders = orders["Order_ID"].count()
unique_orders = orders["Order_ID"].nunique()

total_order_value = orders["Order_Total"].sum()
average_order_value = orders["Order_Total"].mean()

maximum_order = orders["Order_Total"].max()
minimum_order = orders["Order_Total"].min()

print("Total Orders:", total_orders)
print("Unique Orders:", unique_orders)
print("Total Order Value:", total_order_value)
print("Average Order Value:", average_order_value)
print("Maximum Order:", maximum_order)
print("Minimum Order:", minimum_order)


# =========================================================
# 13. ORDERS BY STATUS
# =========================================================

print("\n========== ORDERS BY STATUS ==========")

orders_by_status = orders["Order_Status"].value_counts()

print(orders_by_status)

print("\nOrder Status Percentage:")

status_percentage = (
    orders["Order_Status"]
    .value_counts(normalize=True) * 100
)

print(status_percentage.round(2))




print("\n========== PROFIT KPIs ==========")

total_quantity = order_items["Quantity"].sum()

total_revenue = order_items["Net_Amount"].sum()

total_profit = order_items["Profit"].sum()

average_profit = order_items["Profit"].mean()

profit_margin = (
    total_profit / total_revenue
) * 100

print("Total Quantity Sold:", total_quantity)
print("Total Revenue:", total_revenue)
print("Total Profit:", total_profit)
print("Average Profit per Item:", average_profit)
print(f"Overall Profit Margin: {profit_margin:.2f}%")



print("\n========== CUSTOMER DISTRIBUTION ==========")

print("\nCustomer Distribution by Gender:")
print(customers["Gender"].value_counts())

print("\nCustomer Distribution by Segment:")
print(customers["Customer_Segment"].value_counts())

print("\nCustomer Distribution by City:")
print(customers["City"].value_counts())

print("\nCustomer Distribution by State:")
print(customers["State"].value_counts())

print("\n========== ORDER ITEMS CHECK ==========")

print("First 5 rows:")
print(order_items.head())

print("\nLast 5 rows:")
print(order_items.tail())

print("\nOrder Items final shape:")
print(order_items.shape)

print("--Check Order Date--")
Order_Date = orders["Order_Date"].dtypes
print(Order_Date)

Earliest_Order_Date = orders["Order_Date"].min()
Latest_Order_Date = orders["Order_Date"].max()
print("Earliest Order Date:", Earliest_Order_Date)
print("Latest Order Date:", Latest_Order_Date)

#%%
# ==============================
# TASK 2 — SALES TRENDS
# ==============================

print("\n--Create year and month columns--")
orders = pd.read_excel(
    file_path,
    sheet_name="Orders"
)

print(orders.head())
print(orders.columns)
print(orders["Order_Date"].dtypes)
#%%
orders["Order_Year"]=orders["Order_Date"].dt.year
orders["Order_Month"]=orders["Order_Date"].dt.month
print(orders[
    ["Order_Date","Order_Year","Order_Month"]
].head(10)
)

#%%
print("--Yearly sales Analysis--")
number_Of_Orders=orders.groupby(["Order_Year"])["Order_ID"].count()
print(number_Of_Orders)

yearly_Revenue=orders.groupby(["Order_Year"])["Order_Total"].sum()
print(yearly_Revenue)

Yearly_avg=orders.groupby(["Order_Year"])["Order_Total"].mean()
print(Yearly_avg)

#%%
yearly_sales=orders.groupby("Order_Year").agg(
    Total_Orders=("Order_ID", "count"),
    Total_Revenue=("Order_Total", "sum"),
    Average_Order_Value=("Order_Total", "mean")
).reset_index()

print(yearly_sales)

#%%
print("--Monthly Sales Analysis--")
monthly_sales=orders.groupby(["Order_Year","Order_Month"]).agg(
    Total_Orders=("Order_ID", "count"),
    Total_Revenue=("Order_Total", "sum"),
    Average_Order_Value=("Order_Total", "mean")
).reset_index()
print(monthly_sales)

#%%
monthly_sales=monthly_sales.sort_values(["Order_Year","Order_Month"])
print(monthly_sales)

#%%
highest_revenue_month=monthly_sales.loc[monthly_sales["Total_Revenue"].idxmax()]
lowest_revenue_month=monthly_sales.loc[monthly_sales["Total_Revenue"].idxmin()]
highest_month_order=monthly_sales.loc[monthly_sales["Total_Orders"].idxmax()]
print("Highest Revenue Month:", highest_revenue_month)
print("Lowest Revenue Month:", lowest_revenue_month)
print("Highest Order Month:", highest_month_order)

#%%
monthly_sales = orders.groupby(
    ["Order_Year", "Order_Month"]
).agg(
    Total_Orders=("Order_ID", "count"),
    Total_Revenue=("Order_Total", "sum"),
    Average_Order_Value=("Order_Total", "mean")
).reset_index()

#%%
monthly_sales = monthly_sales.sort_values(
    ["Order_Year", "Order_Month"]
)

print(monthly_sales)

#%%
# ==============================
# TASK 3 — CUSTOMER BEHAVIOR
# ==============================

print("--Customer behaviour--")

print(customers["Age"].head(10))

print("maximum age:",customers["Age"].max())
print("minimum age:",customers["Age"].min())

bins=[0, 18, 25, 35, 45, 55, 65, float("inf")]
labels=["0-17","18-24","25-34","35-44","45-54","55-64","65+"]
customers["Age_Group"]=pd.cut(customers["Age"],bins=bins,labels=labels,right=False)
print(customers[["Age","Age_Group"]].head(10))
print("\nCustomers by Age Group:")
print(customers["Age_Group"].value_counts().sort_index())


#%%
print("--Customer Segmentation--")
segment_count=customers["Customer_Segment"].value_counts()
print(segment_count)

percentage_of_customer_Segment=customers["Customer_Segment"].value_counts(normalize=True)*100
print(percentage_of_customer_Segment.round(2))

print("--Customer Orders and Revenue--")
customer_orders=customers.merge(
    orders,
    on="Customer_ID",
    how="inner"
    )
print(customer_orders)
#%%
customer_revenue=customer_orders.groupby(["Customer_ID","Customer_Name"]).agg(
    Total_Orders=("Order_ID","count"),
    Total_Revenue=("Order_Total","sum"),
    Average_Order_Value=("Order_Total","mean")
).reset_index()
print(customer_revenue)

top_10_customers = customer_revenue.sort_values(
    "Total_Revenue",
    ascending=False
).head(10)

print("\nTop 10 Customers by Revenue:")
print(top_10_customers)

#%%
print("--Customer Gender Analysis--")

gender_analysis = customer_orders.groupby("Gender").agg(
    Total_Customers=("Customer_ID", "nunique"),
    Total_Orders=("Order_ID", "count"),
    Total_Revenue=("Order_Total", "sum"),
    Average_Order_Value=("Order_Total", "mean")
).reset_index()

print("\n--Gender Analysis--")
print(gender_analysis)

#%%
# ==============================
# TASK 4 — PRODUCT PERFORMANCE
# ==============================

print("--Product Performance Analysis--")

product_orders=products.merge(
    order_items,
    on="Product_ID",
    how="left"
).reset_index()

#%%
print(product_orders.head(10))
#print(product_orders.columns.tolist())
product_performance = product_orders.groupby(
    ["Product_ID", "Product_Name", "Category", "Brand"]
).agg(
    Total_Quantity=("Quantity", "sum"),
    Total_Revenue=("Net_Amount", "sum"),
    Total_Profit=("Profit", "sum"),
    Average_Price=("Unit_Price_x", "mean")
).reset_index()

print("\n--Product Performance--")
print(product_performance.head(10))

#%%
print("--Top 10 Products by Quantity Sold--")

Top_10_Products=product_performance.sort_values(
    "Total_Quantity",
    ascending=False
).head(10)

print("\nTop 10 Products by Quantity Sold:")
print(Top_10_Products)


#%%
print("\n--Product Category Performance--")

category_performance = product_performance.groupby(
    "Category"
).agg(
    Total_Products=("Product_ID", "nunique"),
    Total_Quantity=("Total_Quantity", "sum"),
    Total_Revenue=("Total_Revenue", "sum"),
    Total_Profit=("Total_Profit", "sum")
).reset_index()

print(category_performance)
category_performance = category_performance.sort_values(
    "Total_Revenue",
    ascending=False
)

#%%
print("\nCategory Performance by Revenue:")
print(category_performance)
best_category = category_performance.loc[
    category_performance["Total_Revenue"].idxmax()
]

#%%
print("\nBest Category by Revenue:")
print(best_category)
best_profit_category = category_performance.loc[
    category_performance["Total_Profit"].idxmax()
]

print("\nBest Category by Profit:")
print(best_profit_category)



print("--Brand Performance--")

#%%
brand_performance=product_performance.groupby(
    "Brand").agg(
    Total_Products=("Product_ID","nunique"),
    Total_Quantity=("Total_Quantity","sum"),
    Total_Revenue=("Total_Revenue","sum"),
    Total_Profit=("Total_Profit","sum")
    ).reset_index()
print(brand_performance)

top_10_brands=brand_performance.sort_values(
    "Total_Revenue",
    ascending=False
).head(10)

print("\nTop 10 Brands by Revenue:")
print(top_10_brands)


print("--Best brand by Profit--")

#%%
best_brand=brand_performance.loc[
    brand_performance["Total_Profit"].idxmax()
]

print("\n Best Brand by Profit:")
print(best_brand)


#%%
# ==============================
# TASK 5 — RETURN ANALYSIS
# ==============================

print("--Return Analysis--")

returns_analysis=returns.groupby("Return_Reason").agg(
    Total_Returns=("Return_ID","count"),
).reset_index()

print("\nReturn Analysis:")
print(returns_analysis)


#%%
return_products=returns.merge(
    order_items,
    on="Order_ID",
    how="inner"
)
print(return_products.head(10))


#%%
print("--Return Rate Analysis--")
total_orders=orders["Order_ID"].nunique()
total_returns=returns["Return_ID"].nunique()
return_rate=(total_returns/total_orders)*100
print(f"\nReturn Rate: {return_rate:.2f}%")
print("Total_Orders:",total_orders)
print("Total_Returns:",total_returns)

#%%
print("--Returns by product--")
return_products=return_products.merge(
    products,
    on="Product_ID",
    how="inner"
)


#%%
product_returns=return_products.groupby(
    ["Product_ID","Product_Name"]
).agg(
    Total_Returns=("Return_ID","count"),
    Total_Quantity_Returned=("Quantity","sum")
).reset_index()

#%%
product_returns=product_returns.sort_values(
    "Total_Returns",
    ascending=False
)
print("\nReturns by Product:")
print(product_returns.head(10))


#%%
print("\n-- Return Reasons Analysis --")

return_reason_analysis = returns.groupby(
    "Return_Reason"
).agg(
    Total_Returns=("Return_ID", "count"),
    Total_Refund_Amount=("Refund_Amount", "sum")
).reset_index()

#%%
return_reason_analysis = return_reason_analysis.sort_values(
    "Total_Returns",
    ascending=False
)

print(return_reason_analysis)

#%%
# ==============================
# TASK 6 — MARKETING ANALYSIS
# ==============================

print("--Marketing Campaigns Analysis--")
print(marketing.columns.tolist())

#%%
print("--Campaigns Performance--")
campaigns_performance=marketing.groupby(
    ["Campaign_ID","Campaign_Name","Channel"]
).agg(
    Total_Budget=("Budget","sum"),
    Total_Spend=("Spend","sum"),
    TOtal_Impression=("Impressions","sum"),
    Total_Clicks=("Clicks","sum"),
    Total_Conversions=("Conversions","sum"),
    Total_Revenue=("Revenue_Generated","sum")
).reset_index()

print(campaigns_performance)

#%%
campaigns_performance["ROI"] = (
    (campaigns_performance["Total_Revenue"] -
     campaigns_performance["Total_Spend"])
    / campaigns_performance["Total_Spend"]
) * 100

print("\nCampaign Performance with ROI:")
print(campaigns_performance)


#%%
print("--Top 10 Campaigns by Revenue")
top_campaigns=campaigns_performance.sort_values(
    "Total_Revenue",
    ascending=False
)
print(top_campaigns)

#%%
print("--Channel Performance--")

channel_performance=marketing.groupby(
    "Channel"
).agg(
     Total_Campaigns=("Campaign_ID","count"),
     Total_Budget=("Budget","sum"),
     Total_Spend=("Spend","sum"),
     TOtal_Impression=("Impressions","sum"),
     Total_Clicks=("Clicks","sum"),
     Total_Conversions=("Conversions","sum"),
     Total_Revenue=("Revenue_Generated","sum")  
).reset_index()
print(channel_performance.head(10))

channel_performance["ROI"] = (
    (channel_performance["Total_Revenue"] -
     channel_performance["Total_Spend"])
    / channel_performance["Total_Spend"]
) * 100
print(channel_performance)

#%%
print("--Best Channel--")
best_channel=channel_performance.loc[
    channel_performance["ROI"].idxmax()
]

print(best_channel)

print("\n-- Campaign Efficiency --")

#%%
campaign_efficiency = marketing.groupby(
    ["Campaign_ID", "Campaign_Name", "Channel"]
).agg(
    Total_Impressions=("Impressions", "sum"),
    Total_Clicks=("Clicks", "sum"),
    Total_Conversions=("Conversions", "sum")
).reset_index()

campaign_efficiency["CTR"] = (
    campaign_efficiency["Total_Clicks"] /
    campaign_efficiency["Total_Impressions"]
) * 100

campaign_efficiency["Conversion_Rate"] = (
    campaign_efficiency["Total_Conversions"] /
    campaign_efficiency["Total_Clicks"]
) * 100

print(campaign_efficiency.head(10))

print("--Top_ctr_campaigns")
top_ctr_campaigns=campaign_efficiency.sort_values(
    "CTR",
    ascending=False
).head(10)
print(top_ctr_campaigns)
#%%
print("--top_conversion Rate")
top_conversion_campaigns=campaign_efficiency.sort_values(
    "Conversion_Rate",
    ascending=False
).head(10)
print(top_conversion_campaigns)

print("\n-- Customer Acquisition Cost & Marketing ROI --")
#%%
marketing_roi = marketing.groupby("Channel").agg(
    Total_Spend=("Spend", "sum"),
    Total_Conversions=("Conversions", "sum"),
    Total_Revenue=("Revenue_Generated", "sum"),
    Average_CAC=("CUSTOMER ACQUITATION COST", "mean"),
    Average_Marketing_ROI=("MARKETING ROI", "mean")
).reset_index()
#%%
print(marketing_roi)
best_marketing_channel = marketing_roi.loc[
    marketing_roi["Average_Marketing_ROI"].idxmax()
]
#%%
print("\nBest Channel by Marketing ROI:")
print(best_marketing_channel)
lowest_cac_channel = marketing_roi.loc[
    marketing_roi["Average_CAC"].idxmin()
]
#%%
print("\nChannel with Lowest CAC:")
print(lowest_cac_channel)

#%%
# ==============================
# TASK 7 — PAYMENT ANALYSIS
# ==============================

print("--PAYMENT PERFORMANCE--")

payment_performance = payments.groupby(
    "Payment_Method"
).agg(
    Total_Payments=("Payment_ID", "count"),
    Total_Amount=("Payment_Amount", "sum"),
    Average_Payment=("Payment_Amount", "mean")
).reset_index()

print(payment_performance)
print("\n-- Payment Status Analysis --")

payment_status = payments.groupby(
    "Payment_Status"
).agg(
    Total_Payments=("Payment_ID", "count"),
    Total_Amount=("Payment_Amount", "sum")
).reset_index()

print(payment_status)

print("\n-- Payment Success Rate --")

total_payments = payments["Payment_ID"].nunique()

successful_payments = payments[
    payments["Payment_Status"].str.lower() == "completed"
]["Payment_ID"].nunique()

payment_success_rate = (
    successful_payments / total_payments
) * 100

print("Total Payments:", total_payments)
print("Successful Payments:", successful_payments)
print("Payment Success Rate:", payment_success_rate, "%")
#%%
payment_method_status = payments.groupby(
    ["Payment_Method", "Payment_Status"]
).agg(
    Total_Payments=("Payment_ID", "count"),
    Total_Amount=("Payment_Amount", "sum")
).reset_index()

print("\nPayment Method & Status:")
print(payment_method_status)


