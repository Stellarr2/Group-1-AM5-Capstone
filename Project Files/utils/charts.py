import altair as alt
import pandas as pd
import numpy as np

def billing_status_chart(df: pd.DataFrame):
    data = df["Billing Status"].value_counts().reset_index()
    data.columns = ["Billing Status", "Count"]
    return alt.Chart(data, title="Paid and Unpaid Orders").mark_arc().encode(
        theta="Count",
        color=alt.Color("Billing Status", scale=alt.Scale(
            domain=["Paid", "Unpaid"],
            range=["green", "red"]
        )),
        tooltip=["Billing Status", "Count"]
    ).properties(width=250, height=250)

def revenue_by_product_chart(df: pd.DataFrame):
    data = df.groupby("Product")["Amount"].sum().reset_index()
    return alt.Chart(data, title="Revenue by Product").mark_bar().encode(
        x="Product",
        y="Amount",
        color=alt.Color("Product", scale=alt.Scale(scheme="category10")),
        tooltip=["Product", "Amount"]
    ).properties(width=400, height=400)

def delivery_status_chart(df: pd.DataFrame):
    data = df["Delivery"].value_counts().reset_index()
    data.columns = ["Delivery Status", "Count"]
    return alt.Chart(data, title = "Products In/Not In Transit").mark_arc().encode(
        theta="Count", color="Delivery Status", tooltip=["Delivery Status", "Count"]
    ).properties(width=250, height=250)

def revenue_over_time_chart(df: pd.DataFrame):
    data = df.groupby("Order Date")["Amount"].sum().reset_index()

    # Add a category column
    data["Revenue Category"] = data["Amount"].apply(
        lambda x: "Under 30,000 Revenue" if x < 30000 else "Over 30,000 Revenue"
    )

    # Base line (always neutral)
    line = (
        alt.Chart(data)
        .mark_line(color="lightblue", strokeWidth=2)   # fixed neutral color
        .encode(
            x=alt.X("Order Date:T", title="Order Date"),
            y=alt.Y("Amount:Q", title="Revenue"),
            tooltip=["Order Date:T", "Amount:Q"]
        )
    )

    # Points with categorical color (legend will appear)
    points = (
        alt.Chart(data)
        .mark_point(size=60, filled=True, opacity=1)
        .encode(
            x="Order Date:T",
            y="Amount:Q",
            color=alt.Color(
                "Revenue Category:N",
                scale=alt.Scale(domain=["Under 30,000 Revenue", "Over 30,000 Revenue"],
                                range=["red", "green"]),
                legend=alt.Legend(title="Revenue Threshold")
            ),
            tooltip=["Order Date:T", "Amount:Q", "Revenue Category"]
        )
    )

    return (line + points).properties(title="Revenue Over Time", width=400, height=250)

def orders_per_customer_chart(df: pd.DataFrame):
    data = df["Customer"].value_counts().reset_index()
    data.columns = ["Customer", "Orders"]
    return alt.Chart(data, title="Orders Per Customer").mark_bar().encode(
        x= 'Orders:Q',
        y=alt.Y('Customer:N', sort= '-x'),
        color=alt.Color("Customer", scale=alt.Scale(scheme="tableau20")),  # distinct palette
        tooltip=["Customer", "Orders"]
    ).properties(width=250, height=500)

def confirmed_chart(df: pd.DataFrame):
    data = df["Confirmed"].value_counts().reset_index()
    data.columns = ["Confirmed", "Count"]
    return alt.Chart(data, title="Production Orders").mark_arc().encode(
        theta="Count",
        color=alt.Color("Confirmed", scale=alt.Scale(
            domain=[True, False],
            range=["blue", "red"]
        )),
        tooltip=["Confirmed", "Count"]
    ).properties(width=250, height=250)

def top_customers_chart(df: pd.DataFrame):
    data = df.groupby("Customer")["Amount"].sum().reset_index()
    data = data.sort_values("Amount", ascending=False).head(5)

    return alt.Chart(data, title="Top 5 Customers by Revenue").mark_bar().encode(
        x="Amount:Q",
        y=alt.Y("Customer:N", sort="-x"),
        color=alt.Color("Customer:N", scale=alt.Scale(scheme="tableau10")),
        tooltip=["Customer", "Amount"]
    ).properties(width=400, height=250)

