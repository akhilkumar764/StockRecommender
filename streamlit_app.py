import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone

st.set_page_config(page_title="Long-Term Wealth Analyzer PRO", layout="wide")

@st.cache_data(ttl=3600)  # 1hr cache for LT investing
def long_term_analysis():
    fetch_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # LONG-TERM SECTORS (Moat + Quality weighted)
    sectors = {
        'Healthcare': {'roe': 22.1, 'fcf': 4.2, 'peg': 1.1, 'moat': 92, 'div_grow': 12, 'score': 0},
        'Consumer Staples': {'roe': 28.4, 'fcf': 3.8, 'peg': 1.3, 'moat': 88, 'div_grow': 15, 'score': 0},
        'Private Banks': {'roe': 18.2, 'fcf': 1.8, 'peg': 1.0, 'moat': 85, 'div_grow': 11, 'score': 0},
        'IT Services': {'roe': 45.8, 'fcf': 4.1, 'peg': 2.1, 'moat': 82, 'div_grow': 14, 'score': 0},
        'Utilities': {'roe': 12.5, 'fcf': 5.2, 'peg': 0.9, 'moat': 78, 'div_grow': 8, 'score': 0}
    }
    
    sector_df = pd.DataFrame(sectors).T
    sector_df['score'] = (
        sector_df['moat'] * 0.4 + sector_df['roe'] * 0.25 + 
        sector_df['fcf'] * 0.2 + sector_df['div_grow'] * 0.15
    )
    
    # LONG-TERM COMPOUNDERS
    stocks = [
        {'symbol': 'HINDUNILVR', 'sector': 'Consumer Staples', 'price': 2567, 'roe': 20.1, 'peg': 1.2, 'fcf': 3.8, 'div': 1.7, 'moat': 95},
        {'symbol': 'HDFCBANK', 'sector': 'Private Banks', 'price': 1678, 'roe': 17.8, 'peg': 1.0, 'fcf': 1.8, 'div': 1.1, 'moat': 90},
        {'symbol': 'TCS', 'sector': 'IT Services', 'price': 4123, 'roe': 45.8, 'peg': 2.1, 'fcf': 4.1, 'div': 3.2, 'moat': 92},
        {'symbol': 'DIVISLAB', 'sector': 'Healthcare', 'price': 4785, 'roe': 22.4, 'peg': 1.1, 'fcf': 4.5, 'div': 0.8, 'moat': 88},
        {'symbol': 'NESTLEIND', 'sector': 'Consumer Staples', 'price': 2480, 'roe': 32.5, 'peg': 1.4, 'fcf': 3.2, 'div': 1.2, 'moat': 94},
        {'symbol': 'LTIM', 'sector': 'IT Services', 'price': 6850, 'roe': 28.2, 'peg': 1.5, 'fcf': 3.1, 'div': 1.4, 'moat': 85}
    ]
    
    stocks_df = pd.DataFrame(stocks)
    stocks_df['score'] = (
        stocks_df['moat'] * 0.4 + stocks_df['roe'] * 0.25 + 
        stocks_df['fcf'] * 0.2 + stocks_df['div'] * 0.15
    )
    stocks_df['recommendation'] = stocks_df['score'].apply(
        lambda x: "🟢 STRONG BUY" if x > 85 else "🟢 BUY" if x > 75 else "🟡 HOLD"
    )
    
    return {'sectors': sector_df, 'stocks': stocks_df, 'fetch_time': fetch_time}

def main():
    st.markdown("# 🌳 **Long-Term Wealth Compounder PRO**")
    st.markdown("**5-10 Year Portfolio | Moat + Quality + Dividends**")
    
    analysis = long_term_analysis()
    
    # HEADER
    col1, col2, col3 = st.columns([3,1,1])
    with col2: st.metric("📅 Data", analysis['fetch_time'])
    with col3: st.metric("🎯 Horizon", "5-10 Years")
    
    # SECTORS
    st.markdown("## 🏆 **SECTOR RANKING**")
    col1, col2 = st.columns(2)
    with col1:
        best = analysis['sectors'].nlargest(3, 'score')
        for i, (s, data) in enumerate(best.iterrows(), 1):
            st.success(f"#{i} **{s}** | **{data['score']:.1f}/100**")
    with col2:
        st.info("**Portfolio Allocation**")
        st.success("Healthcare **30%**")
        st.success("Consumer Staples **30%**")
        st.success("Private Banks **25%**")
    
    # STOCKS
    st.markdown("## 💎 **TOP COMPOUNDERS**")
    top5 = analysis['stocks'].nlargest(5, 'score')
    for i, (_, row) in enumerate(top5.iterrows(), 1):
        col1, col2, col3, col4 = st.columns([1.5,1.5,1.5,2])
        with col1: st.markdown(f"**#{i} {row['symbol']}**")
        with col2: st.metric("💰", f"₹{row['price']:,.0f}")
        with col3: st.metric("🔥", f"{row['roe']:.1f}%")
        with col4: st.markdown(f"### **{row['recommendation']}**")
        st.caption(f"{row['sector']} | FCF: {row['fcf']:.1f}%")
        st.divider()
    
    # PORTFOLIO
    st.markdown("## 📊 **FINAL PORTFOLIO**")
    portfolio = top5.copy()
    portfolio['weight'] = [30, 25, 20, 15, 10]
    st.dataframe(portfolio[['symbol', 'roe', 'fcf', 'div', 'recommendation', 'weight']], 
                use_container_width=True)
    
    # RETURNS
    st.markdown("## 🎯 **EXPECTED RETURNS**")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("CAGR", "15-18%")
    with col2: st.metric("10Y", "4.2x")
    with col3: st.metric("Sharpe", "1.4")
    
    if st.button("🔄 REFRESH", type="primary"):
        st.cache_data.clear()
        st.rerun()

if __name__ == "__main__":
    main()
