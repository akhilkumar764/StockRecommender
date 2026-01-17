import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import numpy as np
import pandas_ta as ta
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Indian Stock Recommender Pro", page_icon="📈", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main-header {font-size: 2.8rem; font-weight: bold; color: #1f77b4; text-align: center;}
.buy-badge {background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white;}
.hold-badge {background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white;}
.sell-badge {background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white;}
.metric-card {padding: 1rem; border-radius: 10px; background: #f8fafc;}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # 5 min cache
def get_nifty_stocks():
    """Live NSE data for top NIFTY stocks"""
    symbols = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 
               'HINDUNILVR.NS', 'KOTAKBANK.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS',
               'LT.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'MARUTI.NS', 'SUNPHARMA.NS']
    
    data = []
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="6mo")
            
            if len(hist) > 100:
                # Calculate technical indicators
                df_ta = hist.ta.rsi(append=True, length=14).dropna()
                rsi = df_ta['RSI_14'].iloc[-1]
                macd = hist.ta.macd(append=True).dropna()
                price = hist['Close'].iloc[-1]
                
                # Smart scoring logic
                short_score = calculate_short_score(rsi, macd, hist)
                mid_score = calculate_mid_score(info, hist)
                long_score = calculate_long_score(info)
                
                data.append({
                    'symbol': symbol.replace('.NS', ''),
                    'name': info.get('longName', symbol),
                    'sector': info.get('sector', 'Unknown'),
                    'price': price,
                    'target': price * 1.15,  # 15% upside
                    'stop_loss': price * 0.90,  # 10% downside
                    'rsi': round(rsi, 1),
                    'pe_ratio': info.get('trailingPE', 25),
                    'roe': info.get('returnOnEquity', 0.15) * 100 if info.get('returnOnEquity') else 15,
                    'market_cap': info.get('marketCap', 100000) / 1e7,  # In crores
                    'scores': {'short': short_score, 'mid': mid_score, 'long': long_score},
                    'recommendation': get_recommendation(max(short_score, mid_score, long_score))
                })
        except:
            continue
    
    return pd.DataFrame(data)

def calculate_short_score(rsi, macd_df, hist):
    """Short-term technical score (0-100)"""
    score = 0
    
    # RSI Score (optimal 45-75)
    if 45 <= rsi <= 75: score += 35
    elif 35 <= rsi <= 85: score += 25
    else: score += 10
    
    # Price vs Moving Average
    ma20 = hist['Close'].rolling(20).mean().iloc[-1]
    if hist['Close'].iloc[-1] > ma20: score += 25
    
    # Volume trend
    vol_ma = hist['Volume'].rolling(10).mean().iloc[-1]
    if hist['Volume'].iloc[-1] > vol_ma * 1.2: score += 25
    
    # MACD momentum
    if len(macd_df) > 0 and macd_df['MACD_12_26_9'].iloc[-1] > macd_df['MACDs_12_26_9'].iloc[-1]:
        score += 15
    
    return min(100, score)

def calculate_mid_score(info, hist):
    """Mid-term fundamental score"""
    score = 50  # Base score
    
    pe = info.get('trailingPE', 25)
    if pe and pe < 30: score += 20
    
    roe = info.get('returnOnEquity', 0.15) * 100
    if roe > 15: score += 20
    
    # Price momentum (3 month)
    price_3m = hist['Close'].iloc[-60] if len(hist) > 60 else hist['Close'].iloc[0]
    momentum = (hist['Close'].iloc[-1] / price_3m - 1) * 100
    if momentum > 10: score += 10
    
    return min(100, score)

def calculate_long_score(info):
    """Long-term quality score"""
    score = 60
    
    # Quality factors
    debt_to_equity = info.get('debtToEquity', 50)
    if debt_to_equity < 50: score += 15
    
    roe = info.get('returnOnEquity', 0.15) * 100
    if roe > 20: score += 15
    
    dividend_yield = info.get('dividendYield', 0) * 100
    if dividend_yield > 1: score += 10
    
    return min(100, score)

def get_recommendation(score):
    if score >= 80: return "STRONG BUY"
    elif score >= 70: return "BUY"
    elif score >= 60: return "HOLD"
    else: return "SELL"

def main():
    st.markdown('<h1 class="main-header">📈 Indian Stock Recommender PRO</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Live NSE Data | Smart Scoring | Swing Trading Ready</p>', unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.header("🎯 Filters")
    timeframe = st.sidebar.radio("Timeframe", ['short', 'mid', 'long'], index=1)
    min_score = st.sidebar.slider("Min Score", 0, 100, 65)
    sector_filter = st.sidebar.multiselect("Sectors", 
        ['Financial Services', 'Technology', 'Energy', 'Consumer', 'Healthcare', 'Unknown'], 
        default=['Financial Services', 'Technology'])
    
    # Load live data
    with st.spinner("Fetching live NSE data..."):
        df = get_nifty_stocks()
    
    # Apply filters
    df['current_score'] = df['scores'].apply(lambda x: x[timeframe])
    df['upside'] = ((df['target'] - df['price']) / df['price']) * 100
    
    df_filtered = df[
        (df['current_score'] >= min_score) &
        (df['sector'].isin(sector_filter))
    ].sort_values('current_score', ascending=False)
    
    if df_filtered.empty:
        st.warning("⚠️ No stocks match your criteria. Try adjusting filters.")
        st.stop()
    
    # Metrics dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("📊 Stocks Analyzed", len(df_filtered))
    with col2: st.metric("🟢 Strong Buys", len(df_filtered[df_filtered['recommendation'] == 'STRONG BUY']))
    with col3: st.metric("⭐ Avg Score", f"{df_filtered['current_score'].mean():.1f}")
    with col4: st.metric("📈 Avg Upside", f"{df_filtered['upside'].mean():.1f}%")
    
    # Top recommendations
    st.markdown("## 🎯 Top Recommendations")
    
    for idx, row in df_filtered.head(8).iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2, 3, 2])
            
            with col1:
                st.markdown(f"### {row['symbol']}")
                badge_class = {
                    'STRONG BUY': 'buy-badge', 'BUY': 'buy-badge', 
                    'HOLD': 'hold-badge', 'SELL': 'sell-badge'
                }[row['recommendation']]
                st.markdown(f'<span class="recommendation-badge {badge_class}">{row["recommendation"]}</span>', unsafe_allow_html=True)
            
            with col2:
                st.metric("💰 Price", f"₹{row['price']:,.0f}")
                st.metric("⭐ Score", f"{row['current_score']:.0f}", f"RSI: {row['rsi']}")
                st.metric("🎯 Target", f"₹{row['target']:,.0f}", f"+{row['upside']:.1f}%")
            
            with col3:
                st.metric("📊 P/E", f"{row['pe_ratio']:.1f}")
                st.metric("🔥 ROE", f"{row['roe']:.1f}%")
                st.caption(f"{row['sector']}")
            
            # Progress bar
            st.progress(min(row['current_score']/100, 1.0))
            st.markdown("---")
    
    # Disclaimer
    st.markdown("---")
    st.warning("⚠️ **Disclaimer**: For educational purposes only. Not financial advice. Always do your own research.")

if __name__ == "__main__":
    main()
