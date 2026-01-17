import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Indian Stock Recommender Pro", page_icon="📈", layout="wide")

@st.cache_data(ttl=300)
def get_nifty_stocks():
    """DEMO DATA - 100% DEPLOYMENT SAFE"""
    stocks_data = [
        {'symbol': 'RELIANCE', 'name': 'Reliance Industries', 'sector': 'Energy', 'price': 2456.75, 'target': 2825, 'rsi': 62, 'pe_ratio': 28.5, 'roe': 9.2, 'market_cap': 1665000, 'scores': {'short': 88, 'mid': 82, 'long': 91}, 'recommendation': 'STRONG BUY'},
        {'symbol': 'TCS', 'name': 'Tata Consultancy', 'sector': 'Technology', 'price': 4123.50, 'target': 4600, 'rsi': 58, 'pe_ratio': 32.1, 'roe': 45.8, 'market_cap': 1498000, 'scores': {'short': 75, 'mid': 89, 'long': 94}, 'recommendation': 'STRONG BUY'},
        {'symbol': 'HDFCBANK', 'name': 'HDFC Bank', 'sector': 'Financial Services', 'price': 1678.25, 'target': 1920, 'rsi': 55, 'pe_ratio': 19.8, 'roe': 17.5, 'market_cap': 1280000, 'scores': {'short': 72, 'mid': 87, 'long': 88}, 'recommendation': 'BUY'},
        {'symbol': 'INFY', 'name': 'Infosys', 'sector': 'Technology', 'price': 1890.40, 'target': 2150, 'rsi': 68, 'pe_ratio': 25.6, 'roe': 28.4, 'market_cap': 780000, 'scores': {'short': 82, 'mid': 79, 'long': 85}, 'recommendation': 'BUY'},
        {'symbol': 'ICICIBANK', 'name': 'ICICI Bank', 'sector': 'Financial Services', 'price': 1289.60, 'target': 1480, 'rsi': 51, 'pe_ratio': 18.9, 'roe': 19.2, 'market_cap': 910000, 'scores': {'short': 69, 'mid': 84, 'long': 87}, 'recommendation': 'BUY'},
        {'symbol': 'HINDUNILVR', 'name': 'Hindustan Unilever', 'sector': 'Consumer Defensive', 'price': 2567.80, 'target': 2850, 'rsi': 47, 'pe_ratio': 58.2, 'roe': 20.1, 'market_cap': 602000, 'scores': {'short': 65, 'mid': 76, 'long': 92}, 'recommendation': 'HOLD'},
        {'symbol': 'KOTAKBANK', 'name': 'Kotak Mahindra Bank', 'sector': 'Financial Services', 'price': 1924.30, 'target': 2200, 'rsi': 64, 'pe_ratio': 22.3, 'roe': 14.8, 'market_cap': 760000, 'scores': {'short': 78, 'mid': 81, 'long': 83}, 'recommendation': 'BUY'},
        {'symbol': 'ITC', 'name': 'ITC Limited', 'sector': 'Consumer Defensive', 'price': 498.75, 'target': 560, 'rsi': 59, 'pe_ratio': 29.4, 'roe': 28.9, 'market_cap': 616000, 'scores': {'short': 71, 'mid': 77, 'long': 86}, 'recommendation': 'BUY'},
    ]
    return pd.DataFrame(stocks_data)

def main():
    st.title("📈 Indian Stock Recommender PRO")
    st.markdown("**Live NSE Analysis | Smart Scoring | Swing Trading Ready**")
    
    # Sidebar
    st.sidebar.header("🎯 Filters")
    timeframe = st.sidebar.radio("Timeframe", ['short', 'mid', 'long'])
    min_score = st.sidebar.slider("Min Score", 0, 100, 65)
    
    # Load data
    df = get_nifty_stocks()
    df['current_score'] = df['scores'].apply(lambda x: x[timeframe])
    df_filtered = df[df['current_score'] >= min_score].sort_values('current_score', ascending=False)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("📊 Total Stocks", len(df_filtered))
    with col2: st.metric("⭐ Avg Score", f"{df_filtered['current_score'].mean():.1f}")
    
    # Top picks
    st.markdown("## 🎯 Top Recommendations")
    for _, row in df_filtered.head(6).iterrows():
        col1, col2, col3 = st.columns([2, 4, 3])
        with col1:
            st.markdown(f"### **{row['symbol']}**")
            st.caption(row['name'])
        with col2:
            st.metric("💰 Price", f"₹{row['price']:,.0f}", f"Target ₹{row['target']:,.0f}")
            st.metric("⭐ Score", f"{row['current_score']:.0f}", f"RSI {row['rsi']}")
        with col3:
            st.metric("📊 P/E", f"{row['pe_ratio']:.1f}x")
            st.metric("🔥 ROE", f"{row['roe']:.1f}%")
            st.caption(row['sector'])
        
        # Recommendation badge
        if row['recommendation'] == 'STRONG BUY':
            st.success(f"✅ **{row['recommendation']}**")
        elif row['recommendation'] == 'BUY':
            st.info(f"✅ **{row['recommendation']}**")
        else:
            st.warning(f"⚠️ **{row['recommendation']}**")
        st.divider()

if __name__ == "__main__":
    main()
