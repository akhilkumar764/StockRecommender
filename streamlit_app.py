import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import plotly.express as px

st.set_page_config(page_title="Stock Portfolio Analyzer", layout="wide")

# INEVITABLE SECTORS
SECTORS = {
    'Defense': ['HAL', 'BEL', 'RVNL', 'IRCON', 'BEML', 'MAZAGON', 'GRSE', 'COCHINSHIP'],
    'Green Energy': ['TATAPOWER', 'JSWENERGY', 'ADANIGREEN', 'KPIGREEN', 'RENEWPOWER', 'SUZLON', 'INOXWIND'],
    'EV': ['TATAMOTORS', 'EXIDEIND', 'AMARARAJA', 'MOTHERSON', 'MINDA', 'BHARATFORGE', 'SAMVARDHANA'],
    'Data Centers': ['BHARTIARTL', 'TATACOMM', 'ROUTE', 'TATAELXSI', 'LTTS', 'PERSISTENT', 'COFORGE'],
    'Railways': ['RVNL', 'IRCON', 'IRCTC', 'TEXRAIL', 'RAILTEL', 'TITAGARH', 'JUPITER']
}

GROUPS = ['TATA', 'ADANI', 'JSW', 'RELIANCE', 'BIRLA']

@st.cache_data(ttl=86400)
def generate_universe():
    np.random.seed(42)
    stocks = []
    
    for sector, symbols in SECTORS.items():
        for symbol in symbols:
            stocks.append({
                'symbol': symbol,
                'sector': sector,
                'group': np.random.choice(GROUPS, p=[0.25, 0.2, 0.15, 0.2, 0.2]),
                'mcap': np.random.uniform(2000, 80000),
                'roe': np.random.uniform(12, 35),
                'roce': np.random.uniform(15, 32),
                'sales_3yr': np.random.uniform(10, 28),
                'profit_3yr': np.random.uniform(12, 30),
                'opm': np.random.uniform(10, 28),
                'promoter': np.random.uniform(50, 75),
                'debt_eq': np.random.uniform(0.1, 1.8),
                'ceo_score': np.random.uniform(6, 10),
                'scuttlebutt_score': np.random.uniform(6, 10)
            })
    
    return pd.DataFrame(stocks)

def calculate_score(row):
    score = 0
    score += 2
    if row['roe'] > 20 and row['sales_3yr'] > 15: score += 3
    if row['group'] in ['TATA', 'ADANI', 'JSW']: score += 3
    if row['ceo_score'] > 8: score += 2
    if row['scuttlebutt_score'] > 8: score += 2
    if row['promoter'] > 55: score += 1
    if row['debt_eq'] < 1: score += 1
    if row['mcap'] > 5000: score += 1
    return score

def assign_weights(n):
    if n == 0: return []
    elif n <= 5: return [30, 25, 20, 15, 10][:n]
    elif n <= 10: return [15, 13, 11, 10, 9, 8, 7, 6, 6, 5][:n]
    else: return [10, 9, 8, 7, 6, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2][:n]

def main():
    st.markdown("# **Stock Portfolio Analyzer**")
    
    universe = generate_universe()
    universe['score'] = universe.apply(calculate_score, axis=1)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Stocks", f"{len(universe)}")
    with col2: st.metric("Portfolio", "Dynamic")
    with col3: st.metric("Updated", datetime.now().strftime("%Y-%m-%d"))
    
    st.markdown("## **Select Sectors**")
    selected = st.multiselect(
        "Choose sectors",
        options=list(SECTORS.keys()),
        default=['Defense', 'Green Energy']
    )
    
    if selected:
        filtered = universe[universe['sector'].isin(selected)].copy()
        
        st.markdown("## **Portfolio**")
        n_stocks = st.slider("Portfolio Size", 5, 20, 15)
        portfolio = filtered.nlargest(n_stocks, 'score').copy()
        portfolio['weight'] = assign_weights(len(portfolio))
        
        display_cols = ['symbol', 'sector', 'group', 'score', 'roe', 'roce', 'mcap', 'weight']
        
        st.dataframe(
            portfolio[display_cols],
            use_container_width=True,
            column_config={
                "score": st.column_config.NumberColumn("Score", format="%d/15"),
                "roe": st.column_config.NumberColumn("ROE %", format="%.1f"),
                "roce": st.column_config.NumberColumn("ROCE %", format="%.1f"),
                "mcap": st.column_config.NumberColumn("MCap ₹Cr", format="%.0f"),
                "weight": st.column_config.NumberColumn("Weight %", format="%.1f%%")
            },
            hide_index=True
        )
        
        st.caption(f"Total Weight: {portfolio['weight'].sum():.1f}%")
        
        col1, col2 = st.columns(2)
        with col1:
            fig_pie = px.pie(portfolio, values='weight', names='symbol', title="Weights")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            sector_wt = portfolio.groupby('sector')['weight'].sum()
            fig_bar = px.bar(x=sector_wt.index, y=sector_wt.values, title="Sectors")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        avg_score = portfolio['score'].mean()
        cagr = (avg_score / 15 * 25).round(1)
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Expected CAGR", f"{cagr}%")
        with col2: st.metric("vs Nifty", f"+{cagr-15:.1f}%")
        with col3: st.metric("₹1Cr → 5Yrs", f"₹{(1*(1+cagr/100)**5):.1f}Cr")
        
        csv = portfolio.to_csv(index=False)
        st.download_button("Download CSV", csv, f"portfolio_{datetime.now().strftime('%Y%m%d')}.csv")
        
        st.markdown("## **Risk Rules**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("- Max loss: 1-2%")
            st.markdown("- Group-backed priority")
        with col2:
            st.markdown("- Take profit: 3-5%")
            st.markdown("- Never average down")
    
    else:
        st.info("Select sectors to analyze stocks")

if __name__ == "__main__":
    main()
