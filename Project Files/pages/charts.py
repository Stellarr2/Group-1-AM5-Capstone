import streamlit as st
from utils.kpis import show_kpis
from utils import charts

def show_charts(df):
    st.title("📊 Charts")
    if df.empty:
        st.warning("No data to show.")
        return

    show_kpis(df)  # KPI tiles
    st.markdown("<hr></hr>", unsafe_allow_html=True)

    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1: st.altair_chart(charts.billing_status_chart(df))
    with row1_col2: st.altair_chart(charts.revenue_by_product_chart(df))
    with row1_col3: st.altair_chart(charts.delivery_status_chart(df))

    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1: st.altair_chart(charts.revenue_over_time_chart(df))
    with row2_col2: st.altair_chart(charts.orders_per_customer_chart(df))
    with row2_col3: st.altair_chart(charts.confirmed_chart(df))
