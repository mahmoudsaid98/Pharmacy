import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set wide layout and title
st.set_page_config(page_title="Pharmacy Dashboard", layout="wide")
st.title("💊 Pharmacy Sales Dashboard")

# Upload Excel file
uploaded_file = st.file_uploader("📤 Upload your pharmacy Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.success("✅ File uploaded successfully!")
    except Exception as e:
        st.error(f"❌ Could not read Excel file: {e}")
        st.stop()

    # Convert 'Date' column to datetime
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df.dropna(subset=["Date"], inplace=True)

    # Required columns check
    required_columns = ["Product", "Quantity", "Customer", "Total_Price", "Date", "Payment_Method"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        st.error(f"❌ Required columns missing: {', '.join(missing_cols)}")
        st.stop()

    # 🔍 Search by product name
    st.subheader("🔎 Search Products")
    search_term = st.text_input("Search by product name")
    if search_term:
        filtered_df = df[df["Product"].str.lower().str.contains(search_term.lower())]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df)

    
    st.subheader("🧑‍💼 All Customers by Total Payment")

# Group by customer and calculate total price
    all_customers = df.groupby("Customer")["Total_Price"].sum().reset_index()

# Rename column for clarity
    all_customers = all_customers.rename(columns={"Total_Price": "Total Spent"})

# Display sortable table
    st.dataframe(all_customers.sort_values("Total Spent", ascending=False))

    # 📊 Daily sales table
    st.subheader("📊 Total Sales Per Day")
    daily_summary = df.groupby(df["Date"].dt.date).agg({
        "Quantity": "sum",
        "Total_Price": "sum"
    }).reset_index().rename(columns={
        "Date": "Date",
        "Quantity": "Total Quantity",
        "Total_Price": "Total Sales"
    })
    st.dataframe(daily_summary)

    # 🧾 Products sold on a specific day
    st.subheader("🧾 Products Sold on a Specific Day")
    selected_date = st.date_input("Select a date to view sales", df["Date"].dt.date.min())
    filtered_day_df = df[df["Date"].dt.date == selected_date]

    if not filtered_day_df.empty:
        product_summary = filtered_day_df.groupby("Product").agg({
            "Quantity": "sum",
            "Total_Price": "sum"
        }).reset_index().rename(columns={
            "Quantity": "Total Quantity",
            "Total_Price": "Total Sales"
        })

        st.markdown(f"### 📅 Sales Breakdown for {selected_date}")
        st.dataframe(product_summary)
    else:
        st.warning("⚠️ No sales recorded on this date.")

    # 📈 Sales by Product
    st.subheader("📈 Sales by Product")
    sales_by_product = df.groupby("Product")["Total_Price"].sum().sort_values(ascending=False)
    st.bar_chart(sales_by_product)

   
else:
    st.info("👈 Please upload your Excel file to begin.")
