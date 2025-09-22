import altair as alt
import streamlit as st
import pandas as pd

def billing_status_chart(df: pd.DataFrame):
    data = df["Billing Status"].value_counts().reset_index()
    data.columns = ["Billing Status", "Count"]
    return alt.Chart(data).mark_arc().encode(
        theta="Count", color="Billing Status", tooltip=["Billing Status", "Count"]
    ).properties(width=250, height=250)

def revenue_by_product_chart(df: pd.DataFrame):
    data = df.groupby("Product")["Amount"].sum().reset_index()
    return alt.Chart(data).mark_bar().encode(
        x="Product", y="Amount", tooltip=["Product", "Amount"]
    ).properties(width=250, height=250)

def delivery_status_chart(df: pd.DataFrame):
    data = df["Delivery"].value_counts().reset_index()
    data.columns = ["Delivery Status", "Count"]
    return alt.Chart(data).mark_arc().encode(
        theta="Count", color="Delivery Status", tooltip=["Delivery Status", "Count"]
    ).properties(width=250, height=250)

def revenue_over_time_chart(df: pd.DataFrame):
    data = df.groupby("Order Date")["Amount"].sum().reset_index()
    return alt.Chart(data).mark_line(point=True).encode(
        x="Order Date:T", y="Amount:Q", tooltip=["Order Date", "Amount"]
    ).properties(width=250, height=250)

def orders_per_customer_chart(df: pd.DataFrame):
    data = df["Customer"].value_counts().reset_index()
    data.columns = ["Customer", "Orders"]
    return alt.Chart(data).mark_bar().encode(
        x="Customer", y="Orders", tooltip=["Customer", "Orders"]
    ).properties(width=250, height=250)

def confirmed_chart(df: pd.DataFrame):
    data = df["Confirmed"].value_counts().reset_index()
    data.columns = ["Confirmed", "Count"]
    return alt.Chart(data).mark_bar().encode(
        x="Confirmed:N", y="Count:Q", tooltip=["Confirmed", "Count"]
    ).properties(width=250, height=250)
