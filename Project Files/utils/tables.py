import streamlit as st
import pandas as pd

def active_orders_table(df: pd.DataFrame):
    if {"Confirmed", "Sales Order", "Product", "Qty", "Production Order", "Delivery"} <= set(df.columns):
        active_orders = df[df["Confirmed"] == True]
        st.dataframe(active_orders[["Sales Order", "Product", "Qty", "Production Order", "Confirmed", "Delivery"]])
    else:
        st.info("Active orders table not available.")

def billing_table(df: pd.DataFrame):
    if {"Invoice", "Customer", "Amount", "Billing Status"} <= set(df.columns):
        st.dataframe(df[["Invoice", "Customer", "Amount", "Billing Status"]])
    else:
        st.info("Billing table not available.")

def full_history_table(df: pd.DataFrame):
    st.dataframe(df)
