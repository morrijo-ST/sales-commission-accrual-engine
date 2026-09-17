import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Commission Accrual Engine",layout="wide")
st.title("Sales Commission Accrual Engine")
st.caption("Synthetic monthly accrual, capitalization, cohort amortization, payout timing, and close true-up.")
random.seed(31)
months=pd.date_range("2026-01-01",periods=18,freq="MS")
cap_rate=st.sidebar.slider("Capitalization rate",0.30,0.65,0.50,0.01)
life=st.sidebar.slider("Amortization life (months)",24,72,48,1)
payout_lag=st.sidebar.slider("Cash payout lag (months)",1,3,1,1)
rows=[]
for m in months:
    earned=random.uniform(1.7,3.4)*1e6
    rows.append([m,earned])
df=pd.DataFrame(rows,columns=["month","earned"])
df["capitalized"]=df.earned*cap_rate
df["current_expense"]=df.earned-df.capitalized
# Cohort amortization approximation: each prior capitalized cohort contributes cap/life per month after creation
amort=[]
for i in range(len(df)):
    amort.append(sum(df.capitalized.iloc[:i+1]/life))
df["amortization"]=amort
df["pnl_expense"]=df.current_expense+df.amortization
df["cash_paid"]=df.earned.shift(payout_lag).fillna(0)
df["accrual_balance"]=df.earned-df.cash_paid
df["commission_asset"]=df.capitalized.cumsum()-df.amortization.cumsum()
df["true_up_flag"]=df.accrual_balance.abs()>750000

latest=df.iloc[-1]
c1,c2,c3,c4=st.columns(4)
c1.metric("Latest Earned",f"${latest.earned/1e6:,.2f}M")
c2.metric("Latest P&L Expense",f"${latest.pnl_expense/1e6:,.2f}M")
c3.metric("Commission Asset",f"${latest.commission_asset/1e6:,.2f}M")
c4.metric("Accrual Balance",f"${latest.accrual_balance/1e6:+.2f}M")

st.subheader("Earned vs expense vs cash")
st.plotly_chart(px.line(df,x="month",y=["earned","pnl_expense","cash_paid"],markers=True),use_container_width=True)

left,right=st.columns(2)
with left:
    st.subheader("Capitalized asset roll-forward")
    st.plotly_chart(px.area(df,x="month",y="commission_asset"),use_container_width=True)
with right:
    st.subheader("Accrual / cash timing")
    st.plotly_chart(px.bar(df,x="month",y="accrual_balance",color="true_up_flag"),use_container_width=True)

st.subheader("Month-end close review")
st.dataframe(df[["month","earned","capitalized","amortization","pnl_expense","cash_paid","accrual_balance","commission_asset","true_up_flag"]].tail(12),use_container_width=True,hide_index=True)
st.info("The public demo uses a simplified straight-line cohort model to demonstrate accounting mechanics. A production engine would retain rep/deal-level cohorts, policy attribution, reversals, term changes, and system-of-record tie-outs.")
