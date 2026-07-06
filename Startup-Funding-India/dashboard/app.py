import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Startup Funding Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Data
df = pd.read_csv("data/cleaned/cleaned_startup_funding.csv")
df["Date"]=pd.to_datetime(df["Date"])
df["Year"]=df["Date"].dt.year

# Title
st.title("📊 Startup Funding Analysis in India")

st.write("Interactive Dashboard")

# Show Dataset
st.subheader("Dataset Preview")
st.dataframe(df.head())
# KPI Cards
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Startups", df["Startup"].nunique())

with col2:
    st.metric("Total Investors", df["Investors"].nunique())

with col3:
    st.metric(
        "Total Funding (USD)",
        f"${df['InvestmentAmount_USD'].sum():,.0f}"
    )
    # Sidebar
st.sidebar.header("Filters")

selected_city = st.sidebar.selectbox(
    "Select City",
    ["All"] + sorted(df["City"].unique().tolist())
)

selected_industry = st.sidebar.selectbox(
    "Select Industry",
    ["All"] + sorted(df["Industry"].unique().tolist())
)
filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

if selected_industry != "All":
    filtered_df = filtered_df[filtered_df["Industry"] == selected_industry]
    industry = (
    filtered_df["Industry"]
    .value_counts()
    .head(10)
    .reset_index()
)
    # Year Filter
 
years = sorted(df["Year"].dropna().unique())
selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + list(years)
)

# Investment Type Filter
investment_types = sorted(df["InvestmentType"].dropna().unique())

selected_investment = st.sidebar.selectbox(
    "Select Investment Type",
    ["All"] + list(investment_types)
)
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year ]

if selected_investment != "All":
    filtered_df = filtered_df[
        filtered_df["InvestmentType"] == selected_investment
    ]
investment = (
    filtered_df["InvestmentType"]
    .value_counts()
    .reset_index()
    )
investment.columns = ["InvestmentType", "Count"]
fig = px.pie(
    investment,
    names="InvestmentType",
    values="Count",
    title="Investment Types"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Investors")

top_investors = (
    filtered_df["Investors"]
    .value_counts()
    .head(10)
)

st.dataframe(filtered_df)
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig, use_container_width=True, key="pie_chart")


    import plotly.express as px

industry = (
    filtered_df["Industry"]
    .value_counts()
    .head(10)
    .reset_index()
)

industry.columns = ["Industry", "Count"]

fig = px.bar(
    industry,
    x="Industry",
    y="Count",
    title="Top 10 Industries"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Startups", df["Startup"].nunique())

col2.metric("Total Investors", df["Investors"].nunique())

col3.metric(
    "Total Funding",
    f"${df['InvestmentAmount_USD'].sum():,.0f}"
)
industry = (
    filtered_df["Industry"]
    .value_counts()
    .head(10)
    .reset_index()
)

industry.columns = ["Industry", "Count"]

fig = px.bar(
     industry,
    x="Industry",
    y="Count",
    color="Count",
    title="Top 10 Industries"
)

st.plotly_chart(fig, use_container_width=True)
city = (
    df["City"]
    .value_counts()
    .head(10)
    .reset_index()
)

city.columns = ["City", "Count"]

fig = px.bar(
    city,
    x="City",
    y="Count",
    color="Count",
    title="Top 10 Startup Cities"
)

st.plotly_chart(fig, use_container_width=True)
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

trend = (
    df.groupby("Year")["InvestmentAmount_USD"]
    .sum()
    .reset_index()
)

fig = px.line(
    trend,
    x="Year",
    y="InvestmentAmount_USD",
    markers=True,
    title="Funding Trend Over Years"
)

st.plotly_chart(fig, use_container_width=True)