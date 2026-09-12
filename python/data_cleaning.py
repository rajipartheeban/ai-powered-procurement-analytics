import pandas as pd

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("Procurement KPI Analysis Dataset.csv")

print("Original Shape:", df.shape)


# ==========================================
# 2. REMOVE DUPLICATE ROWS
# ==========================================

df = df.drop_duplicates()

print("Shape After Removing Duplicates:", df.shape)


# ==========================================
# 3. CONVERT DATE COLUMNS
# ==========================================

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

df["Delivery_Date"] = pd.to_datetime(
    df["Delivery_Date"],
    errors="coerce"
)


# ==========================================
# 4. CHECK MISSING VALUES
# ==========================================

print("\nMissing Values:")
print(df.isnull().sum())


# ==========================================
# 5. CHECK INVALID VALUES
# ==========================================

print("\nNegative Quantity:")
print((df["Quantity"] < 0).sum())

print("\nNegative Unit Price:")
print((df["Unit_Price"] < 0).sum())

print("\nNegative Negotiated Price:")
print((df["Negotiated_Price"] < 0).sum())

print("\nNegative Defective Units:")
print((df["Defective_Units"] < 0).sum())


# ==========================================
# 6. CHECK DEFECTIVE UNITS VS QUANTITY
# ==========================================

invalid_defects = df[
    df["Defective_Units"].notna()
    & (df["Defective_Units"] > df["Quantity"])
]

print("\nDefective Units Greater Than Quantity:")
print(len(invalid_defects))


# ==========================================
# 7. CHECK DATE LOGIC
# ==========================================

invalid_dates = df[
    df["Delivery_Date"].notna()
    & (df["Delivery_Date"] < df["Order_Date"])
]

print("\nDelivery Date Before Order Date:")
print(len(invalid_dates))


# ==========================================
# 8. CHECK UNIQUE VALUES
# ==========================================

print("\nUnique Suppliers:")
print(df["Supplier"].nunique())

print("\nSuppliers:")
print(df["Supplier"].unique())

print("\nItem Categories:")
print(df["Item_Category"].unique())

print("\nOrder Status:")
print(df["Order_Status"].unique())

print("\nCompliance:")
print(df["Compliance"].unique())


# ==========================================
# 9. STANDARDIZE TEXT COLUMNS
# ==========================================

text_columns = [
    "Supplier",
    "Item_Category",
    "Order_Status",
    "Compliance"
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()


# ==========================================
# 10. HANDLE MISSING DEFECTIVE UNITS
# ==========================================

df["Defective_Units"] = df["Defective_Units"].fillna(0)


# ==========================================
# 11. KEEP MISSING DELIVERY DATES
# ==========================================

print("\nMissing Delivery Dates:")
print(df["Delivery_Date"].isnull().sum())


# ==========================================
# 12. FINAL DATA CHECK
# ==========================================

print("\nFinal Data Types:")
print(df.dtypes)

print("\nFinal Missing Values:")
print(df.isnull().sum())

print("\nFinal Shape:")
print(df.shape)


# ==========================================
# 13. SAVE CLEANED DATA
# ==========================================

df.to_csv(
    "vendor_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")