import streamlit as st
from utils.kpis import show_kpis
import pandas as pd
from utils import charts  # where the chart functions live


def show_charts(df: pd.DataFrame):
    # KPIs row
    show_kpis(df)

    st.markdown("---")
    st.title("📊 Charts and Analytics")
    if df.empty:
        st.warning("No data to show.")
        return

    # Charts in responsive card layout
    col1, col2 = st.columns(2)
    with col1.container(border=True, height = "stretch"):
        st.header("Billing")
        st.altair_chart(charts.billing_status_chart(df), use_container_width=True)
        
    with col2.container(border=True, height = "stretch"):
        st.header("Delivery")
        st.altair_chart(charts.delivery_status_chart(df), use_container_width=True)
        
    col3, = st.columns(1)
    with col3.container(border=True, height = "stretch"):
        st.header("Revenue")
        st.altair_chart(charts.revenue_over_time_chart(df), use_container_width=True)        

    col5, col6 = st.columns(2)
    with col5.container(border=True, height = "stretch"):
        st.header("Top Customers")
        st.altair_chart(charts.top_customers_chart(df), use_container_width=True)
        
    with col6.container(border=True, height = "stretch"):
        st.header("Status")
        st.altair_chart(charts.order_status_chart(df), use_container_width=True)

    col7, = st.columns(1)
    with col7.container(border=True, height="stretch"):
        st.header("Products")
        st.altair_chart(charts.revenue_by_product_chart(df), use_container_width=True)

    col8, = st.columns(1)
    with col8.container(border=True, height="stretch"):
        st.header("Customers")
        st.altair_chart(charts.orders_per_customer_chart(df), use_container_width=True)
    
    col9, = st.columns(1)
    with col9.container(border=True, height="stretch"):
        st.header("Total Revenue")
        st.altair_chart(charts.cumulative_revenue_chart(df), use_container_width=True)
        
    colX, colY = st.columns(2)
    with colX.container(border=True):
        st.header("Order Funnel")
        st.altair_chart(charts.order_funnel_chart(df), use_container_width=True)

    with colY.container(border=True):
        st.header("Revenue Growth")
        st.altair_chart(charts.monthly_revenue_growth_chart(df), use_container_width=True)

    colA, colB = st.columns(2)
    with colA.container(border=True):
        st.header("Product Amounts")
        st.altair_chart(charts.product_mix_share_chart(df), use_container_width=True)

    with colB.container(border=True):
        st.header("Customer Value")
        st.altair_chart(charts.customer_segmentation_chart(df), use_container_width=True)

