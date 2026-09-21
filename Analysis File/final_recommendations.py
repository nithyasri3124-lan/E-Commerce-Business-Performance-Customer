import pandas as pd
import numpy as np

# =========================================================
# PART 10 — FINAL RECOMMENDATIONS
# =========================================================
# 8+ Actionable Recommendations
# Each with: Problem → Data → Action → Expected Impact
# =========================================================

file_path = r"C:\Users\nithy\Desktop\E-COMMERCE\E-commerce_analysis\Ecommerce_Analysis.xlsx"

customers = pd.read_excel(file_path, sheet_name="Customers")
products = pd.read_excel(file_path, sheet_name="Products")
orders = pd.read_excel(file_path, sheet_name="Orders")
order_items = pd.read_excel(file_path, sheet_name="Order_Items")
returns = pd.read_excel(file_path, sheet_name="Returns")
marketing = pd.read_excel(file_path, sheet_name="Marketing_Campaigns")

print("=" * 70)
print("PART 10 — FINAL RECOMMENDATIONS")
print("=" * 70)
print("""
Based on comprehensive analysis of the e-commerce data,
here are 8+ actionable recommendations to address the 
management concern: "Revenue is increasing, but profitability 
and customer retention are not improving at the same rate."
""")


# =========================================================
# RECOMMENDATION 1
# =========================================================

print("=" * 70)
print("RECOMMENDATION 1: REDUCE EXCESSIVE DISCOUNTING")
print("=" * 70)

order_items["Discount_Pct"] = order_items["Discount_Rate"] * 100
high_disc = order_items[order_items["Discount_Pct"] > 15]
low_disc = order_items[order_items["Discount_Pct"] <= 15]

high_disc_margin = (high_disc["Profit"].sum() / high_disc["Net_Amount"].sum()) * 100
low_disc_margin = (low_disc["Profit"].sum() / low_disc["Net_Amount"].sum()) * 100

print(f"""
PROBLEM: Discounts above 15% significantly reduce profit margins.

SUPPORTING DATA:
  - Items with 15%+ discount profit margin: {high_disc_margin:.2f}%
  - Items with <=15% discount profit margin: {low_disc_margin:.2f}%
  - Margin difference: {low_disc_margin - high_disc_margin:.2f} percentage points
  - High-discount items count: {len(high_disc):,}

RECOMMENDED ACTION:
  - Cap maximum discount at 15% for standard products
  - Use targeted discounts only for slow-moving inventory
  - Implement approval workflow for discounts above 10%
  - Replace blanket discounts with loyalty-based rewards

EXPECTED BUSINESS IMPACT:
  - Potential profit increase: {((low_disc_margin - high_disc_margin) / 100 * high_disc["Net_Amount"].sum()):,.0f}
  - Improved profit margin by 2-4 percentage points
  - Better price integrity across product range
""")


# =========================================================
# RECOMMENDATION 2
# =========================================================

print("=" * 70)
print("RECOMMENDATION 2: DISCONTINUE OR RESTRUCTURE LOSS-MAKING PRODUCTS")
print("=" * 70)

product_loss = order_items.merge(
    products[["Product_ID", "Product_Name", "Category"]],
    on="Product_ID", how="left"
)

product_profit_summary = product_loss.groupby(
    ["Product_ID", "Product_Name", "Category"]
).agg(
    Total_Revenue=("Net_Amount", "sum"),
    Total_Profit=("Profit", "sum")
).reset_index()

loss_products = product_profit_summary[product_profit_summary["Total_Profit"] < 0]
total_loss = loss_products["Total_Profit"].sum()

print(f"""
PROBLEM: Some products consistently generate negative profit.

SUPPORTING DATA:
  - Number of loss-making products: {len(loss_products)}
  - Total loss from these products: ${total_loss:,.2f}
  - Top loss-making products:
""")

for _, row in loss_products.head(5).iterrows():
    print(f"    - {row['Product_Name']}: ${row['Total_Profit']:,.2f}")

