
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

# LOAD DATA
@st.cache_data
def load_data():
    data = pd.read_csv("ecommerce_sales_cleaned.csv")
    data["order_date"] = pd.to_datetime(data["order_date"])
    return data

df = load_data()


# PREMIUM DARK THEME CSS
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: #0B1120;
    color: #F1F5F9;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #111C30;
    border-right: 1px solid #263750;
}

[data-testid="stSidebar"] label {
    color: #DCE6F2 !important;
}

/* MAIN HEADER */
h1 {
    color: #FFFFFF !important;
    font-size: 38px !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #E2E8F0 !important;
    font-weight: 700 !important;
}

/* KPI CARDS */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #17263D, #1D304A);
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #29445F;
    box-shadow: 0 4px 15px rgba(0,0,0,0.20);
}

/* KPI LABEL */
[data-testid="stMetricLabel"] {
    color: #B8C7D9 !important;
    font-size: 15px !important;
}

/* KPI VALUE */
[data-testid="stMetricValue"] {
    color: #00E5CC !important;
    font-size: 30px !important;
    font-weight: 750 !important;
}

/* FILTERS */
[data-baseweb="select"] > div {
    background-color: #1B2A40;
    border-color: #344B68;
    color: white;
}

/* SELECTED FILTER TAGS */
[data-baseweb="tag"] {
    background-color: #087F8C !important;
    color: white !important;
}

/* INPUTS */
input {
    color: white !important;
}

/* DIVIDERS */
hr {
    border-color: #34445B !important;
}

/* CAPTION */
.stCaption {
    color: #94A3B8 !important;
}

/* DATA TABLE */
[data-testid="stDataFrame"] {
    border: 1px solid #29445F;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# PROFESSIONAL PLOTLY CHART THEME

def style_chart(fig):

    fig.update_layout(
        paper_bgcolor="#0B1120",
        plot_bgcolor="#111C30",
        font=dict(
            color="#E2E8F0",
            family="Arial",
            size=12
        ),
        title_font=dict(
            color="#FFFFFF",
            size=18
        ),
        legend=dict(
            font=dict(color="#E2E8F0")
        ),
        margin=dict(l=30, r=30, t=60, b=40)
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#263750",
        zerolinecolor="#34445B"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#263750",
        zerolinecolor="#34445B"
    )

    return fig


# HEADER
st.title("🛒 E-Commerce Sales Dashboard")
st.caption("Business Intelligence | Sales | Profit | Customer Analytics")

st.divider()

# SIDEBAR FILTERS
st.sidebar.title("Dashboard Filters")

categories = st.sidebar.multiselect(
    "Product Category",
    df["product_category"].unique(),
    default=df["product_category"].unique()
)

states = st.sidebar.multiselect(
    "State",
    df["state"].unique(),
    default=df["state"].unique()
)

statuses = st.sidebar.multiselect(
    "Order Status",
    df["order_status"].unique(),
    default=df["order_status"].unique()
)

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# APPLY FILTERS
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df["product_category"].isin(categories)) &
    (df["state"].isin(states)) &
    (df["order_status"].isin(statuses)) &
    (df["order_date"].dt.date >= start_date) &
    (df["order_date"].dt.date <= end_date)
].copy()

delivered = filtered[
    filtered["order_status"] == "Delivered"
]

