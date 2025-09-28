import streamlit as st
import pandas as pd

def show_kpis(df: pd.DataFrame):
    """Render KPI metric tiles with context inside bordered containers."""
    total_orders = len(df)
    confirmed_orders = int(df["Confirmed"].sum()) if "Confirmed" in df.columns else 0
    delivered_orders = int((df["Delivery"] == "Delivered").sum()) if "Delivery" in df.columns else 0
    total_revenue = df["Amount"].sum() if "Amount" in df.columns else 0.0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    paid_count = int((df["Billing Status"] == "Paid").sum()) if "Billing Status" in df.columns else 0
    # unpaid_count = total_orders - paid_count
    paid_pct = (paid_count / total_orders * 100) if total_orders > 0 else 0
    delivered_pct = (delivered_orders / total_orders * 100) if total_orders > 0 else 0
    confirmed_pct = (confirmed_orders / total_orders * 100) if total_orders > 0 else 0

    st.title("📊 Streamflow: MTO Production Dashboard")
    st.header("Key Peformance Indicators")
    col1, col2 = st.columns(2)

    # Total Orders
    with col1.container(border=True, height="stretch"):
        st.metric("📦 Total Orders", total_orders, border=True)
        st.caption(f"Avg Order Value: ${avg_order_value:,.2f}")

    # Confirmed Orders
    with col2.container(border=True, height="stretch"):
        st.metric("✅ Confirmed Orders", confirmed_orders, border=True)
        st.caption(f"{confirmed_pct:.1f}% of all orders")


    col3, col4 = st.columns(2)
    # Delivered Orders
    with col3.container(border=True, height="stretch"):
        st.metric("🚚 Delivered Orders", delivered_orders, border=True)
        st.caption(f"{delivered_pct:.1f}% of all orders")

    # Total Revenue
    with col4.container(border=True, height="stretch"):
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}", border=True)
        st.caption(f"{paid_pct:.1f}% invoices paid ({paid_count} / {total_orders})")
