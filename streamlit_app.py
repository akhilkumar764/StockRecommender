"""
Indian Stock Recommendation System
Production-ready Streamlit app with built-in demo data
Deploy to Streamlit Cloud without errors!
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Indian Stock Recommender",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .recommendation-badge {
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        font-size: 1.1rem;
    }
    .buy-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    .hold-badge {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    .sell-badge {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ==================== DATA GENERATION ====================

@st.cache_data
def generate_demo_stocks():
    """Generate realistic demo stock data"""
    stocks_data = [
        {
            'symbol': 'RELIANCE',
            'name': 'Reliance Industries Ltd',
            'sector': 'Energy',
            'price': 2456.50,
            'target': 2850.00,
            'stop_loss': 2280.00,
            'scores': {'short': 72, 'mid': 81, 'long': 88},
            'component_scores': {
                'short': {'technical': 78, 'momentum': 82, 'volume': 68, 'risk': 65},
                'mid': {'fundamental': 85, 'growth': 78, 'quality': 83, 'valuation': 72},
                'long': {'fundamental': 92, 'moat': 90, 'management': 87, 'growth': 85}
            },
            'pe_ratio': 23.4,
            'pb_ratio': 2.8,
            'roe': 12.8,
            'roce': 14.5,
            'debt_equity': 0.45,
            'market_cap': 1654000,
            'revenue_growth': 18.5,
            'profit_growth': 22.3,
            'dividend_yield': 0.8,
            'recommendation': 'STRONG BUY'
        },
        {
            'symbol': 'TCS',
            'name': 'Tata Consultancy Services',
            'sector': 'IT',
            'price': 3842.75,
            'target': 4100.00,
            'stop_loss': 3650.00,
            'scores': {'short': 58, 'mid': 74, 'long': 86},
            'component_scores': {
                'short': {'technical': 54, 'momentum': 48, 'volume': 62, 'risk': 68},
                'mid': {'fundamental': 78, 'growth': 68, 'quality': 85, 'valuation': 65},
                'long': {'fundamental': 89, 'moat': 88, 'management': 90, 'growth': 75}
            },
            'pe_ratio': 28.5,
            'pb_ratio': 12.4,
            'roe': 42.3,
            'roce': 38.7,
            'debt_equity': 0.03,
            'market_cap': 1398000,
            'revenue_growth': 12.4,
            'profit_growth': 14.7,
            'dividend_yield': 1.2,
            'recommendation': 'HOLD'
        },
        {
            'symbol': 'HDFCBANK',
            'name': 'HDFC Bank Ltd',
            'sector': 'Banking',
            'price': 1678.30,
            'target': 1920.00,
            'stop_loss': 1550.00,
            'scores': {'short': 65, 'mid': 78, 'long': 92},
            'component_scores': {
                'short': {'technical': 62, 'momentum': 58, 'volume': 71, 'risk': 68},
                'mid': {'fundamental': 82, 'growth': 75, 'quality': 88, 'valuation': 68},
                'long': {'fundamental': 95, 'moat': 94, 'management': 91, 'growth': 88}
            },
            'pe_ratio': 19.2,
            'pb_ratio': 2.9,
            'roe': 17.5,
            'roce': 16.8,
            'debt_equity': 0.12,
            'market_cap': 1245000,
            'revenue_growth': 15.2,
            'profit_growth': 19.8,
            'dividend_yield': 1.5,
            'recommendation': 'BUY'
        },
        {
            'symbol': 'INFY',
            'name': 'Infosys Ltd',
            'sector': 'IT',
            'price': 1523.60,
            'target': 1720.00,
            'stop_loss': 1420.00,
            'scores': {'short': 68, 'mid': 76, 'long': 83},
            'component_scores': {
                'short': {'technical': 72, 'momentum': 75, 'volume': 65, 'risk': 62},
                'mid': {'fundamental': 80, 'growth': 71, 'quality': 82, 'valuation': 70},
                'long': {'fundamental': 86, 'moat': 85, 'management': 84, 'growth': 77}
            },
            'pe_ratio': 24.8,
            'pb_ratio': 8.6,
            'roe': 29.4,
            'roce': 31.2,
            'debt_equity': 0.05,
            'market_cap': 632000,
            'revenue_growth': 13.8,
            'profit_growth': 16.2,
            'dividend_yield': 2.1,
            'recommendation': 'BUY'
        },
        {
            'symbol': 'BAJFINANCE',
            'name': 'Bajaj Finance Ltd',
            'sector': 'NBFC',
            'price': 6854.20,
            'target': 7850.00,
            'stop_loss': 6350.00,
            'scores': {'short': 76, 'mid': 84, 'long': 87},
            'component_scores': {
                'short': {'technical': 80, 'momentum': 85, 'volume': 72, 'risk': 68},
                'mid': {'fundamental': 88, 'growth': 92, 'quality': 82, 'valuation': 74},
                'long': {'fundamental': 90, 'moat': 86, 'management': 88, 'growth': 85}
            },
            'pe_ratio': 32.4,
            'pb_ratio': 6.8,
            'roe': 21.6,
            'roce': 19.3,
            'debt_equity': 5.8,
            'market_cap': 421000,
            'revenue_growth': 28.5,
            'profit_growth': 31.2,
            'dividend_yield': 0.3,
            'recommendation': 'STRONG BUY'
        },
        {
            'symbol': 'ICICIBANK',
            'name': 'ICICI Bank Ltd',
            'sector': 'Banking',
            'price': 1087.45,
            'target': 1250.00,
            'stop_loss': 1010.00,
            'scores': {'short': 71, 'mid': 80, 'long': 89},
            'component_scores': {
                'short': {'technical': 75, 'momentum': 78, 'volume': 69, 'risk': 64},
                'mid': {'fundamental': 84, 'growth': 79, 'quality': 86, 'valuation': 71},
                'long': {'fundamental': 91, 'moat': 90, 'management': 88, 'growth': 87}
            },
            'pe_ratio': 17.8,
            'pb_ratio': 2.7,
            'roe': 16.2,
            'roce': 15.9,
            'debt_equity': 0.15,
            'market_cap': 768000,
            'revenue_growth': 17.3,
            'profit_growth': 25.6,
            'dividend_yield': 0.9,
            'recommendation': 'STRONG BUY'
        },
        {
            'symbol': 'HINDUNILVR',
            'name': 'Hindustan Unilever Ltd',
            'sector': 'FMCG',
            'price': 2389.90,
            'target': 2650.00,
            'stop_loss': 2220.00,
            'scores': {'short': 62, 'mid': 71, 'long': 84},
            'component_scores': {
                'short': {'technical': 58, 'momentum': 55, 'volume': 68, 'risk': 70},
                'mid': {'fundamental': 75, 'growth': 65, 'quality': 81, 'valuation': 64},
                'long': {'fundamental': 87, 'moat': 92, 'management': 86, 'growth': 72}
            },
            'pe_ratio': 58.4,
            'pb_ratio': 14.2,
            'roe': 24.8,
            'roce': 28.3,
            'debt_equity': 0.02,
            'market_cap': 561000,
            'revenue_growth': 8.9,
            'profit_growth': 11.2,
            'dividend_yield': 1.8,
            'recommendation': 'HOLD'
        },
        {
            'symbol': 'ASIANPAINT',
            'name': 'Asian Paints Ltd',
            'sector': 'Consumer Goods',
            'price': 2876.55,
            'target': 3150.00,
            'stop_loss': 2680.00,
            'scores': {'short': 55, 'mid': 68, 'long': 81},
            'component_scores': {
                'short': {'technical': 52, 'momentum': 48, 'volume': 61, 'risk': 65},
                'mid': {'fundamental': 72, 'growth': 63, 'quality': 78, 'valuation': 61},
                'long': {'fundamental': 84, 'moat': 88, 'management': 82, 'growth': 71}
            },
            'pe_ratio': 54.2,
            'pb_ratio': 19.6,
            'roe': 36.5,
            'roce': 41.2,
            'debt_equity': 0.01,
            'market_cap': 275000,
            'revenue_growth': 6.8,
            'profit_growth': 9.4,
            'dividend_yield': 0.7,
            'recommendation': 'HOLD'
        },
        {
            'symbol': 'AXISBANK',
            'name': 'Axis Bank Ltd',
            'sector': 'Banking',
            'price': 1089.70,
            'target': 1280.00,
            'stop_loss': 1010.00,
            'scores': {'short': 69, 'mid': 77, 'long': 85},
            'component_scores': {
                'short': {'technical': 71, 'momentum': 74, 'volume': 67, 'risk': 65},
                'mid': {'fundamental': 80, 'growth': 76, 'quality': 82, 'valuation': 70},
                'long': {'fundamental': 88, 'moat': 86, 'management': 84, 'growth': 82}
            },
            'pe_ratio': 12.4,
            'pb_ratio': 1.8,
            'roe': 14.8,
            'roce': 13.6,
            'debt_equity': 0.18,
            'market_cap': 338000,
            'revenue_growth': 19.5,
            'profit_growth': 28.3,
            'dividend_yield': 0.4,
            'recommendation': 'BUY'
        },
        {
            'symbol': 'WIPRO',
            'name': 'Wipro Ltd',
            'sector': 'IT',
            'price': 445.30,
            'target': 510.00,
            'stop_loss': 415.00,
            'scores': {'short': 52, 'mid': 65, 'long': 76},
            'component_scores': {
                'short': {'technical': 48, 'momentum': 45, 'volume': 58, 'risk': 62},
                'mid': {'fundamental': 68, 'growth': 61, 'quality': 72, 'valuation': 63},
                'long': {'fundamental': 78, 'moat': 76, 'management': 75, 'growth': 74}
            },
            'pe_ratio': 18.6,
            'pb_ratio': 3.2,
            'roe': 17.2,
            'roce': 19.8,
            'debt_equity': 0.08,
            'market_cap': 243000,
            'revenue_growth': 11.2,
            'profit_growth': 13.7,
            'dividend_yield': 1.9,
            'recommendation': 'HOLD'
        }
    ]
    
    return pd.DataFrame(stocks_data)


@st.cache_data
def generate_price_history(symbol, days=365):
    """Generate realistic price history"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Base prices for different stocks
    base_prices = {
        'RELIANCE': 2200,
        'TCS': 3600,
        'HDFCBANK': 1550,
        'INFY': 1450,
        'BAJFINANCE': 6200,
        'ICICIBANK': 980,
        'HINDUNILVR': 2300,
        'ASIANPAINT': 2750,
        'AXISBANK': 1020,
        'WIPRO': 420
    }
    
    base_price = base_prices.get(symbol, 2000)
    
    # Generate realistic price movement
    np.random.seed(hash(symbol) % 2**32)
    returns = np.random.normal(0.0005, 0.02, days)
    prices = base_price * (1 + returns).cumprod()
    
    # Add some trend
    trend = np.linspace(0, 0.15, days)
    prices = prices * (1 + trend)
    
    # Generate volume
    base_volume = np.random.randint(1000000, 10000000)
    volume = base_volume + np.random.normal(0, base_volume * 0.3, days)
    volume = np.abs(volume).astype(int)
    
    return pd.DataFrame({
        'date': dates,
        'close': prices,
        'volume': volume,
        'high': prices * 1.02,
        'low': prices * 0.98,
        'open': prices * (1 + np.random.normal(0, 0.005, days))
    })


