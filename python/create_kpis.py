import pandas as pd

# ==========================================
# STEP 1: LOAD CLEANED DATA
# ==========================================

df = pd.read_csv("vendor_cleaned.csv")

print("Cleaned Data Loaded Successfully!")
print("Original Shape:", df.shape)


# ==========================================
# STEP 2: CREATE TOTAL SPEND
# ==========================================

df["Total_Spend"] = (
    df["Quantity"] * df["Negotiated_Price"]
)


# ==========================================
# STEP 3: CREATE POTENTIAL SPEND
# ==========================================

df["Potential_Spend"] = (
    df["Quantity"] * df["Unit_Price"]
)


# ==========================================
# STEP 4: CREATE SAVINGS
# ==========================================

df["Savings"] = (
    df["Potential_Spend"] - df["Total_Spend"]
)


# ==========================================
# STEP 5: CREATE SAVINGS PERCENTAGE
# ==========================================

df["Savings_Percentage"] = (
    df["Savings"] /
    df["Potential_Spend"].replace(0, pd.NA)
) * 100


# ==========================================
# STEP 6: CREATE DELIVERY DAYS
# ==========================================

# Convert dates again to make sure they are datetime

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

df["Delivery_Date"] = pd.to_datetime(
    df["Delivery_Date"],
    errors="coerce"
)

df["Delivery_Days"] = (
    df["Delivery_Date"] - df["Order_Date"]
).dt.days


# ==========================================
# STEP 7: CREATE DEFECT RATE
# ==========================================

df["Defect_Rate"] = (
    df["Defective_Units"] /
    df["Quantity"].replace(0, pd.NA)
) * 100


# ==========================================
# STEP 8: CREATE QUALITY RATE
# ==========================================

df["Quality_Rate"] = (
    100 - df["Defect_Rate"]
)


# ==========================================
# STEP 9: CREATE MONTH
# ==========================================

df["Order_Month"] = (
    df["Order_Date"].dt.month
)


# ==========================================
# STEP 10: CREATE MONTH NAME
# ==========================================

df["Order_Month_Name"] = (
    df["Order_Date"].dt.strftime("%B")
)


# ==========================================
# STEP 11: CREATE YEAR
# ==========================================

df["Order_Year"] = (
    df["Order_Date"].dt.year
)


# ==========================================
# STEP 12: CREATE QUARTER
# ==========================================

df["Order_Quarter"] = (
    df["Order_Date"]
    .dt.to_period("Q")
    .astype(str)
)


# ==========================================
# STEP 13: DISPLAY KPI RESULTS
# ==========================================

print("\n===== KPI RESULTS =====")

print(
    df[
        [
            "Supplier",
            "Quantity",
            "Unit_Price",
            "Negotiated_Price",
            "Total_Spend",
            "Savings",
            "Savings_Percentage",
            "Delivery_Days",
            "Defect_Rate",
            "Quality_Rate"
        ]
    ].head(10)
)


# ==========================================
# STEP 14: CHECK NEW COLUMNS
# ==========================================

print("\n===== ALL COLUMNS =====")

print(df.columns.tolist())


# ==========================================
# STEP 15: CHECK MISSING VALUES
# ==========================================

print("\n===== MISSING VALUES =====")

print(df.isnull().sum())


# ==========================================
# STEP 16: SAVE FINAL KPI DATASET
# ==========================================

df.to_csv(
    "vendor_cleaned_kpi.csv",
    index=False
)

print("\n==========================================")
print("KPI DATASET CREATED SUCCESSFULLY!")
print("==========================================")

print("Final Shape:", df.shape)

print("\nFile created:")
print("vendor_cleaned_kpi.csv")