import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sponge City Readiness Index",
    layout="wide"
)

df = pd.read_csv(
    "scri_dashboard_data.csv"
)

st.title(
    "🌧 Sponge City Readiness Index (SCRI)"
)

st.markdown(
    """
    Climate Risk and Urban Resilience Analytics Platform
    """
)

#KPI CARDS 
col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Grid Cells",
    len(df)
)

col2.metric(
    "Average SCRI",
    round(df["scri"].mean(),3)
)

col3.metric(
    "Highest SCRI",
    round(df["scri"].max(),3)
)

col4.metric(
    "Critical Zones",
    (df["risk_tier"]=="Critical").sum()
)

#RISK FILTER
risk = st.selectbox(
    "Select Risk Tier",
    ["All"] + list(df["risk_tier"].unique())
)

if risk != "All":
    filtered = df[
        df["risk_tier"] == risk
    ]
else:
    filtered = df


#India Risk Map
fig = px.scatter_map(
    filtered,
    lat="lat",
    lon="lon",
    color="risk_tier",
    hover_data=[
        "scri",
        "mean_annual_rf",
        "heavy_days"
    ],
    zoom=3
)

st.plotly_chart(
    fig,
    use_container_width=True
)



fig = px.scatter_geo(
    filtered,
    lat="lat",
    lon="lon",
    color="risk_tier"
)



#SCRI Distribution
fig = px.histogram(
    filtered,
    x="scri",
    nbins=30,
    title="SCRI Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

#Risk Breakdown
fig = px.pie(
    filtered,
    names="risk_tier",
    title="Risk Tier Composition"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

#Feature Analysis
feature_cols = [
    "mean_annual_rf",
    "std_annual",
    "cv",
    "dry_days",
    "heavy_days"
]

feature = st.selectbox(
    "Select Feature",
    feature_cols
)

fig = px.histogram(
    filtered,
    x=feature,
    color="risk_tier"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


#Raw Data Explorer
st.subheader(
    "SCRI Dataset"
)

st.dataframe(
    filtered
)