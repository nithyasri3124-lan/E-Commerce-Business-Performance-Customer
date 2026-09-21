import matplotlib.pyplot as plt
from e_commerce_analysis import yearly_sales,monthly_sales,gender_analysis,customers,top_10_customers,Top_10_Products,category_performance,marketing


# =========================================================
#                         CHARTS
# =========================================================
#%%
# CHART -1 -> YEARLY REVENUE


plt.figure(figsize=(8,5))

plt.bar(
    yearly_sales["Order_Year"],
    yearly_sales["Total_Revenue"]
)

plt.title("Yearly Revenue")
plt.xlabel("Year")
plt.ylabel("Total revenue")
plt.show()

#%%
#CHART-2 --> MONTHLY REVENUE TREND
plt.figure(figsize=(10,5))

for year in monthly_sales["Order_Year"].unique():

    data=monthly_sales[
        monthly_sales["Order_Year"] == year
    ]

    plt.plot(
        data["Order_Month"],
        data["Total_Revenue"],
        marker="o",
        label=str(year)
    )
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue")

plt.xticks(range(1, 13))
plt.legend(title="Year")

plt.show()   

#%%
# CHART 3 -> CUSTOMER DISTRIBUTION BY GENDER

plt.figure(figsize=(8,5))

plt.bar(
    gender_analysis["Gender"],
    gender_analysis["Total_Customers"]
)

plt.title("Customer Distribution by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Customers")

plt.show()

#%%
# CHART 4 -> CUSTOMER DISTRIBUTION BY SEGMENT

segment_counts = customers["Customer_Segment"].value_counts()

plt.figure(figsize=(7,7))

plt.pie(
    segment_counts.values,
    labels=segment_counts.index,
    autopct="%1.1f%%"
)

plt.title("Customer Distribution by Segment")

plt.show()

#%%
#CHART-5 -->Age Groups

age_group_counts=customers["Age_Group"].value_counts().sort_index()
plt.figure(figsize=(9,5))
plt.bar(
    age_group_counts.index,
    age_group_counts.values
)

plt.title("cutomers by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Customers")
plt.show()


#%%
# CHART 6 -> REVENUE BY GENDER

plt.figure(figsize=(8,5))

plt.bar(
    gender_analysis["Gender"],
    gender_analysis["Total_Revenue"]
)

plt.title("Revenue by Gender")
plt.xlabel("Gender")
plt.ylabel("Total Revenue")

plt.show()

#%%
# CHART 7 -> TOP 10 CUSTOMERS BY REVENUE
plt.figure(figsize=(10,6))

plt.barh(
    top_10_customers["Customer_Name"],
    top_10_customers["Total_Revenue"]
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Total Revenue")
plt.ylabel("Customer Name")

plt.gca().invert_yaxis()

plt.show()


#%%
# CHART 8 -> TOP 10 PRODUCTS BY REVENUE
plt.figure(figsize=(10,6))

plt.barh(
    Top_10_Products["Product_Name"],
    Top_10_Products["Total_Revenue"]
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Total Revenue")
plt.ylabel("Product Name")

plt.gca().invert_yaxis()

plt.show()


#%%
# CHART 9 -> REVENUE BY PRODUCT CATEGORY


plt.figure(figsize=(9,5))

plt.bar(
    category_performance["Category"],
    category_performance["Total_Revenue"]
)

plt.title("Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Revenue")

plt.xticks(rotation=45)

plt.show()


#%%
# CHART 10 -> MARKETING SPEND VS REVENUE

plt.figure(figsize=(9,6))

plt.scatter(
    marketing["Spend"],
    marketing["Revenue_Generated"]
)

plt.title("Marketing Spend vs Revenue Generated")
plt.xlabel("Marketing Spend")
plt.ylabel("Revenue Generated")

plt.show()


