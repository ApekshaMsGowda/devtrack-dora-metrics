import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="DevTrack - DORA Metrics",
    page_icon="🚀",
    layout="wide"
)

# Dashboard heading
st.title("🚀 DevTrack")
st.subheader("DORA Metrics & Engineering Velocity Tracker")

st.write(
    "Monitor software delivery performance "
    "using engineering activity data."
)

# Load data from CSV
DATA_FILE = "data/dora_metrics.csv"

df = pd.read_csv(DATA_FILE)
df["date"] = pd.to_datetime(df["date"])

# Date range filter
st.sidebar.header("Dashboard Filters")

start_date = st.sidebar.date_input(
    "Start date",
    df["date"].min().date()
)

end_date = st.sidebar.date_input(
    "End date",
    df["date"].max().date()
)

if start_date > end_date:
    st.error("Start date cannot be after end date.")
    st.stop()

df = df[
    (df["date"].dt.date >= start_date)
    & (df["date"].dt.date <= end_date)
]

if df.empty:
    st.warning("No data available for the selected dates.")
    st.stop()

# Calculate DORA metrics
total_deployments = df["deployments"].sum()

total_failures = df["failed_deployments"].sum()

total_records = len(df)

average_lead_time = df["lead_time_hours"].mean()

change_failure_rate = (
    total_failures / total_deployments * 100
    if total_deployments > 0
    else 0
)

average_recovery_time = df.loc[
    df["failed_deployments"] > 0,
    "recovery_time_minutes"
].mean()

if pd.isna(average_recovery_time):
    average_recovery_time = 0

# Display metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🚀 Total Deployments",
    int(total_deployments)
)
col2.metric(
    "⏱️ Average Lead Time",
    f"{average_lead_time:.1f} hours"
)

col3.metric(
    "⚠️ Change Failure Rate",
    f"{change_failure_rate:.1f}%"
)

col4.metric(
    "🔧 Average Recovery Time",
    f"{average_recovery_time:.1f} minutes"
)

# Deployment activity chart
st.subheader("📊 Daily Deployment Activity")

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df["date"],
        y=df["deployments"],
        name="Deployments"
    )
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Deployments",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Failure chart
st.subheader("⚠️ Daily Deployment Failures")

failure_fig = go.Figure()

failure_fig.add_trace(
    go.Bar(
        x=df["date"],
        y=df["failed_deployments"],
        name="Failed Deployments"
    )
)

failure_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Failed Deployments",
    template="plotly_white"
)

st.plotly_chart(
    failure_fig,
    use_container_width=True
)

# Display underlying data
st.subheader("📋 Engineering Activity Records")

st.dataframe(df, use_container_width=True)

# Information
st.info(
    "This dashboard currently uses simulated data. "
    "GitHub integration will be added in a later stage."
)