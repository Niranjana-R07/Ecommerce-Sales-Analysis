import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# ==========================================================
# DATABASE CONNECTION
# ==========================================================

engine = create_engine(
    "mysql+pymysql://root:nira2006@localhost/ecommerce"
)

# Read data from MySQL
query = "SELECT * FROM ecommerce_sales"
df = pd.read_sql(query, engine)

# ==========================================================
# BASIC INFORMATION
# ==========================================================

print("\n========== FIRST 5 RECORDS ==========")
print(df.head())

print("\n========== LAST 5 RECORDS ==========")
print(df.tail())

print("\n========== SHAPE ==========")
print(df.shape)

print("\n========== COLUMNS ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== INFO ==========")
df.info()

print("\n========== DESCRIPTIVE STATISTICS ==========")
print(df.describe())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATES ==========")
print(df.duplicated().sum())

# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

if "Order_Date" in df.columns:
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    df["Month_Name"] = df["Order_Date"].dt.month_name()
    df["Day"] = df["Order_Date"].dt.day

if "Sales" in df.columns and "Profit" in df.columns:
    df["Profit_Margin"] = (df["Profit"] / df["Sales"]) * 100

print("\nFeature Engineering Completed")

# ==========================================================
# UNIQUE VALUES
# ==========================================================

if "Category" in df.columns:
    print("\nCategories")
    print(df["Category"].unique())

if "Region" in df.columns:
    print("\nRegions")
    print(df["Region"].unique())

# ==========================================================
# SALES DISTRIBUTION
# ==========================================================

if "Sales" in df.columns:
    plt.figure(figsize=(8,5))
    plt.hist(df["Sales"], bins=20)
    plt.title("Sales Distribution")
    plt.xlabel("Sales")
    plt.ylabel("Frequency")
    plt.show()

# ==========================================================
# PROFIT DISTRIBUTION
# ==========================================================

if "Profit" in df.columns:
    plt.figure(figsize=(8,5))
    plt.hist(df["Profit"], bins=20)
    plt.title("Profit Distribution")
    plt.xlabel("Profit")
    plt.ylabel("Frequency")
    plt.show()

# ==========================================================
# CATEGORY SALES
# ==========================================================

if "Category" in df.columns:

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nCategory Sales")
    print(category_sales)

    plt.figure(figsize=(8,5))
    category_sales.plot(kind="bar")
    plt.title("Category Wise Sales")
    plt.ylabel("Sales")
    plt.show()

# ==========================================================
# REGION PROFIT
# ==========================================================

if "Region" in df.columns:

    region_profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nRegion Profit")
    print(region_profit)

    plt.figure(figsize=(8,5))
    region_profit.plot(kind="bar")
    plt.title("Region Wise Profit")
    plt.ylabel("Profit")
    plt.show()

# ==========================================================
# TOP 10 PRODUCTS
# ==========================================================

if "Product_Name" in df.columns:

    top_products = (
        df.groupby("Product_Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\nTop Products")
    print(top_products)

    plt.figure(figsize=(10,5))
    top_products.plot(kind="bar")
    plt.title("Top 10 Products")
    plt.ylabel("Sales")
    plt.show()

# ==========================================================
# MONTHLY SALES
# ==========================================================

if "Year" in df.columns:

    monthly_sales = (
        df.groupby(["Year", "Month"])["Sales"]
        .sum()
        .reset_index()
        .sort_values(["Year", "Month"])
    )

    print("\nMonthly Sales")
    print(monthly_sales)

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

numeric_df = df.select_dtypes(include=np.number)

corr = numeric_df.corr()

plt.figure(figsize=(10,6))
sns.heatmap(corr, annot=True)
plt.title("Correlation Heatmap")
plt.show()

# ==========================================================
# BOXPLOTS
# ==========================================================

if "Sales" in df.columns:
    plt.figure(figsize=(8,3))
    sns.boxplot(x=df["Sales"])
    plt.title("Sales Outliers")
    plt.show()

if "Profit" in df.columns:
    plt.figure(figsize=(8,3))
    sns.boxplot(x=df["Profit"])
    plt.title("Profit Outliers")
    plt.show()

# ==========================================================
# SAVE CSV
# ==========================================================

df.to_csv("ecommerce_sales_cleaned.csv", index=False)

print("\nCSV Saved Successfully")

# ==========================================================
# SAVE TO MYSQL
# ==========================================================

with engine.begin() as conn:
    df.to_sql(
        "ecommerce_sales_cleaned",
        con=conn,
        if_exists="replace",
        index=False
    )

print("MySQL Table Created Successfully")

engine.dispose()



