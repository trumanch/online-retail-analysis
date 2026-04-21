import streamlit as st
import pandas as pd

st.set_page_config(page_title="Online Retail Dashboard", layout="wide")

st.title("Online Retail Dashboard")
st.write("Interactive dashboard for analysing revenue, orders, and product performance.")

@st.cache_data
def load_data():
    df = pd.read_csv("data/online_retail.csv", encoding="ISO-8859-1")
    df = df.dropna(subset=["CustomerID", "Description"])
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]

    df["CustomerID"] = df["CustomerID"].astype(str)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

countries = sorted(df["Country"].dropna().unique())
selected_country = st.sidebar.selectbox("Select Country", ["All"] + countries)

if selected_country != "All":
    filtered_df = df[df["Country"] == selected_country].copy()
else:
    filtered_df = df.copy()

# KPIs
total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["CustomerID"].nunique()
average_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"£{total_revenue:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Total Customers", total_customers)
col4.metric("Average Order Value", f"£{average_order_value:,.2f}")

st.divider()

# Monthly revenue trend
st.subheader("Monthly Revenue Trend")
monthly_revenue = filtered_df.groupby("Month")["Revenue"].sum()
st.line_chart(monthly_revenue)

# Top products
st.subheader("Top 10 Products by Revenue")
top_products = (
    filtered_df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
st.bar_chart(top_products)

# Top countries only when All selected
if selected_country == "All":
    st.subheader("Top 10 Countries by Revenue")
    country_revenue = (
        filtered_df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(country_revenue)

# Raw data preview
with st.expander("Preview filtered data"):
    st.dataframe(filtered_df.head(20))