def order_status_chart(df: pd.DataFrame):
    data = df["Status"].value_counts().reset_index()
    data.columns = ["Status", "Count"]

    return alt.Chart(data, title="Order Status Breakdown").mark_arc().encode(
        theta="Count",
        color=alt.Color("Status:N", scale=alt.Scale(scheme="set2")),
        tooltip=["Status", "Count"]
    ).properties(width=250, height=250)

def cumulative_revenue_chart(df: pd.DataFrame):
    data = df.groupby("Order Date")["Amount"].sum().reset_index()
    data = data.sort_values("Order Date")
    data["Cumulative Revenue"] = data["Amount"].cumsum()

    return alt.Chart(data, title="Cumulative Revenue Over Time").mark_line(point=True).encode(
        x="Order Date:T",
        y="Cumulative Revenue:Q",
        tooltip=["Order Date:T", "Cumulative Revenue:Q"]
    ).properties(width=400, height=250)

def order_funnel_chart(df: pd.DataFrame):
    """Funnel chart: Sales → Production → Delivery → Billing"""
    stages = {
        "Sales Orders": len(df),
        "Production Orders": df["Production Order"].nunique() if "Production Order" in df.columns else 0,
        "Delivered": int((df["Delivery"] == "Delivered").sum()) if "Delivery" in df.columns else 0,
        "Billed": int((df["Billing Status"] == "Paid").sum()) if "Billing Status" in df.columns else 0
    }
    data = pd.DataFrame({"Stage": list(stages.keys()), "Count": list(stages.values())})

    return alt.Chart(data, title="Order Lifecycle Funnel").mark_bar().encode(
        x="Count:Q",
        y=alt.Y("Stage:N", sort=list()),
        color="Stage:N",
        tooltip=["Stage", "Count"]
    ).properties(width=400, height=300)

def monthly_revenue_growth_chart(df: pd.DataFrame):
    """Revenue by month with line following the bar tops."""
    data = df.copy()
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    data["Year-Month"] = data["Order Date"].dt.to_period("M").astype(str)

    grouped = data.groupby("Year-Month")["Amount"].sum().reset_index()
    grouped["Growth (%)"] = round(grouped["Amount"].pct_change().fillna(0) * 100, 2)

    base = alt.Chart(grouped).encode(
        x=alt.X("Year-Month:N", title="Month"),
        tooltip=["Year-Month", "Amount", "Growth (%)"]
    )

    # Bars = Revenue
    bars = base.mark_bar(color="steelblue").encode(
        y=alt.Y("Amount:Q", axis=alt.Axis(title="Revenue"))
    )

    # Line = Revenue (aligned with bar tops)
    line = base.mark_line(color="lightgreen", point=True).encode(
        y=alt.Y("Amount:Q")   # <- same as bars
    )

    return (bars + line).properties(
        title="Monthly Revenue Growth",
        width=500,
        height=300
    )

def customer_segmentation_chart(df: pd.DataFrame):
    """Group customers by revenue tiers (High/Medium/Low)."""
    data = df.groupby("Customer")["Amount"].sum().reset_index()

    # Compute thresholds (tertiles)
    q1, q2 = np.percentile(data["Amount"], [33, 66]) if len(data) > 2 else (0, 0)
    def segment(x):
        if x >= q2:
            return "High Value"
        elif x >= q1:
            return "Medium Value"
        else:
            return "Low Value"
    data["Segment"] = data["Amount"].apply(segment)

    return alt.Chart(data, title="Customer Segmentation by Revenue").mark_bar().encode(
        x="Customer:N",
        y="Amount:Q",
        color=alt.Color("Segment:N", scale=alt.Scale(
            domain=["High Value", "Medium Value", "Low Value"],
            range=["green", "lightblue", "red"]
        )),
        tooltip=["Customer", "Amount", "Segment"]
    ).properties(width=500, height=300)


def product_mix_share_chart(df: pd.DataFrame):
    """Show % of revenue by product line."""
    data = df.groupby("Product")["Amount"].sum().reset_index()

    return alt.Chart(data, title="Product Mix Share").mark_arc(innerRadius=60).encode(
        theta="Amount:Q",
        color="Product:N",
        tooltip=["Product", "Amount"]
    ).properties(width=350, height=300)