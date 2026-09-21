import pandas as pd
file_path = r"C:\Users\nithy\Desktop\E-COMMERCE\E-commerce_analysis\Ecommerce_Analysis.xlsx"

products=pd.read_excel(file_path,sheet_name="Products")
order_items=pd.read_excel(file_path,sheet_name="Order_Items")
returns=pd.read_excel(file_path,sheet_name="Returns")
print("All files are loaded successfully")


print("===== PRODUCT SALES ANALYSIS=====")

product_sales=order_items.groupby("Product_ID").agg(
    Total_Quantity_Sold=("Quantity","sum"),
    Total_Revenue=("Net_Amount","sum"),
    Total_Profit=("Profit","sum"),
    Avg_selling_price=("Unit_Price","mean")
).reset_index()

print(product_sales)

print("\n========== PRODUCT DETAILS ==========")

product_analysis = product_sales.merge(
    products[
        [
            "Product_ID",
            "Product_Name",
            "Category",
            "Brand"
        ]
    ],
    on="Product_ID",
    how="left"
)

print("\nProduct Analysis Table:")
print(product_analysis.head(10))




print("\n========== TOP PERFORMING PRODUCTS ==========")

# Top 10 products by revenue
top_10_revenue = (
    product_analysis
    .sort_values(
        by="Total_Revenue",
        ascending=False
    )
    .head(10)
)

print("\nTop 10 Products by Revenue:")
print(
    top_10_revenue[
        [
            "Product_ID",
            "Product_Name",
            "Category",
            "Brand",
            "Total_Quantity_Sold",
            "Total_Revenue",
            "Total_Profit"
        ]
    ]
)


# Top 10 products by profit
top_10_profit = (
    product_analysis
    .sort_values(
        by="Total_Profit",
        ascending=False
    )
    .head(10)
)

print("\nTop 10 Products by Profit:")
print(
    top_10_profit[
        [
            "Product_ID",
            "Product_Name",
            "Category",
            "Brand",
            "Total_Quantity_Sold",
            "Total_Revenue",
            "Total_Profit"
        ]
    ]
)


print("\n========== CATEGORY PERFORMANCE ==========")

category_analysis = (
    product_analysis
    .groupby("Category")
    .agg(
        Total_Quantity_Sold=("Total_Quantity_Sold", "sum"),
        Total_Revenue=("Total_Revenue", "sum"),
        Total_Profit=("Total_Profit", "sum"),
        Average_Selling_Price=("Avg_selling_price", "mean")
    )
    .reset_index()
)

category_analysis = category_analysis.round(2)

print("\nCategory Performance:")
print(category_analysis)


print("\n========== LOW-PERFORMING PRODUCTS ==========")

quantity_25 = product_analysis["Total_Quantity_Sold"].quantile(0.25)
revenue_25 = product_analysis["Total_Revenue"].quantile(0.25)

low_performing_products = product_analysis[
    (product_analysis["Total_Quantity_Sold"] <= quantity_25)
    &
    (product_analysis["Total_Revenue"] <= revenue_25)
].sort_values(
    by="Total_Revenue",
    ascending=True
)

print("\nLow-Performing Products:")

print(
    low_performing_products[
        [
            "Product_ID",
            "Product_Name",
            "Category",
            "Brand",
            "Total_Quantity_Sold",
            "Total_Revenue",
            "Total_Profit"
        ]
    ]
)

print("=====Loss Making Products=====")

loss_making_products=(
    product_analysis[
        product_analysis["Total_Profit"] < 0
    ]
    .sort_values(
        by="Total_Profit",
        ascending=True
    )
)

print(loss_making_products[
      [
            "Product_ID",
            "Product_Name",
            "Category",
            "Brand",
            "Total_Quantity_Sold",
            "Total_Revenue",
            "Total_Profit"
        ]

])
print("\n========== HIGH-RETURN PRODUCTS ==========")

# Get products belonging to returned orders
returned_product_orders = (
    returns[["Order_ID"]]
    .drop_duplicates()
    .merge(
        order_items[["Order_ID", "Product_ID"]],
        on="Order_ID",
        how="left"
    )
)

# Count unique returned orders for each product
high_return_products = (
    returned_product_orders
    .groupby("Product_ID")
    .agg(
        Returned_Orders=("Order_ID", "nunique")
    )
    .reset_index()
)

