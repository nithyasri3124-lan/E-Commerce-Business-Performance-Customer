import pandas as pd

file_path=file_path = r"C:\Users\nithy\Desktop\E-COMMERCE\E-commerce_analysis\Ecommerce_Analysis.xlsx"
marketing=pd.read_excel(file_path, sheet_name="Marketing_Campaigns")
print("Marketing file successfully loaded")


print(marketing.columns)
print(marketing.head())

#%%
# ==============================
# STEP 2 — MARKETING METRICS
# ==============================

print("\n========== MARKETING METRICS ==========")

marketing_analysis = marketing.copy()

# Impressions
marketing_analysis["Impressions"] = marketing_analysis["Impressions"]

# Click-Through Rate
marketing_analysis["CTR_Calculated"] = (
    marketing_analysis["Clicks"]
    / marketing_analysis["Impressions"]
)

# Conversion Rate
marketing_analysis["Conversion_Rate_Calculated"] = (
    marketing_analysis["Conversions"]
    / marketing_analysis["Clicks"]
)

# Customer Acquisition Cost
marketing_analysis["CAC_Calculated"] = (
    marketing_analysis["Spend"]
    / marketing_analysis["Conversions"]
)

# Revenue Generated
marketing_analysis["Revenue_Generated"] = (
    marketing_analysis["Revenue_Generated"]
)

# Marketing ROI
marketing_analysis["Marketing_ROI_Calculated"] = (
    (
        marketing_analysis["Revenue_Generated"]
        - marketing_analysis["Spend"]
    )
    / marketing_analysis["Spend"]
)

print("\nMarketing Analysis:")

print(
    marketing_analysis[
        [
            "Campaign_ID",
            "Campaign_Name",
            "Channel",
            "Impressions",
            "Clicks",
            "Conversions",
            "CTR_Calculated",
            "Conversion_Rate_Calculated",
            "CAC_Calculated",
            "Revenue_Generated",
            "Marketing_ROI_Calculated"
        ]
    ].head(10)
)

print("\n========== MARKETING CHANNEL COMPARISON ==========")

channel_analysis = (
    marketing_analysis
    .groupby("Channel")
    .agg(
        Total_Impressions=("Impressions", "sum"),
        Total_Clicks=("Clicks", "sum"),
        Total_Conversions=("Conversions", "sum"),
        Total_Spend=("Spend", "sum"),
        Total_Revenue=("Revenue_Generated", "sum")
    )
    .reset_index()
)

# Calculate channel-level CTR
channel_analysis["CTR"] = (
    channel_analysis["Total_Clicks"]
    / channel_analysis["Total_Impressions"]
)

# Calculate channel-level Conversion Rate
channel_analysis["Conversion_Rate"] = (
    channel_analysis["Total_Conversions"]
    / channel_analysis["Total_Clicks"]
)

# Calculate channel-level Customer Acquisition Cost
channel_analysis["Customer_Acquisition_Cost"] = (
    channel_analysis["Total_Spend"]
    / channel_analysis["Total_Conversions"]
)

# Calculate channel-level Marketing ROI
channel_analysis["Marketing_ROI"] = (
    (
        channel_analysis["Total_Revenue"]
        - channel_analysis["Total_Spend"]
    )
    / channel_analysis["Total_Spend"]
)

channel_analysis = channel_analysis.round(4)

print("\nChannel Analysis:")

print(channel_analysis)

print("\n========== BEST ROI CHANNEL ==========")

best_roi_channel = channel_analysis.loc[
    channel_analysis["Marketing_ROI"].idxmax()
]

print("\nBest Marketing Channel by ROI:")
print("Channel:", best_roi_channel["Channel"])
print("Marketing ROI:", round(best_roi_channel["Marketing_ROI"], 4))
print(
    "Marketing ROI (%):",
    round(best_roi_channel["Marketing_ROI"] * 100, 2),
    "%"
)

print("\nConclusion:")
print(
    f"{best_roi_channel['Channel']} provides the best return on investment."
)

#%%
# ==============================
# STEP 5 — MARKETING RECOMMENDATION
# ==============================

print("\n========== MARKETING RECOMMENDATION ==========")

print(
    f"1. {best_roi_channel['Channel']} provides the best return on investment "
    f"with an ROI of {best_roi_channel['Marketing_ROI'] * 100:.2f}%."
)

print(
    "2. The company should focus more marketing budget on the channel "
    "with the highest ROI."
)

print(
    "3. Channels with lower ROI should be reviewed and optimized "
    "before increasing their budget."
)

print(
    "4. Marketing performance should be monitored using CTR, "
    "Conversion Rate, CAC, Revenue Generated, and ROI."
)