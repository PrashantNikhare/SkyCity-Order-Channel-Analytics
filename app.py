import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="SkyCity Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# =====================================
# Title
# =====================================

st.title("🍽️ SkyCity Auckland Restaurants & Bars")
st.write("Order Channel Performance and Market Share Analytics")

# =====================================
# Read Dataset
# =====================================

df = pd.read_csv("restaurants.csv")

# =====================================
# Sidebar Filters
# =====================================

st.sidebar.header("Filters")

st.sidebar.markdown("---")

st.sidebar.info("""
### About

SkyCity Auckland Restaurants & Bars

Order Channel Performance Dashboard

Developed using:

• Python

• Pandas

• Plotly

• Streamlit
""")

subregion = st.sidebar.multiselect(
    "Subregion",
    df["Subregion"].unique(),
    default=df["Subregion"].unique()
)

cuisine = st.sidebar.multiselect(
    "Cuisine",
    df["CuisineType"].unique(),
    default=df["CuisineType"].unique()
)

segment = st.sidebar.multiselect(
    "Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)

# =====================================
# Apply Filters
# =====================================

df_filtered = df[
    (df["Subregion"].isin(subregion)) &
    (df["CuisineType"].isin(cuisine)) &
    (df["Segment"].isin(segment))
]

# =====================================
# KPI Calculations
# =====================================

total_restaurants = len(df_filtered)

total_orders = df_filtered["MonthlyOrders"].sum()

average_aov = round(df_filtered["AOV"].mean(), 2)

average_profit = round(
    df_filtered[
        [
            "InStoreNetProfit",
            "UberEatsNetProfit",
            "DoorDashNetProfit",
            "SelfDeliveryNetProfit"
        ]
    ].sum(axis=1).mean(),
    2
)

# =====================================
# KPI Dashboard
# =====================================

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Restaurants", total_restaurants)

col2.metric("Monthly Orders", f"{total_orders:,}")

col3.metric("Average AOV ($)", average_aov)

col4.metric("Average Profit ($)", average_profit)

# =====================================
# Orders by Channel
# =====================================

st.markdown("---")
st.subheader("📊 Total Orders by Channel")

channel_orders = pd.DataFrame({
    "Channel": [
        "In-Store",
        "Uber Eats",
        "DoorDash",
        "Self Delivery"
    ],
    "Orders": [
        df_filtered["InStoreOrders"].sum(),
        df_filtered["UberEatsOrders"].sum(),
        df_filtered["DoorDashOrders"].sum(),
        df_filtered["SelfDeliveryOrders"].sum()
    ]
})

fig = px.bar(
    channel_orders,
    x="Channel",
    y="Orders",
    color="Channel",
    text="Orders",
    title="Total Orders by Channel"
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

# =====================================
# Market Share by Channel
# =====================================

st.subheader("🥧 Market Share by Channel")

fig = px.pie(
    channel_orders,
    names="Channel",
    values="Orders",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# =====================================
# Geographic Analysis
# =====================================

st.markdown("---")
st.subheader("🌍 Orders by Subregion")

subregion_orders = (
    df_filtered.groupby("Subregion")["MonthlyOrders"]
    .sum()
    .reset_index()
)

fig = px.bar(
    subregion_orders,
    x="Subregion",
    y="MonthlyOrders",
    color="Subregion",
    text="MonthlyOrders",
    title="Total Monthly Orders by Subregion"
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Subregion Summary")

st.dataframe(
    subregion_orders,
    use_container_width=True
)

best_subregion = subregion_orders.sort_values(
    "MonthlyOrders",
    ascending=False
).iloc[0]

st.success(
    f"🏆 Best Performing Subregion: {best_subregion['Subregion']} "
    f"({int(best_subregion['MonthlyOrders']):,} Orders)"
)

# =====================================
# Cuisine Analysis
# =====================================

st.markdown("---")
st.subheader("🍕 Orders by Cuisine")

cuisine_orders = (
    df_filtered.groupby("CuisineType")["MonthlyOrders"]
    .sum()
    .reset_index()
)

fig = px.bar(
    cuisine_orders,
    x="CuisineType",
    y="MonthlyOrders",
    color="CuisineType",
    text="MonthlyOrders",
    title="Total Monthly Orders by Cuisine"
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Cuisine Summary")

st.dataframe(
    cuisine_orders,
    use_container_width=True
)

top_cuisine = cuisine_orders.sort_values(
    "MonthlyOrders",
    ascending=False
).iloc[0]

st.success(
    f"🏆 Top Performing Cuisine: {top_cuisine['CuisineType']} "
    f"({int(top_cuisine['MonthlyOrders']):,} Orders)"
)

st.subheader("🥧 Cuisine Market Share")

fig = px.pie(
    cuisine_orders,
    names="CuisineType",
    values="MonthlyOrders",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)
st.info(
    "This chart compares monthly orders across different cuisine types to identify customer preferences."
)

# =====================================
# Segment Analysis
# =====================================

st.markdown("---")
st.subheader("☕ Orders by Business Segment")

segment_orders = (
    df_filtered.groupby("Segment")["MonthlyOrders"]
    .sum()
    .reset_index()
)

fig = px.bar(
    segment_orders,
    x="Segment",
    y="MonthlyOrders",
    color="Segment",
    text="MonthlyOrders",
    title="Total Monthly Orders by Business Segment"
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

st.info(
    "This chart compares monthly orders across different business segments."
)
st.subheader("📋 Segment Summary")

st.dataframe(
    segment_orders,
    use_container_width=True
)

top_segment = segment_orders.sort_values(
    "MonthlyOrders",
    ascending=False
).iloc[0]

st.success(
    f"🏆 Best Performing Segment: {top_segment['Segment']} "
    f"({int(top_segment['MonthlyOrders']):,} Orders)"
)

st.subheader("🥧 Segment Market Share")

fig = px.pie(
    segment_orders,
    names="Segment",
    values="MonthlyOrders",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# =====================================
# Channel Dependency Risk Analysis
# =====================================

st.markdown("---")
st.subheader("🚨 Channel Dependency Risk Analysis")

df_filtered["AggregatorDependence"] = (
    (
        df_filtered["UberEatsOrders"] +
        df_filtered["DoorDashOrders"]
    )
    /
    df_filtered["MonthlyOrders"]
) * 100

high_risk = len(
    df_filtered[
        df_filtered["AggregatorDependence"] >= 70
    ]
)

average_dependency = round(
    df_filtered["AggregatorDependence"].mean(),
    2
)

highest_dependency = round(
    df_filtered["AggregatorDependence"].max(),
    2
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "High Risk Restaurants",
    high_risk
)

col2.metric(
    "Average Dependency %",
    average_dependency
)

col3.metric(
    "Highest Dependency %",
    highest_dependency
)

st.subheader("🔴 Restaurants with High Aggregator Dependency")

risk_table = df_filtered[
    df_filtered["AggregatorDependence"] >= 70
][[
    "RestaurantName",
    "CuisineType",
    "Subregion",
    "AggregatorDependence"
]]

st.dataframe(
    risk_table,
    use_container_width=True
)

st.subheader("🏆 Top 10 Highest Dependency Restaurants")

top10 = df_filtered.sort_values(
    "AggregatorDependence",
    ascending=False
)[[
    "RestaurantName",
    "AggregatorDependence",
    "CuisineType",
    "Subregion"
]].head(10)

st.dataframe(
    top10,
    use_container_width=True
)

st.subheader("💡 Business Insights")

st.info("""
• Restaurants with dependency above 70% are highly dependent on third-party delivery platforms.

• High dependency may reduce profitability because of commission charges.

• Restaurants should improve In-Store and Self Delivery channels to reduce dependency.

• Balanced channel distribution improves long-term business stability.
""")

st.markdown("---")

st.subheader("📥 Download Filtered Dataset")

csv = df_filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    data=csv,
    file_name="SkyCity_Filtered_Data.csv",
    mime="text/csv"
)
