import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Pig Farm Dashboard",
    page_icon="🐖",
    layout="wide"
)

st.title("🐖 Pig Farm Business Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("pig_sales_data.csv")

df = load_data()

st.sidebar.header("Filters")

month = st.sidebar.multiselect(
    "Select Month",
    df["Month"].unique(),
    default=df["Month"].unique()
)

category = st.sidebar.multiselect(
    "Customer Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Month"].isin(month)) &
    (df["Category"].isin(category))
]

total_revenue = filtered_df["Revenue"].sum()
total_pigs = filtered_df["Pigs_Sold"].sum()
profit = filtered_df["Revenue"].sum() - filtered_df["Feed_Cost"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Revenue", f"KES {total_revenue:,.0f}")
col2.metric("Pigs Sold", total_pigs)
col3.metric("Profit", f"KES {profit:,.0f}")

st.subheader("Revenue by Category")

category_sales = filtered_df.groupby("Category")["Revenue"].sum().reset_index()

fig = px.bar(
    category_sales,
    x="Category",
    y="Revenue",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Monthly Revenue Trend")

monthly = filtered_df.groupby("Month")["Revenue"].sum().reset_index()

fig2 = px.line(
    monthly,
    x="Month",
    y="Revenue",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Sales Data")
st.dataframe(filtered_df)