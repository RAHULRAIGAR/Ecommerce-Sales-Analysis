
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load Cleaned Dataset
df = pd.read_csv("ecommerce_sales_cleaned.csv")

df["order_date"] = pd.to_datetime(df["order_date"])

os.makedirs("outputs", exist_ok=True)

sns.set_theme(style="whitegrid")

# ==================================
# 1. KEY BUSINESS METRICS
# ==================================

total_orders = df["order_id"].nunique()
total_customers = df["customer_id"].nunique()
total_sales = df["sales"].sum()
total_profit = df["profit"].sum()

revenue_orders = df[df["sales"] > 0]
avg_order_value = (
    total_sales / revenue_orders["order_id"].nunique()
)

print("\n========== BUSINESS KPIs ==========")

print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Total Sales: ₹", round(total_sales, 2))
print("Total Profit: ₹", round(total_profit, 2))
print("Average Order Value: ₹", round(avg_order_value, 2))


# ==================================
# 2. CATEGORY-WISE SALES
# ==================================

category_sales = (
    df.groupby("product_category")["sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== CATEGORY SALES ==========")
print(category_sales)

category_sales.to_csv("outputs/category_sales.csv")


# ==================================
# 3. MONTHLY SALES ANALYSIS
# ==================================

monthly_sales = (
    df.set_index("order_date")
    .resample("ME")["sales"]
    .sum()
)

print("\n========== MONTHLY SALES ==========")
print(monthly_sales)

monthly_sales.to_csv("outputs/monthly_sales.csv")


# ==================================
# 4. STATE-WISE SALES
# ==================================

state_sales = (
    df.groupby("state")["sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== STATE SALES ==========")
print(state_sales)

state_sales.to_csv("outputs/state_sales.csv")


# ==================================
# 5. TOP 10 PRODUCTS
# ==================================

top_products = (
    df.groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS ==========")
print(top_products)


# ==================================
# 6. PAYMENT METHOD ANALYSIS
# ==================================

payment_analysis = (
    df.groupby("payment_method")["order_id"]
    .count()
    .sort_values(ascending=False)
)

print("\n========== PAYMENT METHODS ==========")
print(payment_analysis)


# ==================================
# 7. CATEGORY-WISE PROFIT
# ==================================

category_profit = (
    df.groupby("product_category")["profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== CATEGORY PROFIT ==========")
print(category_profit)


# ==================================
# 8. VISUALIZATIONS
# ==================================

# Chart 1: Category Sales
plt.figure(figsize=(10, 6))

category_sales.plot(
    kind="bar",
    title="Sales by Product Category",
    xlabel="Category",
    ylabel="Sales (INR)"
)

plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("outputs/category_sales.png")
plt.show()


# Chart 2: Monthly Sales Trend
plt.figure(figsize=(12, 6))

monthly_sales.plot(
    kind="line",
    marker="o",
    title="Monthly Sales Trend",
    xlabel="Month",
    ylabel="Sales (INR)"
)

plt.tight_layout()
plt.savefig("outputs/monthly_sales.png")
plt.show()


# Chart 3: State-wise Sales
plt.figure(figsize=(12, 6))

state_sales.head(10).plot(
    kind="bar",
    title="Top 10 States by Sales",
    xlabel="State",
    ylabel="Sales (INR)"
)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/state_sales.png")
plt.show()


# Chart 4: Category Profit
plt.figure(figsize=(10, 6))

category_profit.plot(
    kind="bar",
    title="Profit by Product Category",
    xlabel="Category",
    ylabel="Profit (INR)"
)

plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("outputs/category_profit.png")
plt.show()


print("\n========== EDA COMPLETED ==========")
print("Charts and analysis files saved in outputs folder.")
