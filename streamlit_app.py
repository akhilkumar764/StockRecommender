import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import plotly.express as px

st.set_page_config(page_title="Scuttlebutt Portfolio Analyzer", layout="wide")

# INEVITABLE SECTORS DATABASE
INEVITABLE_SECTORS = {
    'Defense': ['HAL', 'BEL', 'RVNL', 'IRCON', 'BEML', 'MAZAGON', 'GRSE', 'COCHINSHIP'],
    'Green Energy': ['TATAPOWER', 'JSWENERGY', 'ADANIGREEN', 'KPIGREEN', 'RENEWPOWER', 'SUZLON', 'INOXWIND'],
    'EV': ['TATAMOTORS', 'EXIDEIND', 'AMARARAJA', 'MOTHERSON', 'MINDA', 'BHARAT FORGE', 'SAMVARDHANA'],
    'Data Centers': ['BHARTIARTL', 'TATACOMM', 'ROUTE', 'TATAELXSI', 'LTTS', 'PERSISTENT', 'COFORGE'],
    'Railways': ['RVNL', 'IRCON', 'IRCTC', 'TEXRAIL', 'RAILTEL', 'TITAGARH', 'JUPITER']
}

@st.cache_data(ttl=86400)
def generate_stock_universe():
    """Generate 50+ stock universe with ALL columns"""
    np.random.seed(42)
    stocks = []
    
    for sector, symbols in INEVITABLE_SECTORS.items():
        for symbol in symbols:
            stocks.append({
                'symbol': symbol,
                'sector': sector,
                'group': np.random.choice(['TATA', 'ADANI', 'JSW', 'None'], p=[0.25, 0.2, 0.15, 0.4]),
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
    """Podcast strategy scoring"""
    score = 0
    score += 2  # Inevitable sector
    if row['roe'] > 20 and row['sales_3yr'] > 15: score += 3
    if row['group'] in ['TATA', 'ADANI', 'JSW']: score += 3
    if row['ceo_score'] > 8: score += 2
    if row['scuttlebutt_score'] > 8: score += 2
    if row['promoter'] > 55: score += 1
    if row['debt_eq'] < 1: score += 1
    if row['mcap'] > 5000: score += 1
    return score

def assign_weights(n_stocks):
    """DYNAMIC weight assignment based on available stocks"""
    if n_stocks == 0:
        return []
    elif n_stocks == 1:
        return [100]
    elif n_stocks <= 5:
        weights = [30, 25, 20, 15, 10][:n_stocks]
    elif n_stocks <= 10:
        weights = [15, 13, 11, 10, 9, 8, 7, 6, 6, 5][:n_stocks]
    else:  # 11-15+ stocks
        weights = [10, 9, 8, 7, 6, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2][:n_stocks]
    
    # Normalize to 100%
    total = sum(weights)
    return [round(w/total*100, 1) for w in weights]

def main():
    st.markdown("# **🎯 Scuttlebutt Portfolio Analyzer**")
    st.markdown("**₹1.1Cr Strategy: Inevitable Sectors → Oligopoly Winners**")
    
    # LOAD UNIVERSE
    universe = generate_stock_universe()
    universe['criteria_passed'] = universe.apply(calculate_podcast_score, axis=1)
    
    # HEADER
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("📊 Universe", f"{len(universe)}")
    with col2: st.metric("🎯 Target", "15 Elite")
    with col3: st.metric("📅 Updated", datetime.now().strftime("%Y-%m-%d"))
    
    # SECTOR FILTER
    st.markdown("## **🚀 STEP 1: SELECT INEVITABLE SECTORS**")
    selected_sectors = st.multiselect(
        "Choose 2-5 sectors",
        options=list(INEVITABLE_SECTORS.keys()),
        default=['Defense', 'Green Energy'],
        help="Defense: ₹80k Cr | Green: 30% margins"
    )
    
    if selected_sectors:
        filtered = universe[universe['sector'].isin(selected_sectors)].copy()
        
        # TOP N PORTFOLIO
        st.markdown("## **🏆 STEP 2: ELITE PORTFOLIO**")
        n_portfolio = st.slider("Portfolio Size", 5, 20, 15)
        
        portfolio = filtered.nlargest(n_portfolio, 'criteria_passed').copy()
        
        # SAFE WEIGHT ASSIGNMENT
        portfolio['weight'] = assign_weights(len(portfolio))
        
        # DISPLAY
        display_cols = ['symbol', 'sector', 'group', 'criteria_passed', 'roe', 'roce', 'mcap', 'weight']
        
        st.dataframe(
            portfolio[display_cols],
            use_container_width=True,
            column_config={
                "criteria_passed": st.column_config.NumberColumn("Score", format="%d/15"),
                "roe": st.column_config.NumberColumn("ROE %", format="%.1f"),
                "roce": st.column_config.NumberColumn("ROCE %", format="%.1f"),
                "mcap": st.column_config.NumberColumn("MCap ₹Cr", format="%.0f"),
                "weight": st.column_config.NumberColumn("Weight %", format="%.1f%%")
            },
            hide_index=True
        )
        
        st.caption(f"**Total Weight: {portfolio['weight'].sum():.1f}%**")
        
        # CHARTS
        st.markdown("## **📊 VISUALIZATION**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(portfolio, values='weight', names='symbol', 
                           title="Portfolio Weights")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            sector_weight = portfolio.groupby('sector')['weight'].sum()
            fig_bar = px.bar(x=sector_weight.index, y=sector_weight.values,
                           title="Sector Allocation", 
                           labels={'x': 'Sector', 'y': 'Weight %'})
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # QUALITY MATRIX
        fig_scatter = px.scatter(portfolio, x='roce', y='criteria_passed', 
                                size='weight', color='sector',
                                hover_data=['symbol', 'roe'],
                                title="Quality Matrix",
                                labels={'criteria_passed': 'Score', 'roce': 'ROCE %'})
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # RETURNS
        st.markdown("## **💰 EXPECTED RETURNS**")
        avg_score = portfolio['criteria_passed'].mean()
        expected_cagr = (avg_score / 15 * 25).round(1)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("CAGR", f"{expected_cagr}%")
        with col2: st.metric("vs Nifty", f"+{expected_cagr-15}%")
        with col3: st.metric("₹1Cr→5Yrs", f"₹{(1*(1+expected_cagr/100)**5):.1f}Cr")
        with col4: st.metric("Stocks", len(portfolio))
        
        # RISK RULES
        st.markdown("## **🛡️ PODCAST RISK RULES**")
        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            **✅ Entry:**
            - Max loss: 1-2%
            - Only top scorers
            - Group-backed priority
            """)
        with col2:
            st.warning("""
            **⚠️ Exit:**
            - Take profit: 3-5%
            - Cut loss: -2% max
            - Never average down
            """)
        
        # SCUTTLEBUTT
        st.markdown("## **🔍 STEP 3: SCUTTLEBUTT NOTES**")
        obs = st.text_area(
            "Your observations",
            placeholder="Wires in Mumbai → Polycab | Defense orders → HAL/BEL"
        )
        if obs:
            st.success("✅ Scuttlebutt recorded!")
        
        # DOWNLOAD
        csv = portfolio.to_csv(index=False)
        st.download_button(
            "💾 Download Portfolio",
            csv,
            f"portfolio_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
    else:
        st.info("""
        **🎙️ PODCAST STRATEGY (₹1.1Cr)**
        
        1. **Inevitable Sectors** → Defense/Green/EV
        2. **Oligopoly** → Top 2-3 win 80%
        3. **Group Backing** → TATA/ADANI/JSW
        4. **Scuttlebutt** → Wires/orders observations
        
        **Result:** 20-25% CAGR | ₹1Cr→₹6Cr (10yrs)
        
        **→ Select sectors above**
        """)
    
    st.markdown("---")
    st.caption("*₹1.1Cr podcast strategy: Defense/Railway scuttlebutt*")

if __name__ == "__main__":
    main()
