import pandas as pd
import numpy as np
from scipy import stats

file_path = r"C:\Users\nithy\Desktop\E-COMMERCE\E-commerce_analysis\Ecommerce_Analysis.xlsx"

orders = pd.read_excel(
    file_path,
    sheet_name="Orders"
)

marketing = pd.read_excel(
    file_path,
    sheet_name="Marketing_Campaigns"
)

print("Data loaded successfully!")

# PART 4 — STATISTICAL ANALYSIS
# ==============================

print("\n========== STATISTICAL ANALYSIS ==========")

order_mean = orders["Order_Total"].mean()
order_median = orders["Order_Total"].median()
order_std = orders["Order_Total"].std()

print("Mean Order Value:", order_mean)
print("Median Order Value:", order_median)
print("Standard Deviation:", order_std)


print("=========CORRELATION ANALYSIS=========")

marketing_correlation=marketing[
    ["Spend","Revenue_Generated"]
].corr()
print(marketing_correlation)


click_conversion_correlation=marketing[
    ["Clicks","Conversions"]
].corr()
print(click_conversion_correlation)


#%%
# ==============================
# STEP 3 — CONFIDENCE INTERVAL
# ==============================

print("\n========== CONFIDENCE INTERVAL ==========")

# 95% Confidence Interval for Average Order Value

order_values = orders["Order_Total"].dropna()

confidence_level = 0.95

confidence_interval = stats.t.interval(
    confidence_level,
    df=len(order_values) - 1,
    loc=order_values.mean(),
    scale=stats.sem(order_values)
)

print("95% Confidence Interval for Mean Order Value:")
print("Lower Limit:", confidence_interval[0].round(2))
print("Upper Limit:", confidence_interval[1].round(2))



#%%
# ==============================
# STEP 4 — HYPOTHESIS TESTING
# ==============================

marketing["Start_Date"] = pd.to_datetime(marketing["Start_Date"])
marketing = marketing.sort_values("Start_Date")

new = marketing.iloc[-1]
old = marketing.iloc[:-1]

new_rate = new["Conversions"] / new["Clicks"]
old_rate = old["Conversions"].sum() / old["Clicks"].sum()

z = (new_rate - old_rate) / np.sqrt(
    new_rate * (1 - new_rate) / new["Clicks"] +
    old_rate * (1 - old_rate) / old["Clicks"].sum()
)

p = 1 - stats.norm.cdf(z)

print("\n========== HYPOTHESIS TESTING ==========")
print("New Campaign:", new["Campaign_Name"])
print("New Conversion Rate:", new_rate * 100, "%")
print("Previous Conversion Rate:", old_rate * 100, "%")
print("Significance Level: 0.05")
print("Z-Score:", z)
print("P-Value:", p)

if p < 0.05:
    print("Result: Significant improvement")
else:
    print("Result: No significant improvement")