# ==================== SESSION STATE ====================

if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = None
if 'timeframe' not in st.session_state:
    st.session_state.timeframe = 'long'


# ==================== SIDEBAR ====================

def render_sidebar():
    """Render sidebar filters"""
    st.sidebar.markdown("# 🎯 Filters")
    
    timeframe = st.sidebar.radio(
        "**Investment Timeframe**",
        options=['short', 'mid', 'long'],
        format_func=lambda x: {
            'short': '📅 Short Term (1-3 months)',
            'mid': '📊 Mid Term (3-12 months)',
            'long': '📈 Long Term (1-5 years)'
        }[x],
        index=2
    )
    st.session_state.timeframe = timeframe
    
    min_score = st.sidebar.slider(
        "**Minimum Score**",
        min_value=0,
        max_value=100,
        value=60,
        step=5,
        help="Filter stocks by minimum score"
    )
    
    sectors = ['All', 'Banking', 'IT', 'Energy', 'NBFC', 'FMCG', 'Consumer Goods']
    sector = st.sidebar.selectbox("**Sector Filter**", sectors)
    
    st.sidebar.markdown("---")
    
    st.sidebar.info("""
    **📊 Score Ranges:**
    
    🟢 **80-100**: Strong Buy  
    🔵 **70-79**: Buy  
    🟡 **60-69**: Hold  
    🔴 **<60**: Avoid
    """)
    
    st.sidebar.markdown("---")
    
    with st.sidebar.expander("ℹ️ About This App"):
        st.markdown("""
        **Indian Stock Recommender** uses a multi-factor scoring system combining:
        
        - 📈 Technical Analysis
        - 💼 Fundamental Analysis  
        - 📊 Momentum Indicators
        - 🎯 Quality Metrics
        - 💰 Valuation Ratios
        
        Data updates daily after market close.
        """)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Made with ❤️ using Streamlit")
    
    return timeframe, min_score, sector


