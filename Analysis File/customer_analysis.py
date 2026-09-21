import pandas as pd

#%%
# ==============================
# DATA LOADING
# ==============================

file_path = r"C:\Users\nithy\Desktop\E-COMMERCE\E-commerce_analysis\Ecommerce_Analysis.xlsx"

customers = pd.read_excel(
    file_path,
    sheet_name="Customers"
)

orders = pd.read_excel(
    file_path,
    sheet_name="Orders"
)

print("Data loaded successfully!")


#%%
# ==============================
# STEP 1 — CUSTOMER SPENDING
# ==============================

print("\n======== CUSTOMER SPENDING ANALYSIS ========")

customer_spending = (
    orders.groupby("Customer_ID")["Order_Total"]
    .sum()
    .reset_index()
)

customer_spending = customer_spending.rename(
    columns={
        "Order_Total": "Total_Spending"
    }
)

print(customer_spending.head(10))


#%%
# ==============================
# STEP 2 — NUMBER OF ORDERS
#           & AVERAGE ORDER VALUE
# ==============================

print("\n======= NUMBER OF ORDERS & AVERAGE ORDER VALUE =======")

customer_orders = (
    orders.groupby("Customer_ID")
    .agg(
        No_of_Orders=("Order_ID", "count"),
        Order_Avg_Value=("Order_Total", "mean")
    )
    .reset_index()
)

print(customer_orders.head(10))


#%%
# ==============================
# STEP 3 — PURCHASE FREQUENCY
#           & RECENCY
# ==============================

print("\n======= PURCHASE FREQUENCY & RECENCY =======")

orders["Order_Date"] = pd.to_datetime(
    orders["Order_Date"]
)

# Latest order date in the dataset
reference_date = orders["Order_Date"].max()

customer_behavior = (
    orders.groupby("Customer_ID")
    .agg(
        purchase_frequency=("Order_ID", "count"),
        Last_Order_Date=("Order_Date", "max")
    )
    .reset_index()
)

# Calculate number of days since last purchase
customer_behavior["Recency"] = (
    reference_date
    - customer_behavior["Last_Order_Date"]
).dt.days

print(customer_behavior.head(10))


#%%
# ==============================
# STEP 4 — CUSTOMER LIFETIME VALUE
# ==============================

print("\n======= CUSTOMER LIFETIME VALUE =======")

customer_analysis = (
    customer_spending
    .merge(
        customer_orders,
        on="Customer_ID",
        how="left"
    )
    .merge(
        customer_behavior,
        on="Customer_ID",
        how="left"
    )
)

# Historical customer value
customer_analysis["Customer_Lifetime_Value"] = (
    customer_analysis["Total_Spending"]
)

print("\n========== CUSTOMER ANALYSIS TABLE ==========")

print(customer_analysis.head(10))


#%%
# ==============================
# STEP 5 — CUSTOMER SEGMENTATION
# ==============================

print("\n======= CUSTOMER SEGMENTATION ========")

# Spending thresholds
spending_25 = (
    customer_analysis["Total_Spending"]
    .quantile(0.25)
)

spending_75 = (
    customer_analysis["Total_Spending"]
    .quantile(0.75)
)

# Order and AOV thresholds
orders_75 = (
    customer_analysis["No_of_Orders"]
    .quantile(0.75)
)

aov_75 = (
    customer_analysis["Order_Avg_Value"]
    .quantile(0.75)
)

# Recency thresholds
recency_75 = (
    customer_analysis["Recency"]
    .quantile(0.75)
)

recency_90 = (
    customer_analysis["Recency"]
    .quantile(0.90)
)


def Customer_Segment(row):

    # Inactive Customers
    if row["Recency"] > recency_90:
        return "Inactive Customers"

    # At-Risk Customers
    elif row["Recency"] > recency_75:
        return "At-Risk Customers"

    # VIP Customers
    elif (
        row["Total_Spending"] >= spending_75
        and row["No_of_Orders"] >= orders_75
    ):
        return "VIP Customers"

    # High-Value Customers
    elif (
        row["Total_Spending"] >= spending_75
        or row["Order_Avg_Value"] >= aov_75
    ):
        return "High-Value Customers"

    # Low-Value Customers
    elif row["Total_Spending"] < spending_25:
        return "Low-Value Customers"

    # Regular Customers
    else:
        return "Regular Customers"


# Apply segmentation
customer_analysis["Customer_Segment"] = (
    customer_analysis.apply(
        Customer_Segment,
        axis=1
    )
)

print("\n========== CUSTOMER SEGMENTS ==========")

print(
    customer_analysis[
        [
            "Customer_ID",
            "Total_Spending",
            "No_of_Orders",
            "Order_Avg_Value",
            "purchase_frequency",
            "Recency",
            "Customer_Lifetime_Value",
            "Customer_Segment"
        ]
    ].head(20)
)


#%%
# ==============================
# STEP 6 — SEGMENT CHARACTERISTICS
# ==============================

print("\n======= SEGMENT CHARACTERISTICS ========")

segment_analysis = (
    customer_analysis
    .groupby("Customer_Segment")
    .agg(
        Number_of_Customers=("Customer_ID", "count"),
        Total_Spending=("Total_Spending", "sum"),
        Average_Spending=("Total_Spending", "mean"),
        Average_Orders=("No_of_Orders", "mean"),
        Average_Order_Value=("Order_Avg_Value", "mean"),
        Average_Purchase_Frequency=(
            "purchase_frequency",
            "mean"
        ),
        Average_Recency=("Recency", "mean"),
        Average_Lifetime_Value=(
            "Customer_Lifetime_Value",
            "mean"
        )
    )
    .reset_index()
)

segment_analysis = segment_analysis.round(2)

print("\n========== SEGMENT CHARACTERISTICS ==========")

print(segment_analysis)


#%%
# ==============================
# SEGMENT CUSTOMER COUNT
# ==============================

print("\n======= CUSTOMER COUNT BY SEGMENT ========")

segment_count = (
    customer_analysis["Customer_Segment"]
    .value_counts()
)

print(segment_count)