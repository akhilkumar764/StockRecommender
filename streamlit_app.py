import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timezone

st.set_page_config(page_title="Sector-Stock Analyzer PRO", layout="wide")

# GLOBAL TIMESTAMP TRACKING
if 'data_fetch_time' not in st.session_state:
    st.session_state.data_fetch_time = None

@st.cache_data(ttl=1800)  
def automated_sector_analysis():
    """Execute with exact timestamp capture"""
    # CAPTURE EXACT FETCH TIME (UTC)
    fetch_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Your existing analysis code...
    sectors_data = {
        'Private Banks': {'roe': 18.2, 'growth': 15.2, 'pe': 19.8},
        'IT Services': {'roe': 45.8, 'growth': 9.1, 'pe': 32.1}, 
        'Auto Ancillaries': {'roe': 15.2, 'growth': 18.4, 'pe': 42.0}
    }
    
    sector_df = pd.DataFrame(sectors_data).T
    sector_df['composite_score'] = (
        sector_df['roe'] * 0.4 + 
        sector_df['growth'] * 0.3 + 
        (100/sector_df['pe']) * 0.3
    )
    
    best_sectors = sector_df.nlargest(3, 'composite_score').index.tolist()
    
    # LIVE NSE DATA FETCH WITH TIMESTAMP
    stock_data = []
    for sector in best_sectors:
        for symbol in ['HDFCBANK', 'TCS', 'ICICIBANK', 'INFY', 'MOTHERSUMI']:
            try:
                ticker = yf.Ticker(f"{symbol}.NS")
                info = ticker.info
                stock_data.append({
                    'symbol': symbol,
                    'sector': sector,
                    'price': info.get('currentPrice', np.nan),
                    'pe': info.get('trailingPE', np.nan),
                    'roe': info.get('returnOnEquity', np.nan) * 100,
                    'fetch_time': fetch_time  # EXACT FETCH TIMESTAMP
                })
            except:
                continue
    
    return {
        'sectors': sector_df,
        'best_sectors': best_sectors,
        'stocks': pd.DataFrame(stock_data),
        'fetch_time': fetch_time
    }

def main():
    st.markdown("# **🏛️ Sector-to-Stock Analyzer PRO**")
    
    # 📅 EXACT DATA FETCH TIMESTAMP (HEADER)
    st.markdown("---")
    st.markdown("**🕒 Data Fetch Time:** *Dynamic - Updates on refresh*")
    
    # RUN ANALYSIS WITH TIMESTAMP CAPTURE
    with st.spinner("🔄 Fetching live NSE data..."):
        analysis = automated_sector_analysis()
        st.session_state.data_fetch_time = analysis['fetch_time']
    
    # 🕐 DISPLAY EXACT TIMESTAMP (PROMINENT)
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        st.metric("📅 **Data As Of**", 
                 f"**{st.session_state.data_fetch_time}**",
                 delta=None)
    
    # SECTOR ANALYSIS
    st.markdown("## **📊 SECTOR RANKING**")
    st.dataframe(analysis['sectors'], use_container_width=True)
    
    # STOCK RECOMMENDATIONS WITH FETCH TIME
    st.markdown("## **🎯 LIVE STOCK DATA**")
    if not analysis['stocks'].empty:
        # ADD FETCH TIME COLUMN TO TABLE
        display_df = analysis['stocks'].copy()
        display_df['fetch_time'] = pd.to_datetime(display_df['fetch_time'])
        
        st.dataframe(
            display_df[['symbol', 'sector', 'price', 'pe', 'roe', 'fetch_time']],
            use_container_width=True,
            column_config={
                "fetch_time": st.column_config.DatetimeColumn(
                    "Data Fetched",
                    format="ll HH:mm:ss Z",  # Exact format
                    display_format="MMM DD, YYYY HH:mm:ss UTC"
                )
            },
            hide_index=True
        )
    
    # REFRESH BUTTON (Forces new data fetch)
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 **REFRESH LIVE DATA**", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    # FOOTER WITH CACHE STATUS
    st.caption(f"ℹ️ **Last full analysis**: {st.session_state.data_fetch_time} | Cache: 30 min")

if __name__ == "__main__":
    main()