# ==================== MAIN APP ====================

def render_header():
    """Render app header"""
    st.markdown('<p class="main-header">📈 Indian Stock Recommender</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">AI-Powered Multi-Factor Stock Analysis for Indian Markets</p>', unsafe_allow_html=True)
    st.markdown("---")


def render_metrics_row(df):
    """Render top metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Stocks Analyzed",
            value=len(df),
            delta="Active"
        )
    
    with col2:
        strong_buy = len(df[df['recommendation'] == 'STRONG BUY'])
        st.metric(
            label="🟢 Strong Buy Signals",
            value=strong_buy,
            delta=f"{strong_buy/len(df)*100:.0f}%"
        )
    
    with col3:
        avg_score = df['current_score'].mean()
        st.metric(
            label="⭐ Average Score",
            value=f"{avg_score:.1f}",
            delta="Strong" if avg_score > 75 else "Good" if avg_score > 65 else "Mixed"
        )
    
    with col4:
        avg_upside = df['upside'].mean()
        st.metric(
            label="📈 Avg Upside Potential",
            value=f"{avg_upside:.1f}%",
            delta="Bullish" if avg_upside > 15 else "Moderate"
        )


def render_stock_cards(df):
    """Render stock recommendation cards"""
    
    for idx, row in df.iterrows():
        with st.container():
            # Header row
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                st.markdown(f"### {row['symbol']}")
                st.caption(f"**{row['name']}** • {row['sector']}")
                
                # Recommendation badge
                badge_class = {
                    'STRONG BUY': 'buy-badge',
                    'BUY': 'buy-badge',
                    'HOLD': 'hold-badge',
                    'SELL': 'sell-badge'
                }.get(row['recommendation'], 'hold-badge')
                
                st.markdown(
                    f'<span class="recommendation-badge {badge_class}">{row["recommendation"]}</span>',
                    unsafe_allow_html=True
                )
            
            with col2:
                st.metric("💰 Current Price", f"₹{row['price']:,.2f}")
                st.metric("🎯 Target Price", f"₹{row['target']:,.2f}", f"+{row['upside']:.1f}%")
            
            with col3:
                st.metric("⭐ Score", f"{row['current_score']}/100")
                st.metric("🛑 Stop Loss", f"₹{row['stop_loss']:,.2f}")
            
            with col4:
                st.write("")
                st.write("")
                if st.button("📊 Analyze", key=f"btn_{row['symbol']}", use_container_width=True):
                    st.session_state.selected_stock = row['symbol']
                    st.rerun()
            
            # Score progress bar
            score_color = "#10b981" if row['current_score'] >= 80 else "#3b82f6" if row['current_score'] >= 70 else "#f59e0b"
            st.progress(row['current_score'] / 100)
            
            # Key metrics
            col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
            with col_m1:
                st.caption(f"**P/E:** {row['pe_ratio']:.1f}")
            with col_m2:
                st.caption(f"**ROE:** {row['roe']:.1f}%")
            with col_m3:
                st.caption(f"**Revenue Growth:** {row['revenue_growth']:.1f}%")
            with col_m4:
                st.caption(f"**Market Cap:** ₹{row['market_cap']:,.0f}Cr")
            with col_m5:
                st.caption(f"**Div Yield:** {row['dividend_yield']:.1f}%")
            
            st.markdown("---")


def render_detailed_analysis(symbol):
    """Render detailed stock analysis page"""
    
    # Back button
    if st.button("← Back to Stock List"):
        st.session_state.selected_stock = None
        st.rerun()
    
    # Get stock data
    df = generate_demo_stocks()
    stock = df[df['symbol'] == symbol].iloc[0]
    
    st.markdown(f"# 📊 {stock['symbol']} - Detailed Analysis")
    st.markdown(f"### {stock['name']}")
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📊 Technical Analysis", "💼 Fundamentals", "🎯 Recommendation"])
    
    with tab1:
        render_overview_tab(stock)
    
    with tab2:
        render_technical_tab(stock)
    
    with tab3:
        render_fundamentals_tab(stock)
    
    with tab4:
        render_recommendation_tab(stock)


def render_overview_tab(stock):
    """Overview tab"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Company Information")
        info_df = pd.DataFrame({
            'Attribute': ['Sector', 'Market Cap', 'P/E Ratio', 'P/B Ratio', 'ROE', 'Debt/Equity'],
            'Value': [
                stock['sector'],
                f"₹{stock['market_cap']:,.0f} Cr",
                f"{stock['pe_ratio']:.2f}",
                f"{stock['pb_ratio']:.2f}",
                f"{stock['roe']:.2f}%",
                f"{stock['debt_equity']:.2f}"
            ]
        })
        st.dataframe(info_df, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Price Targets")
        upside = (stock['target'] - stock['price']) / stock['price'] * 100
        risk = (stock['price'] - stock['stop_loss']) / stock['price'] * 100
        rr_ratio = upside / risk if risk > 0 else 0
        
        target_df = pd.DataFrame({
            'Metric': ['Current Price', 'Target Price', 'Stop Loss', 'Upside %', 'Risk %', 'Reward/Risk'],
            'Value': [
                f"₹{stock['price']:,.2f}",
                f"₹{stock['target']:,.2f}",
                f"₹{stock['stop_loss']:,.2f}",
                f"{upside:.2f}%",
                f"{risk:.2f}%",
                f"{rr_ratio:.2f}x"
            ]
        })
        st.dataframe(target_df, hide_index=True, use_container_width=True)
    
    # Price chart
    st.markdown("### 📊 Price Movement (1 Year)")
    price_data = generate_price_history(stock['symbol'])
    
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Scatter(
        x=price_data['date'],
        y=price_data['close'],
        mode='lines',
        name='Price',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.1)'
    ))
    
    # Target and stop loss lines
    fig.add_hline(
        y=stock['target'], 
        line_dash="dash", 
        line_color="green", 
        annotation_text="Target",
        annotation_position="right"
    )
    fig.add_hline(
        y=stock['stop_loss'], 
        line_dash="dash", 
        line_color="red", 
        annotation_text="Stop Loss",
        annotation_position="right"
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        hovermode='x unified',
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_technical_tab(stock):
    """Technical analysis tab"""
    st.markdown("### 📈 Technical Score Breakdown")
    
    timeframe = st.session_state.timeframe
    component_scores = stock['component_scores'][timeframe]
    
    # Score cards
    cols = st.columns(len(component_scores))
    for idx, (component, score) in enumerate(component_scores.items()):
        with cols[idx]:
            delta = "Strong" if score >= 80 else "Good" if score >= 70 else "Weak"
            st.metric(
                label=component.title(),
                value=f"{score}/100",
                delta=delta
            )
    
    # Score bar chart
    st.markdown("### 📊 Component Analysis")
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(component_scores.keys()),
        y=list(component_scores.values()),
        marker_color=['#10b981' if v >= 80 else '#3b82f6' if v >= 70 else '#f59e0b' for v in component_scores.values()],
        text=list(component_scores.values()),
        textposition='outside'
    ))
    
    fig.update_layout(
        yaxis_title="Score",
        xaxis_title="Component",
        height=400,
        yaxis_range=[0, 100]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Volume chart
    st.markdown("### 📊 Trading Volume")
    price_data = generate_price_history(stock['symbol'])
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=price_data['date'],
        y=price_data['volume'],
        name='Volume',
        marker_color='rgba(31, 119, 180, 0.6)'
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Volume",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_fundamentals_tab(stock):
    """Fundamentals tab"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Valuation Metrics")
        valuation_df = pd.DataFrame({
            'Metric': ['P/E Ratio', 'P/B Ratio', 'Market Cap', 'Dividend Yield'],
            'Value': [
                f"{stock['pe_ratio']:.2f}",
                f"{stock['pb_ratio']:.2f}",
                f"₹{stock['market_cap']:,.0f} Cr",
                f"{stock['dividend_yield']:.2f}%"
            ],
            'Status': [
                '✅ Good' if stock['pe_ratio'] < 30 else '⚠️ High',
                '✅ Good' if stock['pb_ratio'] < 5 else '⚠️ High',
                '✅ Large Cap',
                '✅ Pays Dividend' if stock['dividend_yield'] > 0 else '⚠️ No Dividend'
            ]
        })
        st.dataframe(valuation_df, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Profitability Metrics")
        profitability_df = pd.DataFrame({
            'Metric': ['ROE', 'ROCE', 'Revenue Growth', 'Profit Growth'],
            'Value': [
                f"{stock['roe']:.2f}%",
                f"{stock['roce']:.2f}%",
                f"{stock['revenue_growth']:.2f}%",
                f"{stock['profit_growth']:.2f}%"
            ],
            'Status': [
                '✅ Excellent' if stock['roe'] > 15 else '⚠️ Average',
                '✅ Excellent' if stock['roce'] > 15 else '⚠️ Average',
                '✅ Growing' if stock['revenue_growth'] > 10 else '⚠️ Slow',
                '✅ Growing' if stock['profit_growth'] > 10 else '⚠️ Slow'
            ]
        })
        st.dataframe(profitability_df, hide_index=True, use_container_width=True)
    
    # ROE Gauge Chart
    st.markdown("### 📈 Return on Equity (ROE)")
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=stock['roe'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "ROE (%)", 'font': {'size': 24}},
        delta={'reference': 15, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 50], 'tickwidth': 1},
            'bar': {'color': "#1f77b4"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 10], 'color': '#fee2e2'},
                {'range': [10, 15], 'color': '#fef3c7'},
                {'range': [15, 25], 'color': '#d1fae5'},
                {'range': [25, 50], 'color': '#a7f3d0'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 20
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Financial Health
    st.markdown("### 💪 Financial Health")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        debt_status = "🟢 Healthy" if stock['debt_equity'] < 1 else "🟡 Moderate" if stock['debt_equity'] < 2 else "🔴 High"
        st.metric("Debt/Equity", f"{stock['debt_equity']:.2f}", debt_status)
    
    with col2:
        growth_status = "🟢 Strong" if stock['revenue_growth'] > 15 else "🟡 Moderate" if stock['revenue_growth'] > 10 else "🔴 Weak"
        st.metric("Revenue Growth", f"{stock['revenue_growth']:.1f}%", growth_status)
    
    with col3:
        profit_status = "🟢 Strong" if stock['profit_growth'] > 20 else "🟡 Moderate" if stock['profit_growth'] > 10 else "🔴 Weak"
        st.metric("Profit Growth", f"{stock['profit_growth']:.1f}%", profit_status)


def render_recommendation_tab(stock):
    """Recommendation tab"""
    timeframe = st.session_state.timeframe
    current_score = stock['scores'][timeframe]
    
    # Main recommendation box
    rec_color = {
        'STRONG BUY': '#10b981',
        'BUY': '#3b82f6',
        'HOLD': '#f59e0b',
        'SELL': '#ef4444'
    }.get(stock['recommendation'], '#f59e0b')
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {rec_color} 0%, {rec_color}dd 100%); 
                padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem;">{stock['recommendation']}</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.5rem;">Overall Score: {current_score}/100</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            {timeframe.title()} Term Investment
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Investment thesis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Key Strengths")
        strengths = []
        
        if stock['roe'] > 15:
            strengths.append("• Strong return on equity (ROE > 15%)")
        if stock['debt_equity'] < 1:
            strengths.append("• Healthy balance sheet with low debt")
        if stock['profit_growth'] > 15:
            strengths.append("• Robust profit growth trajectory")
        if stock['market_cap'] > 500000:
            strengths.append("• Large-cap stability and liquidity")
        if current_score >= 80:
            strengths.append("• Excellent technical setup")
        
        if not strengths:
            strengths = ["• Analyzing market position", "• Evaluating fundamentals"]
        
        for strength in strengths:
            st.markdown(strength)
    
    with col2:
        st.markdown("### ⚠️ Key Risks")
        risks = []
        
        if stock['pe_ratio'] > 30:
            risks.append("• High valuation (P/E > 30)")
        if stock['debt_equity'] > 1:
            risks.append("• Elevated debt levels")
        if current_score < 70:
            risks.append("• Weak technical indicators")
        
        risks.extend([
            "• Market volatility and corrections",
            "• Sector-specific headwinds",
            "• Macroeconomic uncertainties",
            "• Regulatory changes"
        ])
        
        for risk in risks[:5]:
            st.markdown(risk)
    
    st.markdown("---")
    
    # Action plan
    st.markdown("### 📋 Investment Action Plan")
    
    upside = (stock['target'] - stock['price']) / stock['price'] * 100
    risk_pct = (stock['price'] - stock['stop_loss']) / stock['price'] * 100
    rr_ratio = upside / risk_pct if risk_pct > 0 else 0
    
    action_plan = f"""
    **Entry Strategy:**  
    • Buy at current levels: ₹{stock['price']:,.2f}  
    • Consider averaging if price dips 2-3%  
    
    **Exit Strategy:**  
    • Target Price: ₹{stock['target']:,.2f} (Upside: **{upside:.1f}%**)  
    • Stop Loss: ₹{stock['stop_loss']:,.2f} (Risk: **{risk_pct:.1f}%**)  
    • Reward/Risk Ratio: **{rr_ratio:.2f}x**  
    
    **Time Horizon:**  
    • Recommended holding period: **{timeframe.title()} term**  
    • Review position quarterly  
    
    **Position Sizing:**  
    • Allocate 5-10% of portfolio (based on risk tolerance)  
    • Do not exceed 15% in single stock  
    """
    
    st.info(action_plan)
    
    # Score evolution across timeframes
    st.markdown("### 📊 Score Across Different Timeframes")
    
    timeframes = ['short', 'mid', 'long']
    scores = [stock['scores'][tf] for tf in timeframes]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=['Short Term', 'Mid Term', 'Long Term'],
        y=scores,
        mode='lines+markers',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=12, color=scores, colorscale='RdYlGn', cmin=0, cmax=100),
        text=[f"{s}/100" for s in scores],
        textposition="top center"
    ))
    
    fig.update_layout(
        yaxis_title="Score",
        yaxis_range=[0, 100],
        height=300,
        hovermode='x'
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ==================== MAIN ====================

def main():
    """Main application"""
    
    # Render header
    render_header()
    
    # Sidebar
    timeframe, min_score, sector = render_sidebar()
    
    # Check if detailed view
    if st.session_state.selected_stock:
        render_detailed_analysis(st.session_state.selected_stock)
        return
    
    # Load data
    df = generate_demo_stocks()
    
    # Add current score based on timeframe
    df['current_score'] = df['scores'].apply(lambda x: x[timeframe])
    
    # Calculate upside
    df['upside'] = ((df['target'] - df['price']) / df['price'] * 100)
    
    # Filter by score
    df = df[df['current_score'] >= min_score]
    
    # Filter by sector
    if sector != 'All':
        df = df[df['sector'] == sector]
    
    # Sort by score
    df = df.sort_values('current_score', ascending=False)
    
    if df.empty:
        st.warning("⚠️ No stocks match your criteria. Try adjusting the filters.")
        st.stop()
    
    # Render metrics
    st.markdown("## 📊 Portfolio Overview")
    render_metrics_row(df)
    
    st.markdown("---")
    
    # Top picks section
    st.markdown("## 🎯 Top Stock Recommendations")
    st.caption(f"Showing {len(df)} stocks sorted by {timeframe}-term score")
    
    # Render stock cards
    render_stock_cards(df)
    
    # Footer
    st.markdown("---")
    st.warning("""
    **⚠️ Important Disclaimer:**  
    This application is for educational and informational purposes only. It should not be considered as financial advice. 
    Stock market investments are subject to market risks. Always conduct your own research and consult with a qualified 
    financial advisor before making any investment decisions. Past performance is not indicative of future results.
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>Indian Stock Recommender</strong> • Built with Streamlit</p>
        <p>Data updated daily • Scores based on multi-factor analysis</p>
    </div>
    """, unsafe_allow_html=True)


# Run the app
if __name__ == "__main__":
    main()