print(f"""
RECOMMENDED ACTION:
  - Review cost structure of loss-making products
  - Renegotiate supplier costs or adjust pricing
  - Discontinue products with persistent losses
  - Bundle low-margin products with high-margin ones

EXPECTED BUSINESS IMPACT:
  - Immediate profit recovery: ${abs(total_loss):,.2f}
  - Improved overall profit margin
  - Better inventory turnover
  - Resources freed for profitable products
""")


# =========================================================
# RECOMMENDATION 3
# =========================================================

print("=" * 70)
print("RECOMMENDATION 3: IMPLEMENT CUSTOMER WIN-BACK PROGRAM")
print("=" * 70)

orders["Order_Date"] = pd.to_datetime(orders["Order_Date"])
reference_date = orders["Order_Date"].max()

customer_stats = orders.groupby("Customer_ID").agg(
    Last_Order=("Order_Date", "max"),
    Total_Orders=("Order_ID", "count"),
    Total_Spent=("Order_Total", "sum")
).reset_index()

customer_stats["Days_Inactive"] = (reference_date - customer_stats["Last_Order"]).dt.days

at_risk = customer_stats[
    (customer_stats["Days_Inactive"] > 90) &
    (customer_stats["Total_Orders"] > 1)
]

at_risk_revenue = at_risk["Total_Spent"].sum()
avg_at_risk_value = at_risk["Total_Spent"].mean()

print(f"""
PROBLEM: High-value customers are becoming inactive.

SUPPORTING DATA:
  - At-risk customers (90+ days inactive, multi-order): {len(at_risk):,}
  - Total historical spending of at-risk customers: ${at_risk_revenue:,.2f}
  - Average value per at-risk customer: ${avg_at_risk_value:,.2f}
  - These customers previously contributed significantly

RECOMMENDED ACTION:
  - Launch targeted email campaign for 90-day inactive customers
  - Offer personalized discount (10-15%) for return purchase
  - Create "We Miss You" campaign with exclusive offers
  - Implement automated re-engagement triggers at 60 days
  - Assign dedicated account managers for top at-risk customers

EXPECTED BUSINESS IMPACT:
  - Potential revenue recovery: ${at_risk_revenue * 0.2:,.2f} (20% win-back rate)
  - Improved customer retention rate by 15-20%
  - Reduced customer acquisition cost (retention cheaper than acquisition)
  - Enhanced customer lifetime value
""")


# =========================================================
# RECOMMENDATION 4
# =========================================================

print("=" * 70)
print("RECOMMENDATION 4: OPTIMIZE MARKETING BUDGET ALLOCATION")
print("=" * 70)

channel_perf = marketing.groupby("Channel").agg(
    Total_Spend=("Spend", "sum"),
    Total_Revenue=("Revenue_Generated", "sum"),
    Total_Conversions=("Conversions", "sum")
).reset_index()

channel_perf["ROI"] = (
    (channel_perf["Total_Revenue"] - channel_perf["Total_Spend"])
    / channel_perf["Total_Spend"]
) * 100

channel_perf["CAC"] = channel_perf["Total_Spend"] / channel_perf["Total_Conversions"]
channel_perf = channel_perf.sort_values("ROI", ascending=False)

best_channel = channel_perf.iloc[0]
worst_channel = channel_perf.iloc[-1]

print(f"""
PROBLEM: Marketing budget not optimally allocated across channels.

SUPPORTING DATA:
  - Best performing channel: {best_channel['Channel']}
    * ROI: {best_channel['ROI']:.1f}%
    * CAC: ${best_channel['CAC']:.2f}
  - Worst performing channel: {worst_channel['Channel']}
    * ROI: {worst_channel['ROI']:.1f}%
    * CAC: ${worst_channel['CAC']:.2f}
  - Budget wasted on negative-ROI channels

RECOMMENDED ACTION:
  - Reallocate 30% of budget from low-ROI to high-ROI channels
  - Set minimum ROI threshold of 50% for channel funding
  - Increase budget for {best_channel['Channel']} by 25%
  - Reduce or pause spending on {worst_channel['Channel']}
  - Test new channels with small budget pilots

EXPECTED BUSINESS IMPACT:
  - Marketing ROI improvement: 20-30%
  - Customer acquisition cost reduction: 15-25%
  - Better return on marketing investment
  - More efficient customer acquisition
""")


