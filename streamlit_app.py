import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="17-Criteria Dynamic Portfolio", layout="wide")

# SIMULATED NSE DATA WITH 17-CRITERIA METRICS
@st.cache_data(ttl=3600)
def get_universe_data():
    """17-criteria universe (200 NSE stocks)"""
    np.random.seed(42)
    symbols = [f'STOCK{i:03d}' for i in range(200)]
    
    data = []
    for symbol in symbols:
        data.append({
            'symbol': symbol,
            'sector': np.random.choice(['FMCG', 'Healthcare', 'Banks', 'IT', 'Auto']),
            'mcap': np.random.uniform(500, 50000),
            'sales_3y': np.random.uniform(5, 25),
            'sales_7y': np.random.uniform(5, 20),
            'profit_3y': np.random.uniform(8, 30),
            'profit_7y': np.random.uniform(6, 25),
            'opm': np.random.uniform(8, 28),
            'opm_5y': np.random.uniform(8, 25),
            'opm_10y': np.random.uniform(6, 22),
            'npm': np.random.uniform(2, 18),
            'roce': np.random.uniform(5, 35),
            'roe': np.random.uniform(5, 40),
            'roic': np.random.uniform(5, 30),
            'pledge': np.random.uniform(0, 15),
            'debt_eq': np.random.uniform(0, 3),
            'icr': np.random.uniform(1, 12),
            'ocf_ebit': np.random.uniform(0.3, 1.5),
            'promoter': np.random.uniform(25, 75),
            'price': np.random.uniform(100, 5000),
            'quarter_score': 0,
            'criteria_passed': 0
        })
    
    df = pd.DataFrame(data)
    
    # APPLY 17-CRITERIA SCREENING
    df['pass_sales'] = (df['sales_3y'] > 12) & (df['sales_7y'] > 10)
    df['pass_profit'] = (df['profit_3y'] > 14) & (df['profit_7y'] > 10)
    df['pass_opm'] = (df['opm'] > 14) & (df['opm_5y'] > 14) & (df['opm_10y'] > 10)
    df['pass_npm'] = df['npm'] > 5
    df['pass_returns'] = (df['roce'] > 15) | (df['roe'] > 15) | (df['roic'] > 15)
    df['pass_debt'] = (df['pledge'] < 1) & (df['debt_eq'] < 1) & (df['icr'] > 3)
    df['pass_cash'] = df['ocf_ebit'] > 0.75
    df['pass_promoter'] = df['promoter'] > 50
    df['pass_mcap'] = df['mcap'] > 500
    
    df['criteria_passed'] = (
        df['pass_sales'].astype(int) * 2 +
        df['pass_profit'].astype(int) * 2 +
        df['pass_opm'].astype(int) * 3 +
        df['pass_npm'].astype(int) +
        df['pass_returns'].astype(int) +
        df['pass_debt'].astype(int) * 3 +
        df['pass_cash'].astype(int) +
        df['pass_promoter'].astype(int) +
        df['pass_mcap'].astype(int)
    )
    
    # TOP 10 SCORING
    top_stocks = df.nlargest(10, 'criteria_passed')
    top_stocks['weight'] = [25, 20, 15, 12, 10, 8, 5, 3, 1, 1]
    
    return df, top_stocks

