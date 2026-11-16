
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load dataset
df = pd.read_csv("ecommerce_sales_cleaned.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

os.makedirs("outputs", exist_ok=True)

sns.set_theme(style="whitegrid")

# Use delivered orders for customer revenue analysis
delivered = df[df["order_status"] == "Delivered"].copy()

print("\n========== ADVANCED BUSINESS ANALYTICS ==========")

# ==================================
# 1. CUSTOMER SEGMENTATION (RFM)
# ==================================

snapshot_date = delivered["order_date"].max() + pd.Timedelta(days=1)

rfm = delivered.groupby("customer_id").agg(
    Recency=("order_date", lambda x: (snapshot_date - x.max()).days),
    Frequency=("order_id", "nunique"),
    Monetary=("sales", "sum")
).reset_index()

# RFM Scores
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

def customer_segment(row):

    if row["R_Score"] >= 4 and row["F_Score"] >= 4:
        return "Champions"

    elif row["R_Score"] >= 3 and row["F_Score"] >= 4:
        return "Loyal Customers"

    elif row["R_Score"] >= 4 and row["F_Score"] >= 2:
        return "Potential Loyalists"

    elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
        return "At Risk"

    else:
        return "Others"

rfm["Segment"] = rfm.apply(customer_segment, axis=1)

print("\n--- CUSTOMER SEGMENTATION ---")
print(rfm["Segment"].value_counts())

rfm.to_csv("outputs/customer_segmentation.csv", index=False)


# ==================================
# 2. REPEAT CUSTOMER ANALYSIS
# ==================================

customer_orders = delivered.groupby("customer_id")[
    "order_id"
].nunique()

repeat_customers = customer_orders[customer_orders > 1]

repeat_rate = (
    len(repeat_customers) / len(customer_orders) * 100
)

print("\n--- REPEAT CUSTOMER ANALYSIS ---")
print("Total Customers:", len(customer_orders))
print("Repeat Customers:", len(repeat_customers))
print("Repeat Customer Rate:", round(repeat_rate, 2), "%")


# ==================================
# 3. DISCOUNT VS PROFIT ANALYSIS
# ==================================

discount_analysis = delivered.groupby("discount_pct").agg(
    Total_Sales=("sales", "sum"),
    Total_Profit=("profit", "sum"),
    Average_Profit=("profit", "mean"),
    Order_Count=("order_id", "nunique")
).reset_index()

print("\n--- DISCOUNT ANALYSIS ---")
print(discount_analysis)

discount_analysis.to_csv(
    "outputs/discount_analysis.csv", index=False
)


# ==================================
# 4. PROFIT MARGIN ANALYSIS
# ==================================

total_sales = delivered["sales"].sum()
total_profit = delivered["profit"].sum()

profit_margin = (total_profit / total_sales) * 100

print("\n--- PROFIT MARGIN ---")
print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Profit Margin:", round(profit_margin, 2), "%")


# ==================================
# 5. TOP 10 CUSTOMERS
# ==================================

top_customers = (
    delivered.groupby("customer_id")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n--- TOP 10 CUSTOMERS ---")
print(top_customers)

top_customers.to_csv("outputs/top_customers.csv")


# ==================================
# 6. ORDER STATUS ANALYSIS
# ==================================

status_analysis = df["order_status"].value_counts()

print("\n--- ORDER STATUS ---")
print(status_analysis)

status_analysis.to_csv("outputs/order_status.csv")


# ==================================
# 7. VISUALIZATION
# ==================================

# Customer Segmentation Chart
plt.figure(figsize=(10, 6))

rfm["Segment"].value_counts().plot(
    kind="bar",
    title="Customer Segmentation"
)

plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("outputs/customer_segments.png")
plt.show()


# Discount vs Profit Chart
plt.figure(figsize=(10, 6))

plt.plot(
    discount_analysis["discount_pct"],
    discount_analysis["Total_Profit"],
    marker="o"
)

plt.title("Discount vs Total Profit")
plt.xlabel("Discount Percentage")
plt.ylabel("Total Profit")
plt.tight_layout()
plt.savefig("outputs/discount_profit.png")
plt.show()


# Top 10 Customers Chart
plt.figure(figsize=(10, 6))

top_customers.sort_values().plot(
    kind="barh",
    title="Top 10 Customers by Sales"
)

plt.xlabel("Sales (INR)")
plt.ylabel("Customer ID")
plt.tight_layout()
plt.savefig("outputs/top_customers.png")
plt.show()


print("\n========== ADVANCED ANALYSIS COMPLETED ==========")
print("All reports saved in outputs folder.")