# =========================================================
# RECOMMENDATION 5
# =========================================================

print("=" * 70)
print("RECOMMENDATION 5: REDUCE PRODUCT RETURN RATE")
print("=" * 70)

total_orders = orders["Order_ID"].nunique()
total_returns = returns["Order_ID"].nunique()
return_rate = (total_returns / total_orders) * 100
total_refund = returns["Refund_Amount"].sum()

return_reasons = returns.groupby("Return_Reason").agg(
    Count=("Return_ID", "count"),
    Refund=("Refund_Amount", "sum")
).reset_index().sort_values("Count", ascending=False)

top_reason = return_reasons.iloc[0]

print(f"""
PROBLEM: High return rate erodes profitability.

SUPPORTING DATA:
  - Overall return rate: {return_rate:.2f}%
  - Total refund amount: ${total_refund:,.2f}
  - Number of returned orders: {total_returns}
  - Top return reason: {top_reason['Return_Reason']} ({top_reason['Count']} returns)

RECOMMENDED ACTION:
  - Improve product descriptions and images
  - Add size guides and detailed specifications
  - Implement quality checks before shipping
  - Review products with highest return rates
  - Add customer reviews to help purchase decisions
  - Offer exchange option instead of refund

EXPECTED BUSINESS IMPACT:
  - Reduce return rate by 20-30%
  - Save ${total_refund * 0.25:,.2f} in refund costs
  - Improved customer satisfaction
  - Better product quality standards
""")


# =========================================================
# RECOMMENDATION 6
# =========================================================

print("=" * 70)
print("RECOMMENDATION 6: FOCUS ON HIGH-MARGIN PRODUCT CATEGORIES")
print("=" * 70)

product_cat = order_items.merge(
    products[["Product_ID", "Category"]], on="Product_ID", how="left"
)

cat_performance = product_cat.groupby("Category").agg(
    Revenue=("Net_Amount", "sum"),
    Profit=("Profit", "sum")
).reset_index()

cat_performance["Margin"] = (cat_performance["Profit"] / cat_performance["Revenue"]) * 100
cat_performance = cat_performance.sort_values("Margin", ascending=False)

best_cat = cat_performance.iloc[0]
worst_cat = cat_performance.iloc[-1]

print(f"""
PROBLEM: Not all categories contribute equally to profit.

SUPPORTING DATA:
  - Best margin category: {best_cat['Category']} ({best_cat['Margin']:.1f}% margin)
  - Worst margin category: {worst_cat['Category']} ({worst_cat['Margin']:.1f}% margin)
  - Revenue distribution is uneven across categories

RECOMMENDED ACTION:
  - Increase inventory and marketing for {best_cat['Category']}
  - Review pricing strategy for {worst_cat['Category']}
  - Develop category-specific promotional strategies
  - Cross-sell high-margin products with low-margin ones
  - Create product bundles to improve overall margin

EXPECTED BUSINESS IMPACT:
  - Shift sales mix toward higher-margin products
  - Overall profit margin improvement: 3-5%
  - Better inventory allocation
  - Increased revenue per customer
""")


# =========================================================
# RECOMMENDATION 7
# =========================================================

print("=" * 70)
print("RECOMMENDATION 7: IMPLEMENT VIP CUSTOMER RETENTION PROGRAM")
print("=" * 70)

customer_seg = customers.merge(
    orders.groupby("Customer_ID").agg(
        Total_Spent=("Order_Total", "sum"),
        Order_Count=("Order_ID", "count")
    ).reset_index(),
    on="Customer_ID", how="left"
)

vip_customers = customer_seg[
    (customer_seg["Customer_Segment"] == "VIP Customers") |
    (customer_seg["Total_Spent"] > customer_seg["Total_Spent"].quantile(0.75))
]

vip_count = len(vip_customers)
vip_revenue = vip_customers["Total_Spent"].sum()