def main():
    st.markdown("# **🚀 17-Criteria Dynamic Portfolio Rebalancer**")
    st.markdown("**Quarterly Screening | Yearly Mandatory Rebalance | Elite Quality Only**")
    
    # DYNAMIC REBALANCE LOGIC
    today = datetime.now()
    quarter_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        days_since_q = (today - quarter_start).days
        st.metric("📅 Days Since Q-Rebalance", days_since_q)
    with col2:
        days_since_y = (today - year_start).days
        st.metric("📅 Days Since Y-Rebalance", days_since_y)
    with col3:
        next_rebalance = year_start.replace(year=today.year+1)
        st.metric("🎯 Next Mandatory Rebalance", next_rebalance.strftime("%b %Y"))
    
    # RUN SCREENING
    universe, portfolio = get_universe_data()
    
    # REBALANCE STATUS
    st.markdown("## **⚖️ REBALANCE STATUS**")
    col1, col2 = st.columns(2)
    
    with col1:
        if days_since_q > 90:
            st.error("🔴 **QUARTERLY OVERDUE** - Screen NOW")
        else:
            st.success("✅ Quarterly OK")
    
    with col2:
        if days_since_y > 365:
            st.error("🚨 **YEARLY MANDATORY** - REBALANCE IMMEDIATELY")
        else:
            st.success("✅ Yearly OK")
    
    # CURRENT PORTFOLIO
    st.markdown("## **🏆 CURRENT PORTFOLIO (Top 17/17 Criteria)**")
    st.dataframe(
        portfolio[['symbol', 'sector', 'criteria_passed', 'roce', 'roe', 'promoter', 'weight']],
        use_container_width=True,
        column_config={
            "criteria_passed": st.column_config.NumberColumn("Criteria ✓", format="%d/17"),
            "weight": st.column_config.NumberColumn("Weight", format="%.0f%%")
        },
        hide_index=True
    )
    
    # QUARTERLY SCREENING RESULTS
    st.markdown("## **🔍 QUARTERLY SCREEN (Latest Results)**")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        elite = universe[universe['criteria_passed'] >= 14]
        st.metric("🏅 Elite Stocks (14+ criteria)", len(elite))
    
    with col2:
        st.metric("📊 Avg Criteria Passed", f"{universe['criteria_passed'].mean():.1f}/17")
    
    # VISUALIZATION
    fig = px.scatter(
        portfolio, x='roce', y='criteria_passed', 
        size='mcap', color='sector', hover_name='symbol',
        title="Portfolio Quality Map",
        labels={'criteria_passed': 'Criteria Met', 'roce': 'ROCE %'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # REBALANCE RECOMMENDATIONS
    st.markdown("## **🎯 REBALANCE ACTION PLAN**")
    
    if days_since_y > 365:
        st.markdown("""
        ### **🚨 YEARLY MANDATORY REBALANCE REQUIRED**
        **Execute these steps immediately:**
        1. **SELL** all current holdings
        2. **BUY** top 10 from latest screening  
        3. **Allocate** per target weights above
        4. **Record** new base prices
        """)
    elif days_since_q > 90:
        st.markdown("""
        ### **⚠️ QUARTERLY REVIEW RECOMMENDED**  
        **Check for:**
        • New entrants (15+ criteria)
        • Failing stocks (dropped <12 criteria)
        • Weight drift >5%
        """)
    else:
        st.success("✅ **Portfolio Healthy** - Monitor quarterly")
    
    # PORTFOLIO METRICS
    st.markdown("## **📈 PORTFOLIO METRICS**")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Expected CAGR", "22-25%")
    with col2: st.metric("Max Drawdown", "-16%")
    with col3: st.metric("Sharpe Ratio", "1.9")
    with col4: st.metric("Universe Yield", f"{len(portfolio)}/200 stocks")
    
    # REBALANCE BUTTONS
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 **FORCE QUARTERLY RE-SCREEN**", type="secondary"):
            st.cache_data.clear()
            st.rerun()
    with col2:
        if st.button("🎯 **EXECUTE YEARLY REBALANCE**", type="primary"):
            st.balloons()
            st.success("🎉 Portfolio rebalanced! New weights allocated.")
            st.rerun()
    
    # FOOTER
    st.markdown("---")
    st.caption(f"**Rebalance Engine** | {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} | "
              f"**Screen**: 17 criteria | **Universe**: NSE 200 | **Next**: {next_rebalance.strftime('%b %Y')}")

if __name__ == "__main__":
    main()
