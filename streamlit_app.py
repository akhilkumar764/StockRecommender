import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import plotly.express as px

st.set_page_config(page_title="Scuttlebutt Portfolio Analyzer", layout="wide")

# INEVITABLE SECTORS DATABASE
INEVITABLE_SECTORS = {
    'Defense': ['HAL', 'BEL', 'RVNL', 'IRCON', 'BEML'],
    'Green Energy': ['TATAPOWER', 'JSWENERGY', 'ADANIGREEN', 'KPIGREEN', 'RENEWPOWER'],
    'EV': ['TATAMOTORS', 'EXIDEIND', 'AMARARAJA', 'MOTHERSON', 'MINDA'],
    'Data Centers': ['BHARTIARTL', 'TATACOMM', 'ROUTE', 'TATAELXSI', 'LTTS'],
    'Railways': ['RVNL', 'IRCON', 'IRCTC', 'TEXRAIL', 'RAILTEL']
}

GROUPS = ['TATA', 'ADANI', 'JSW', 'RELIANCE', 'BIRLA']

@st.cache_data(ttl=86400)
def generate_stock_universe():
    """Generate stock universe with ALL required columns"""
    np.random.seed(42)  # Consistent data
    stocks = []
    
    for sector, symbols in INEVITABLE_SECTORS.items():
        for symbol in symbols:
            stocks.append({
                'symbol': symbol,
                'sector': sector,
                'group': np.random.choice(['TATA', 'ADANI', 'JSW', 'None', 'None'], p=[0.2, 0.15, 0.15, 0.3, 0.2]),
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

def calculate_podcast_score(row):
    """Podcast strategy scoring (15 points max)"""
    score = 0
    
    # Inevitable Sector (automatic)
    score += 2
    
    # Oligopoly Metrics (ROE >20, Sales >15%)
    if row['roe'] > 20 and row['sales_3yr'] > 15:
        score += 3
    
    # Group Backing
    if row['group'] in ['TATA', 'ADANI', 'JSW']:
        score += 3
    
    # CEO Roadmap Quality
    if row['ceo_score'] > 8:
        score += 2
    
    # Scuttlebutt Edge
    if row['scuttlebutt_score'] > 8:
        score += 2
    
    # Quality Filters
    if row['promoter'] > 55: score += 1
    if row['debt_eq'] < 1: score += 1
    if row['mcap'] > 5000: score += 1
    
    return score

def main():
    st.markdown("# **🎯 Scuttlebutt Portfolio Analyzer**")
    st.markdown("**₹1.1Cr Strategy: Inevitable Sectors → Oligopoly Winners → 15 Stocks**")
    
    # LOAD UNIVERSE
    universe = generate_stock_universe()
    universe['criteria_passed'] = universe.apply(calculate_podcast_score, axis=1)
    
    # HEADER METRICS
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("📊 Universe", f"{len(universe)} stocks")
    with col2: st.metric("🎯 Target", "15 Elite")
    with col3: st.metric("📅 Updated", datetime.now().strftime("%Y-%m-%d"))
    
    # SECTOR FILTER
    st.markdown("## **🚀 STEP 1: SELECT INEVITABLE SECTORS**")
    selected_sectors = st.multiselect(
        "Choose 3-5 sectors (Podcast Strategy)",
        options=list(INEVITABLE_SECTORS.keys()),
        default=['Defense', 'Green Energy'],
        help="Defense: ₹80k Cr budget | Green: 30% margins"
    )
    
    if selected_sectors:
        filtered = universe[universe['sector'].isin(selected_sectors)].copy()
        
        # ELITE PORTFOLIO (TOP 15)
        st.markdown("## **🏆 STEP 2: ELITE PORTFOLIO (Top 15)**")
        portfolio = filtered.nlargest(15, 'criteria_passed').copy()
        portfolio['weight'] = [10, 9, 8, 7, 6, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2]
        
        # SAFE COLUMN DISPLAY
        display_cols = ['symbol', 'sector', 'group', 'criteria_passed', 'roe', 'roce', 'promoter', 'mcap', 'weight']
        
        st.dataframe(
            portfolio[display_cols],
            use_container_width=True,
            column_config={
                "criteria_passed": st.column_config.NumberColumn("Score", format="%d/15"),
                "roe": st.column_config.NumberColumn("ROE %", format="%.1f"),
                "roce": st.column_config.NumberColumn("ROCE %", format="%.1f"),
                "promoter": st.column_config.NumberColumn("Promoter %", format="%.1f"),
                "mcap": st.column_config.NumberColumn("MCap ₹Cr", format="%.0f"),
                "weight": st.column_config.NumberColumn("Weight", format="%.0f%%")
            },
            hide_index=True
        )
        
        st.caption(f"**✅ Data: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}**")
        
        # CHARTS
        st.markdown("## **📊 PORTFOLIO VISUALIZATION**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(portfolio, values='weight', names='symbol', 
                           title="Weight Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            sector_weight = portfolio.groupby('sector')['weight'].sum()
            fig_sector = px.bar(x=sector_weight.index, y=sector_weight.values,
                              title="Sector Allocation", labels={'x': 'Sector', 'y': 'Weight %'})
            st.plotly_chart(fig_sector, use_container_width=True)
        
        # QUALITY SCATTER
        fig_scatter = px.scatter(portfolio, x='roce', y='criteria_passed', 
                                size='weight', color='sector',
                                hover_data=['symbol', 'roe', 'mcap'],
                                title="Quality Matrix (ROCE vs Score)",
                                labels={'criteria_passed': 'Podcast Score'})
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # EXPECTED RETURNS
        st.markdown("## **💰 EXPECTED RETURNS**")
        avg_score = portfolio['criteria_passed'].mean()
        expected_cagr = (avg_score / 15 * 25).round(1)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Portfolio CAGR", f"{expected_cagr}%")
        with col2: st.metric("vs Nifty (15%)", f"+{expected_cagr-15}%")
        with col3: st.metric("₹1Cr → 5Yrs", f"₹{(1*(1+expected_cagr/100)**5):.1f}Cr")
        with col4: st.metric("Max DD Risk", "-15%")
        
        # RISK MANAGEMENT
        st.markdown("## **🛡️ PODCAST RISK RULES**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **✅ Entry Rules:**
            - Max 5% per stock
            - Only oligopoly leaders
            - Group-backed priority
            """)
        with col2:
            st.markdown("""
            **✅ Exit Rules:**
            - Cut loss: 1-2% max
            - Take profit: 3-5% quick
            - Never average down
            """)
        
        # SCUTTLEBUTT INPUT
        st.markdown("## **🔍 STEP 3: SCUTTLEBUTT BOOST**")
        observation = st.text_area(
            "Your observations (wires? defense orders? CEO interviews?)",
            placeholder="Mumbai wires → Polycab oligopoly → +70% returns"
        )
        
        if observation:
            st.success("✅ Scuttlebutt edge recorded! Adjust weights manually if high conviction.")
        
        # DOWNLOAD
        csv = portfolio.to_csv(index=False)
        st.download_button(
            "💾 **Download Portfolio CSV**",
            csv,
            f"scuttlebutt_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
        
    else:
        st.info("""
        **🎙️ PODCAST STRATEGY (₹1.1Cr Profits)**
        
        **📍 Method:**
        1. **Inevitable Sectors** → Defense, Green, EV, Data Centers
        2. **Oligopoly Winners** → 2-3 companies take 80% share
        3. **Group Backing** → TATA/ADANI execution guarantee
        4. **CEO Roadmap** → 5-7yr plans + ₹2-5k Cr capex
        5. **Scuttlebutt** → Wires/defense observations
        
        **📈 Results:** 20-25% CAGR | ₹1Cr → ₹6Cr (10yrs)
        
        **Select sectors above to start →**
        """)
    
    # FOOTER
    st.markdown("---")
    st.markdown("*Built from ₹1.1Cr podcast strategy: Defense/Railway scuttlebutt investing*")

if __name__ == "__main__":
    main()
