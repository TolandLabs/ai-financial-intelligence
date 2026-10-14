import pandas as pd
import plotly.express as px
import streamlit as st
from finance import validate, monthly, runway, scenario, insights

st.set_page_config(page_title="Financial Intelligence", layout="wide")
st.title("Financial Intelligence | CFO Cockpit")
st.caption("Synthetic-data demonstration. Automated insights are rules-based, not generative AI.")
upload = st.file_uploader("Financial CSV (optional)", type="csv")
try:
    df = validate(pd.read_csv(upload if upload else "data/sample_financials.csv"))
except (ValueError, pd.errors.ParserError, UnicodeDecodeError) as exc:
    st.error(f"Invalid data: {exc}")
    st.stop()

trend = monthly(df)
cash = st.number_input("Starting cash ($)", min_value=0.0, value=800000.0, step=10000.0)
net_flow = trend.operating_result.tail(3).mean()
months = runway(cash, net_flow)
a, b, c = st.columns(3)
a.metric("Latest operating result", f"${trend.operating_result.iloc[-1]:,.0f}")
b.metric("Variance to budget", f"${trend.operating_result.iloc[-1] - trend.budget_result.iloc[-1]:+,.0f}")
c.metric("Illustrative runway", "No net burn" if months is None else f"{months:.1f} months")
st.plotly_chart(px.line(trend, x="month", y=["operating_result", "budget_result"]), use_container_width=True)
st.subheader("Scenarios")
growth = st.slider("Revenue change (%)", -50, 100, 10) / 100
costs = st.slider("Expense change (%)", -50, 100, 0) / 100
st.metric("Scenario operating result (all periods)", f"${scenario(df, growth, costs):,.0f}")
st.subheader("Automated insights")
for note in insights(df):
    st.write("- " + note)
st.caption("Not accounting, tax, or investment advice.")