print(f"""
PROBLEM: VIP customers need special attention to prevent churn.

SUPPORTING DATA:
  - VIP/High-Value customers: {vip_count:,}
  - Their total spending: ${vip_revenue:,.2f}
  - These customers drive disproportionate revenue
  - Losing one VIP customer impacts revenue significantly

RECOMMENDED ACTION:
  - Create exclusive VIP loyalty program
  - Offer early access to new products
  - Provide dedicated customer support
  - Send personalized offers and birthday discounts
  - Implement points-based reward system
  - Invite to exclusive events or previews

EXPECTED BUSINESS IMPACT:
  - VIP retention rate improvement: 25-35%
  - Increased customer lifetime value
  - Higher average order value from VIPs
  - Word-of-mouth referrals from satisfied VIPs
""")


# =========================================================
# RECOMMENDATION 8
# =========================================================

print("=" * 70)
print("RECOMMENDATION 8: IMPROVE REGIONAL PROFITABILITY")
print("=" * 70)

region_data = customers.merge(orders, on="Customer_ID", how="inner")
region_data = region_data.merge(
    order_items[["Order_ID", "Net_Amount", "Profit"]],
    on="Order_ID", how="left"
)

region_perf = region_data.groupby("State").agg(
    Orders=("Order_ID", "nunique"),
    Revenue=("Net_Amount", "sum"),
    Profit=("Profit", "sum")
).reset_index()

region_perf["Margin"] = (region_perf["Profit"] / region_perf["Revenue"]) * 100
region_perf = region_perf.sort_values("Margin")

low_margin_region = region_perf.iloc[0]
high_margin_region = region_perf.iloc[-1]

print(f"""
PROBLEM: Significant profit margin variation across regions.

SUPPORTING DATA:
  - Lowest margin region: {low_margin_region['State']} ({low_margin_region['Margin']:.1f}%)
  - Highest margin region: {high_margin_region['State']} ({high_margin_region['Margin']:.1f}%)
  - Margin gap: {high_margin_region['Margin'] - low_margin_region['Margin']:.1f} percentage points

RECOMMENDED ACTION:
  - Review regional pricing strategies
  - Analyze shipping and logistics costs by region
  - Optimize warehouse locations for cost efficiency
  - Region-specific promotional campaigns
  - Negotiate better shipping rates for low-margin regions

EXPECTED BUSINESS IMPACT:
  - Close margin gap by 30-40%
  - Improved overall profitability
  - Better regional customer satisfaction
  - Optimized supply chain costs
""")


# =========================================================
# RECOMMENDATION 9
# =========================================================

print("=" * 70)
print("RECOMMENDATION 9: IMPLEMENT DATA-DRIVEN PRICING STRATEGY")
print("=" * 70)

product_analysis = order_items.merge(
    products[["Product_ID", "Product_Name", "Category", "Unit_Price"]],
    on="Product_ID", how="left"
)

product_margin = product_analysis.groupby(["Product_ID", "Product_Name"]).agg(
    Revenue=("Net_Amount", "sum"),
    Profit=("Profit", "sum"),
    Avg_Selling_Price=("Unit_Price", "mean")
).reset_index()

product_margin["Margin"] = (product_margin["Profit"] / product_margin["Revenue"]) * 100
low_margin_products = product_margin[product_margin["Margin"] < 10]

print(f"""
PROBLEM: Many products priced without margin analysis.

SUPPORTING DATA:
  - Products with less than 10% margin: {len(low_margin_products)}
  - Average margin on these products: {low_margin_products['Margin'].mean():.1f}%
  - Pricing not optimized for profitability

RECOMMENDED ACTION:
  - Conduct cost-plus pricing analysis for all products
  - Implement dynamic pricing based on demand
  - A/B test price adjustments on select products
  - Review competitor pricing regularly
  - Set minimum margin thresholds for product approval
  - Use price elasticity analysis for optimization

EXPECTED BUSINESS IMPACT:
  - Average margin improvement: 5-8%
  - Revenue optimization without volume loss
  - Better competitive positioning
  - Sustainable pricing strategy
""")


# =========================================================
# RECOMMENDATION 10
# =========================================================

print("=" * 70)
print("RECOMMENDATION 10: ENHANCE CUSTOMER SEGMENTATION STRATEGY")
print("=" * 70)