# KPI CALCULATIONS
total_sales = delivered["sales"].sum()
total_profit = delivered["profit"].sum()
total_orders = filtered["order_id"].nunique()
total_customers = filtered["customer_id"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

# KPI CARDS
st.subheader("📊 Business Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"₹{total_sales:,.0f}")
c2.metric("Total Profit", f"₹{total_profit:,.0f}")
c3.metric("Total Orders", f"{total_orders:,}")
c4.metric("Profit Margin", f"{profit_margin:.2f}%")

c5, c6 = st.columns(2)

c5.metric("Total Customers", f"{total_customers:,}")
c6.metric("Delivered Orders", f"{len(delivered):,}")

st.divider()

# MONTHLY SALES TREND
st.subheader("📈 Monthly Sales Trend")

monthly = (
    delivered.groupby(
        delivered["order_date"].dt.to_period("M")
    )["sales"].sum().reset_index()
)

monthly["Month"] = monthly["order_date"].astype(str)


fig1 = px.line(
    monthly,
    x="Month",
    y="sales",
    markers=True,
    title="Monthly Revenue Trend",
    template="plotly_dark",
    color_discrete_sequence=["#00E5CC"]
)

fig1.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

fig1 = style_chart(fig1)

st.plotly_chart(fig1, use_container_width=True)


# CATEGORY AND STATE ANALYSIS
col1, col2 = st.columns(2)

with col1:
    st.subheader("Category-wise Sales")

    category = (
        delivered.groupby("product_category")["sales"]
        .sum().reset_index()
    )

    
fig2 = px.pie(
    category,
    names="product_category",
    values="sales",
    hole=0.58,
    title="Sales Distribution by Category",
    template="plotly_dark",
    color_discrete_sequence=[
        "#00E5CC",
        "#4776E6",
        "#A855F7",
        "#FF9F43",
        "#FF5C8A"
    ]
)

fig2.update_traces(
    textposition="inside",
    textinfo="percent+label",
    marker=dict(
        line=dict(
            color="#111C30",
            width=3
        )
    )
)

fig2 = style_chart(fig2)

st.plotly_chart(fig2, use_container_width=True)


with col2:
    st.subheader("State-wise Revenue")

    state = (
        delivered.groupby("state")["sales"]
        .sum().nlargest(10).reset_index()
    )

   
fig3 = px.bar(
    state,
    x="sales",
    y="state",
    orientation="h",
    title="Revenue by State",
    template="plotly_dark",
    color="sales",
    color_continuous_scale=[
        "#123B50",
        "#00C9A7",
        "#00E5CC"
    ]
)

fig3.update_layout(
    coloraxis_showscale=False,
    yaxis=dict(
        autorange="reversed"
    ),
    bargap=0.35
)

fig3.update_traces(
    marker_line_width=0
)

fig3 = style_chart(fig3)

st.plotly_chart(fig3, use_container_width=True)


# TOP PRODUCTS
st.subheader("🏆 Top 10 Products")

products = (
    delivered.groupby("product_name")["quantity"]
    .sum().nlargest(10).reset_index()
)


fig4 = px.bar(
    products.sort_values("quantity", ascending=True),
    x="quantity",
    y="product_name",
    orientation="h",
    title="Top 10 Products by Quantity Sold",
    template="plotly_dark",
    color="quantity",
    color_continuous_scale=[
        "#312E81",
        "#7C3AED",
        "#C084FC"
    ]
)

fig4.update_layout(
    coloraxis_showscale=False,
    bargap=0.35
)

fig4.update_traces(
    marker_line_width=0
)

fig4 = style_chart(fig4)

st.plotly_chart(fig4, use_container_width=True)

# ORDER STATUS

status_data = filtered["order_status"].value_counts().reset_index()
status_data.columns = ["order_status", "orders"]

fig5 = px.pie(
    status_data,
    names="order_status",
    values="orders",
    hole=0.60,
    title="Order Status Distribution",
    template="plotly_dark",
    color="order_status",
    color_discrete_map={
        "Delivered": "#00E5CC",
        "Cancelled": "#FF4D6D",
        "Returned": "#A855F7",
        "Processing": "#FFB020"
    }
)

fig5.update_traces(
    textposition="inside",
    textinfo="label+percent",
    marker=dict(
        line=dict(color="#0B1220", width=3)
    )
)

fig5 = style_chart(fig5)

st.plotly_chart(fig5, use_container_width=True)




# CUSTOMER TABLE
st.subheader("👥 Top 10 Customers")

top_customers = (
    delivered.groupby("customer_id")["sales"]
    .sum().nlargest(10).reset_index()
)

top_customers.columns = ["Customer ID", "Revenue"]

st.dataframe(
    top_customers,
    use_container_width=True,
    hide_index=True
)

# FOOTER
st.divider()
st.caption("E-Commerce Sales Analytics | Python Portfolio Project")