# Add product details
high_return_products = (
    high_return_products
    .merge(
        products[
            [
                "Product_ID",
                "Product_Name",
                "Category",
                "Brand"
            ]
        ],
        on="Product_ID",
        how="left"
    )
    .sort_values(
        by="Returned_Orders",
        ascending=False
    )
)

print("\nHigh-Return Products:")

print(
    high_return_products[
        [
            "Product_ID",
            "Product_Name",
            "Category",
            "Brand",
            "Returned_Orders"
        ]
    ].head(20)
)

#%%
# ==============================
# STEP 8 — HIGH-DISCOUNT PRODUCTS
# ==============================

print("\n========== HIGH-DISCOUNT PRODUCTS ==========")

high_discount_products = (
    order_items
    .groupby("Product_ID")
    .agg(
        Average_Discount=("Discount_Rate", "mean"),
        Total_Quantity_Sold=("Quantity", "sum"),
        Total_Revenue=("Net_Amount", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .reset_index()
)

# Add product details
high_discount_products = (
    high_discount_products
    .merge(
        products[
            [
                "Product_ID",
                "Product_Name",
                "Category",
                "Brand"
            ]
        ],
        on="Product_ID",
        how="left"
    )
    .sort_values(
        by="Average_Discount",
        ascending=False
    )
)

print("\nHigh-Discount Products:")

print(
    high_discount_products[
        [
            "Product_ID",
            "Product_Name",
            "Category",
            "Brand",
            "Average_Discount",
            "Total_Quantity_Sold",
            "Total_Revenue",
            "Total_Profit"
        ]
    ].head(20)
)

#%%
# ==============================
# STEP 9 — HIGH-REVENUE
#           BUT LOW-MARGIN PRODUCTS
# ==============================

print("\n========== HIGH-REVENUE BUT LOW-MARGIN PRODUCTS ==========")

# Calculate profit margin for each product
product_analysis["Profit_Margin"] = (
    product_analysis["Total_Profit"]
    / product_analysis["Total_Revenue"]
) * 100

# Define thresholds
revenue_75 = product_analysis["Total_Revenue"].quantile(0.75)
margin_25 = product_analysis["Profit_Margin"].quantile(0.25)

# Identify high-revenue but low-margin products
high_revenue_low_margin = product_analysis[
    (product_analysis["Total_Revenue"] >= revenue_75)
    &
    (product_analysis["Profit_Margin"] <= margin_25)
].sort_values(
    by="Total_Revenue",
    ascending=False
)

print("\nHigh-Revenue but Low-Margin Products:")

print(
    high_revenue_low_margin[
        [
            "Product_ID",
            "Product_Name",
            "Category",
            "Brand",
            "Total_Revenue",
            "Total_Profit",
            "Profit_Margin"
        ]
    ].round(2)
)

#%%
# ==============================
# STEP 10 — MANAGEMENT RECOMMENDATIONS
# ==============================

print("\n========== MANAGEMENT RECOMMENDATIONS ==========")

print("""
1. TOP-SELLING PRODUCTS
   - Maintain sufficient inventory for top-selling products.
   - Focus marketing efforts on products with strong sales demand.

2. MOST PROFITABLE PRODUCTS
   - Prioritize products generating high profit.
   - Consider increasing promotions and visibility for these products.

3. LOW-PERFORMING PRODUCTS
   - Review products with low sales and revenue.
   - Consider improving pricing, promotion, or product positioning.
   - Products with consistently weak performance may be candidates for discontinuation.

4. LOSS-MAKING PRODUCTS
   - Investigate the reasons for negative profit.
   - Review pricing, discounts, costs, and margins.
   - Reduce or discontinue products that consistently generate losses.

5. HIGH-RETURN PRODUCTS
   - Investigate the main reasons for product returns.
   - Review product quality, descriptions, packaging, and customer expectations.
   - Take corrective action to reduce return-related costs.

6. HIGH-DISCOUNT PRODUCTS
   - Review whether high discounts are actually increasing sales.
   - Reduce excessive discounts when they significantly affect profitability.
   - Use targeted discounts instead of applying large discounts broadly.

7. HIGH-REVENUE BUT LOW-MARGIN PRODUCTS
   - These products generate strong revenue but relatively low profit margins.
   - Review pricing and discount strategies.
   - Reduce unnecessary costs and improve margins without significantly reducing demand.

8. OVERALL MANAGEMENT FOCUS
   - Invest more in products with strong revenue and profitability.
   - Improve or reposition low-performing products.
   - Closely monitor high-return and high-discount products.
   - Balance revenue growth with profitability.
""")