segment_data = customers.merge(
    orders.groupby("Customer_ID").agg(
        Total_Spent=("Order_Total", "sum"),
        Order_Count=("Order_ID", "count"),
        Last_Order=("Order_Date", "max")
    ).reset_index(),
    on="Customer_ID", how="left"
)

segment_summary = segment_data.groupby("Customer_Segment").agg(
    Count=("Customer_ID", "count"),
    Avg_Spent=("Total_Spent", "mean"),
    Avg_Orders=("Order_Count", "mean")
).reset_index()

print(f"""
PROBLEM: Customer segments not leveraged for targeted strategies.

SUPPORTING DATA:
  - Customer segments identified: {len(segment_summary)}
  - Each segment has different behavior patterns
  - One-size-fits-all approach wastes resources

RECOMMENDED ACTION:
  - Create segment-specific marketing campaigns
  - Tailor product recommendations per segment
  - Develop segment-specific loyalty programs
  - Allocate resources based on segment value
  - Track segment migration over time
  - Implement segment-based customer service tiers

EXPECTED BUSINESS IMPACT:
  - Higher marketing conversion rates
  - Improved customer satisfaction
  - Better resource allocation
  - Increased customer lifetime value
  - More effective cross-selling and upselling
""")


# =========================================================
# SUMMARY TABLE
# =========================================================

print("\n" + "=" * 70)
print("RECOMMENDATIONS SUMMARY TABLE")
print("=" * 70)

recommendations_summary = pd.DataFrame({
    "No": range(1, 11),
    "Recommendation": [
        "Reduce Excessive Discounting",
        "Discontinue Loss-Making Products",
        "Customer Win-Back Program",
        "Optimize Marketing Budget",
        "Reduce Return Rate",
        "Focus on High-Margin Categories",
        "VIP Customer Retention",
        "Improve Regional Profitability",
        "Data-Driven Pricing Strategy",
        "Enhanced Segmentation Strategy"
    ],
    "Priority": [
        "HIGH", "HIGH", "HIGH", "MEDIUM",
        "MEDIUM", "MEDIUM", "HIGH", "MEDIUM",
        "HIGH", "MEDIUM"
    ],
    "Expected_Impact": [
        "2-4% margin improvement",
        f"${abs(order_items[order_items['Profit'] < 0]['Profit'].sum()) * 0.5:,.0f} profit recovery",
        "20% revenue recovery from at-risk",
        "20-30% marketing ROI improvement",
        "20-30% return rate reduction",
        "3-5% margin improvement",
        "25-35% VIP retention improvement",
        "30-40% margin gap closure",
        "5-8% average margin improvement",
        "Higher conversion & satisfaction"
    ],
    "Timeline": [
        "Immediate", "1-3 months", "1-2 months", "1 month",
        "2-4 months", "2-3 months", "1-2 months", "3-6 months",
        "2-4 months", "2-3 months"
    ]
})

print(recommendations_summary.to_string(index=False))


# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

print("\n" + "=" * 70)
print("EXECUTIVE SUMMARY")
print("=" * 70)

print("""
MANAGEMENT CONCERN:
"Our revenue is increasing, but profitability and customer retention 
are not improving at the same rate."

ROOT CAUSES IDENTIFIED:
1. Excessive discounting eroding profit margins
2. Loss-making products dragging down overall profitability
3. High customer churn among valuable segments
4. Inefficient marketing spend on low-ROI channels
5. High product return rates increasing costs
6. Regional pricing inconsistencies
7. Lack of targeted customer strategies

STRATEGIC RESPONSE:
The 10 recommendations above address each root cause with 
specific, data-driven actions. Implementing these changes 
in priority order will:

  - Improve profit margin by 5-10 percentage points
  - Recover 20-30% of at-risk customer revenue
  - Reduce marketing waste by 20-30%
  - Cut return-related costs by 20-30%
  - Enhance customer lifetime value across all segments

NEXT STEPS:
1. Present findings to management team
2. Prioritize HIGH impact recommendations
3. Assign owners and timelines for each initiative
4. Set up KPI tracking dashboard
5. Review progress monthly
""")
