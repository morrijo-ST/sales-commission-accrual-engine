
import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def shell(name, title, subtitle, style):
    global PALETTE, INK, PANEL, BG, ACCENT
    themes = {
      'terminal': ('#091411','#10221d','#e7f5ee','#3fe0a0','#7e9c8d',4),
      'purple': ('#171625','#222137','#f5f1ff','#ba9bff','#9ca1c0',12),
      'indigo': ('#f4f5fb','#ffffff','#242746','#5149b9','#64708b',18),
      'coral': ('#faf7f2','#ffffff','#302a27','#c7543e','#796d65',20),
      'blue': ('#f2f6fa','#ffffff','#183348','#126bb5','#5d7486',8),
      'cyan': ('#07141d','#102330','#def5ff','#53d2ed','#8caab9',4),
      'ops': ('#0b1720','#132733','#e7f5f4','#4edbc4','#99b5bd',10),
      'editorial': ('#f8f7f3','#ffffff','#253b38','#317764','#6b7d77',6),
      'amber': ('#17212c','#223140','#f8f4e9','#efbc67','#a6b2bf',6),
    }
    BG,PANEL,INK,ACCENT,MUTED,RADIUS=themes[style]
    PALETTE=[ACCENT,'#4c9fd6','#d99455','#ae83c6','#6cae8b']
    px.defaults.color_discrete_sequence=PALETTE
    st.markdown(f"""<style>
    .stApp {{background:{BG};color:{INK}}}
    [data-testid="stHeader"] {{background:{BG};}}
    .block-container {{max-width:1480px;padding:2rem 2.5rem 4rem;}}
    [data-testid="stSidebar"] {{background:{PANEL};border-right:1px solid {MUTED}35;}}
    h1,h2,h3,p,label,[data-testid="stMarkdownContainer"], [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{color:{INK};}}
    h1 {{font-size:2.55rem!important;letter-spacing:-.055em;line-height:1.12!important;font-weight:650!important;}}
    h2,h3 {{letter-spacing:-.025em;}}
    [data-testid="stCaptionContainer"] {{opacity:1!important;}}
    [data-testid="stCaptionContainer"] p {{color:{MUTED}!important;}}
    [data-tag] {{background:{ACCENT}25!important;color:{INK}!important;border:1px solid {ACCENT}50;}}
    [data-tag] span,[data-tag] button {{color:{INK}!important;}}
    [data-testid="stMetric"] {{background:{PANEL};border:1px solid {MUTED}30;border-top:2px solid {ACCENT};border-radius:{RADIUS}px;padding:18px 20px;}}
    [data-testid="stMetricValue"] {{font-variant-numeric:tabular-nums;font-size:1.8rem;}}
    [data-testid="stPlotlyChart"] {{background:{PANEL};border:1px solid {MUTED}30;border-radius:{RADIUS}px;overflow:hidden;}}
    [data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"], textarea {{background:{PANEL}!important;color:{INK}!important;}}
    input,textarea {{color:{INK}!important;-webkit-text-fill-color:{INK}!important;}}
    [data-baseweb="tag"] {{background:{ACCENT}25!important;color:{INK}!important;}}
    [data-baseweb="tag"] span {{color:{INK}!important;}}
    button[kind="secondary"], [data-testid="stDownloadButton"] button {{background:{PANEL};color:{INK};border-color:{MUTED}65;}}
    [data-baseweb="tab"] {{color:{INK}!important;}}
    [data-testid="stAlert"] {{background:{PANEL};color:{INK};}}
    .eyebrow {{font:600 11px ui-monospace,monospace;letter-spacing:.15em;color:{ACCENT};margin-bottom:16px;}}
    .hero {{border-bottom:1px solid {MUTED}40;padding:12px 0 25px;margin-bottom:24px;}}
    .hero p {{max-width:850px;color:{MUTED};font-size:1rem;}}
    .brief {{border-left:3px solid {ACCENT};background:{PANEL};padding:16px 20px;margin:18px 0;color:{INK};}}
    @media(max-width:700px){{.block-container{{padding:1rem;}}h1{{font-size:1.8rem!important;}}}}
    </style>""",unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><div class="eyebrow">MORRIS / {html.escape(name.upper())} · SYNTHETIC DEMO</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',unsafe_allow_html=True)
    st.sidebar.caption('MORRIS · PORTFOLIO LAB')
    st.sidebar.caption('Fictional data. Explore the workflow; no external systems are connected.')

def chart(fig, height=340):
    for axis in [fig.layout.xaxis,fig.layout.yaxis]:
        if axis.title.text:axis.title.text=axis.title.text.replace('_',' ').title()
    for trace in fig.data:
        if trace.name:trace.name=trace.name.replace('_',' ').title()
    fig.update_layout(template='plotly_white',paper_bgcolor=PANEL,plot_bgcolor=PANEL,font=dict(color=INK,size=12),colorway=PALETTE,height=height,margin=dict(l=55,r=25,t=55,b=55),legend=dict(orientation='h',y=-.24,x=0),hoverlabel=dict(bgcolor=PANEL,font_color=INK))
    fig.update_xaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    fig.update_yaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    st.plotly_chart(fig,use_container_width=True,theme=None)

def brief(text):
    st.markdown('<div class="brief">'+html.escape(text)+'</div>',unsafe_allow_html=True)

def money(value):
    sign='−' if value<0 else ''
    return f'{sign}${abs(value)/1e6:,.2f}M' if abs(value)>=1e6 else f'{sign}${abs(value):,.0f}'

def metrics(items):
    for col,(label,value) in zip(st.columns(len(items)),items):col.metric(label,value)

def table(df, name='detail', height=360):
    config={}
    for col in df.columns:
        label=str(col).replace('_',' ').title()
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            if any(x in str(col) for x in ['pct','margin','confidence','attainment','probability','achievement']):
                config[col]=st.column_config.NumberColumn(label,format='%.3f')
            elif any(x in str(col) for x in ['amount','revenue','arr','acv','cost','expense','cash','earned','capitalized','amortization','balance','asset','budget','forecast','variance','value','backlog','receipts','payroll','subcontractor','materials','labor']):
                config[col]=st.column_config.NumberColumn(label,format='$%.2f')
            else:config[col]=st.column_config.NumberColumn(label)
        else:config[col]=st.column_config.Column(label)
    st.dataframe(df,use_container_width=True,hide_index=True,height=height,column_config=config)
    st.download_button('Download '+name.replace('_',' ')+' CSV',df.to_csv(index=False),name+'.csv','text/csv',key='export_'+name)

def nonempty(df):
    if df.empty:
        st.info('No records in this selection. Choose at least one filter value to continue.')
        st.stop()

import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Commission Accrual Engine",layout="wide")
shell('COMMISSION LEDGER','From earned to settled.','Follow monthly liabilities, capitalized cohorts, amortization, and cash payouts through the close.','indigo')
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
# Straight-line cohorts: amortization begins in the creation month.
amort=[]
for i in range(len(df)):
    amort.append(sum(df.capitalized.iloc[:i+1]/life))
df["amortization"]=amort
df["pnl_expense"]=df.current_expense+df.amortization
df["cash_paid"]=df.earned.shift(payout_lag).fillna(0)
df["accrual_balance"]=df.earned-df.cash_paid
df["commission_asset"]=df.capitalized.cumsum()-df.amortization.cumsum()
df["true_up_flag"]=df.accrual_balance.abs()>750000


# Liability is cumulative earned less cumulative cash, not the monthly movement.
df['accrual_movement']=df.earned-df.cash_paid
df['accrual_balance']=df.accrual_movement.cumsum()
df['true_up_flag']=df.accrual_movement.abs()>750000
selected=st.sidebar.selectbox('Review month',df.month.dt.strftime('%Y-%m').tolist(),index=len(df)-1)
idx=df.index[df.month.dt.strftime('%Y-%m')==selected][0]
latest=df.loc[idx]
metrics([('Earned this month',money(latest.earned)),('P&L this month',money(latest.pnl_expense)),('Closing asset',money(latest.commission_asset)),('Outstanding liability',money(latest.accrual_balance))])
brief(f"Reviewing {selected}. Opening balances are zero in this simulation. Capitalization begins amortizing in the month earned; cash follows earned commissions by {payout_lag} month(s).")
a,b=st.columns([1.65,1])
with a:
    chart(px.line(df.iloc[:idx+1],x='month',y=['earned','pnl_expense','cash_paid'],title='Monthly flows · earned / expense / cash'))
with b:
    st.subheader('Liability roll-forward')
    opening_liability=df.accrual_balance.iloc[idx-1] if idx else 0
    st.write(f'Opening payable: **{money(opening_liability)}**')
    st.write(f'+ Earned: **{money(latest.earned)}**')
    st.write(f'− Cash paid: **{money(latest.cash_paid)}**')
    st.write(f'= Closing payable: **{money(latest.accrual_balance)}**')
    st.caption('A large monthly movement is a review signal, not evidence that an accounting true-up is required.')
ledger,cohorts=st.tabs(['Monthly ledger','Capitalized cohorts'])
with ledger:table(df,'commission_ledger')
with cohorts:
    matrix=pd.DataFrame(0.0,index=df.month.dt.strftime('%Y-%m'),columns=df.month.dt.strftime('%Y-%m'))
    for i in range(len(df)):
        for j in range(i,min(i+life,len(df))):matrix.iloc[i,j]=df.capitalized.iloc[i]/life
    chart(px.imshow(matrix,aspect='auto',color_continuous_scale='Purples',labels={'x':'Expense month','y':'Earned cohort','color':'Amortization'},title='Cohort amortization schedule'),470)
    table(matrix.reset_index(names='cohort'),'cohort_amortization')
