
import pandas as pd
import numpy as np

# Load Raw Dataset
df = pd.read_csv("ecommerce_sales_raw.csv")

print("ORIGINAL DATA:", df.shape)

# 1. Remove Duplicate Records
df.drop_duplicates(inplace=True)

# 2. Remove Extra Spaces from Text Columns
text_columns = df.select_dtypes(include="object").columns

for col in text_columns:
    df[col] = df[col].str.strip()

# 3. Convert Order Date into Datetime
df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

# 4. Convert Numeric Columns
numeric_columns = [
    "age",
    "quantity",
    "unit_price",
    "discount_pct",
    "shipping_days",
    "sales",
    "profit"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 5. Check Missing Values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# 6. Check Invalid Values
print("\nINVALID VALUES:")

print("Invalid Quantity:", (df["quantity"] <= 0).sum())
print("Invalid Price:", (df["unit_price"] < 0).sum())
print("Invalid Discount:", 
      ((df["discount_pct"] < 0) |
       (df["discount_pct"] > 100)).sum())

# 7. Check Date Conversion
print("Invalid Dates:", df["order_date"].isnull().sum())

# 8. Save Cleaned Dataset
df.to_csv("ecommerce_sales_cleaned.csv", index=False)

print("\nCLEANING COMPLETED!")
print("Final Dataset Shape:", df.shape)
print("Cleaned Dataset Saved Successfully!")
