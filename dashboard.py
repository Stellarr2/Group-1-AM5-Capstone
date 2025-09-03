import streamlit as st
import pandas as pd

# Load processed data
df = pd.read_csv("dashboard_data.csv")

st.set_page_config(page_title="MTO Production Dashboard", layout="wide")

# --- Title ---
st.markdown("<h2 style='color:#0a6ed1;'>📊 Make-to-Order Production Dashboard</h2>", unsafe_allow_html=True)

# --- KPI Cards (like Fiori tiles) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Orders", len(df))
with col2:
    st.metric("Confirmed Orders", int(df["Confirmed"].sum()))
with col3:
    st.metric("Delivered Orders", int((df["Delivery"] == "Delivered").sum()))
with col4:
    st.metric("Total Revenue ($)", f"{df['Amount'].sum():,.2f}")

st.markdown("---")

# --- Active Orders Card ---
with st.container():
    st.markdown("### 📦 Active Production Orders")
    active_orders = df[df["Confirmed"] == True]
    st.dataframe(active_orders[["Sales Order", "Product", "Qty", "Production Order", "Confirmed", "Delivery"]])

# --- Billing Card ---
with st.container():
    st.markdown("### 💰 Billing Overview")
    billing = df[["Invoice", "Customer", "Amount", "Billing Status"]]
    st.dataframe(billing)

# --- Order History Card ---
with st.container():
    st.markdown("### 📜 Full Order History")
    st.dataframe(df)
