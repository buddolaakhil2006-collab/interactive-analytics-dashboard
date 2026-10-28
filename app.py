from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="CodeNova | Interactive Sales Analytics", page_icon="📊", layout="wide")
DATA = Path(__file__).parent / "data" / "sales_data.csv"

@st.cache_data
def load_data():
    d = pd.read_csv(DATA, parse_dates=["order_date"])
    for col in ["sales", "profit", "units"]:
        d[col] = pd.to_numeric(d[col], errors="coerce")
    return d.dropna(subset=["order_date", "sales", "profit", "units"])

df = load_data()
st.title("📊 Interactive Sales Analytics")
st.caption("CodeNova Data Science · Task 3 · Synthetic retail transactions, 2023–2025")
with st.sidebar:
    st.header("Explore the data")
    lo, hi = df.order_date.min().date(), df.order_date.max().date()
    dates = st.date_input("Order date range", value=(lo, hi), min_value=lo, max_value=hi)
    categories = st.multiselect("Product categories", sorted(df.category.unique()), default=sorted(df.category.unique()))
    regions = st.multiselect("Regions", sorted(df.region.unique()), default=sorted(df.region.unique()))
    threshold = st.slider("Minimum line-item sales ($)", 0, int(df.sales.max()), 0, step=25)

if len(dates) != 2:
    st.info("Choose both a start and end date to view the dashboard.")
    st.stop()
start, end = pd.Timestamp(dates[0]), pd.Timestamp(dates[1]) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
f = df[(df.order_date >= start) & (df.order_date <= end) & df.category.isin(categories) & df.region.isin(regions) & (df.sales >= threshold)].copy()
st.caption(f"Showing {len(f):,} of {len(df):,} line items · {dates[0]} through {dates[1]}")
if f.empty:
    st.info("No matching records. Try widening the date range, selecting more categories or regions, or lowering the sales threshold.")
    st.stop()
revenue, profit, units = f.sales.sum(), f.profit.sum(), f.units.sum()
margin = profit / revenue if revenue else 0
aov = revenue / f.order_id.nunique() if f.order_id.nunique() else 0
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Gross revenue", f"${revenue:,.0f}")
c2.metric("Profit", f"${profit:,.0f}")
c3.metric("Profit margin", f"{margin:.1%}")
c4.metric("Average order value", f"${aov:,.2f}")
c5.metric("Units sold", f"{units:,.0f}")
monthly = f.set_index("order_date").resample("MS").agg(revenue=("sales","sum")).reset_index()
bycat = f.groupby("category",as_index=False).agg(revenue=("sales","sum"),profit=("profit","sum"),units=("units","sum"))
left,right = st.columns(2)
with left:
    st.subheader("Revenue over time")
    st.plotly_chart(px.line(monthly,x="order_date",y="revenue",markers=True,labels={"order_date":"Month","revenue":"Revenue ($)"},template="plotly_white"),use_container_width=True)
with right:
    st.subheader("Category performance")
    st.plotly_chart(px.bar(bycat,x="category",y="revenue",color="category",labels={"category":"Category","revenue":"Revenue ($)"},template="plotly_white"),use_container_width=True,showlegend=False)
left,right = st.columns(2)
with left:
    st.subheader("Sales and profit by order")
    st.plotly_chart(px.scatter(f,x="sales",y="profit",color="category",hover_data=["order_id","region","units"],labels={"sales":"Sales ($)","profit":"Profit ($)"},template="plotly_white"),use_container_width=True)
with right:
    st.subheader("Regional sales mix")
    regional = f.groupby("region",as_index=False).sales.sum().sort_values("sales",ascending=False)
    st.plotly_chart(px.bar(regional,x="region",y="sales",color="region",labels={"region":"Region","sales":"Revenue ($)"},template="plotly_white"),use_container_width=True,showlegend=False)
with st.expander("View filtered records"):
    st.dataframe(f.sort_values("order_date",ascending=False),use_container_width=True,hide_index=True)
st.caption("Illustrative synthetic data only. Filtered AOV is filtered revenue divided by distinct filtered orders.")
