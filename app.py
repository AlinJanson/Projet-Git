import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- FIX: Import from the 'src' folder ---
import data_loader
import quant_a
import quant_b
import prediction


# 1. Page Config
st.set_page_config(page_title="Asset Management Dashboard", layout="wide")
st.title("📈 Quantitative Asset Management Platform")

# 2. Sidebar - Global Inputs
st.sidebar.header("Configuration")
tickers_input = st.sidebar.text_input("Tickers (comma separated)", "AAPL, MSFT, GOOG")
tickers = [t.strip().upper() for t in tickers_input.split(",")]

period = st.sidebar.selectbox("Period", ["1y", "2y", "5y", "max"], index=0)

# Load Data
if st.sidebar.button("Load Data"):
    with st.spinner('Fetching data from Yahoo Finance...'):
        df = data_loader.fetch_data(tickers, period=period)
        
    if df is None or df.empty:
        st.error("Error loading data. Check tickers.")
    else:
        st.session_state['data'] = df
        st.success("Data loaded successfully!")

# Ensure data is loaded before showing tabs
if 'data' in st.session_state:
    df = st.session_state['data']
    
    # Create Tabs
    tab1, tab2, tab3 = st.tabs(["Quant A: Single Asset", "Quant B: Portfolio", "Prediction"])

    # --- TAB 1: QUANT A (Strategy) ---
    with tab1:
        st.subheader("Single Asset Strategy Analysis")
        selected_asset = st.selectbox("Select Asset for Analysis", tickers)
        
        # Prepare single asset dataframe
        if isinstance(df.columns, pd.MultiIndex):
            # Safe extraction for multi-index
            try:
                single_df = df.xs(selected_asset, level=1, axis=1) if selected_asset in df.columns.levels[1] else pd.DataFrame(df[selected_asset])
                # Ensure column is named 'Close' for quant_a
                if 'Close' not in single_df.columns and selected_asset in df.columns:
                     single_df = df[[selected_asset]].rename(columns={selected_asset: 'Close'})
                elif 'Close' not in single_df.columns:
                     # Fallback if xs returns series or different structure
                     single_df = pd.DataFrame({'Close': df[selected_asset]['Close']})
            except:
                 st.warning("Data structure mismatch. attempting fallback.")
                 single_df = pd.DataFrame({'Close': df['Close'][selected_asset]})
        else:
            single_df = df[['Close']] # Assuming single ticker download

        # Apply Strategy
        df_strategy = quant_a.apply_strategies(single_df)
        
        # Metrics
        metrics = quant_a.compute_performance_metrics(df_strategy)
        col1, col2, col3 = st.columns(3)
        col1.metric("Sharpe Ratio", metrics["Sharpe Ratio"])
        col2.metric("Max Drawdown", metrics["Max Drawdown"])
        col3.metric("Volatility", metrics["Volatility"])
        
        # Plot
        st.line_chart(df_strategy[['Buy_Hold_Cum', 'Momentum_Cum']])

    # --- TAB 2: QUANT B (Portfolio) ---
    with tab2:
        st.subheader("Portfolio Simulation")
        
        # Weights Input
        weights = {}
        cols = st.columns(len(tickers))
        for i, ticker in enumerate(tickers):
            weights[ticker] = cols[i].number_input(f"Weight {ticker}", 0.0, 1.0, 1.0/len(tickers))
            
        # Strategy Selector
        rebal_strat = st.radio("Rebalancing Strategy", ["Buy & Hold", "Daily Rebalancing"])
        
        if sum(weights.values()) > 0:
            # Process Data
            df_clean = quant_b.clean_data_for_portfolio(df, tickers)
            df_portfolio = quant_b.simulate_portfolio(df_clean, weights, rebal_strat)
            
            # KPIS
            kpis = quant_b.compute_portfolio_kpis(df_portfolio, weights)
            
            # Display KPIs
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Annual Return", f"{kpis['annual_return']:.2%}")
            c2.metric("Portfolio Volatility", f"{kpis['portfolio_volatility']:.2%}")
            c3.metric("Diversification Benefit", f"{kpis['diversification_effect']:.2%}")
            c4.metric("Sharpe Ratio", f"{kpis['sharpe_ratio']:.2f}")
            
            # Charts
            st.line_chart(df_portfolio)
            
            # Correlation Matrix
            st.write("Correlation Matrix:")
            import plotly.express as px
            fig_corr = px.imshow(kpis['correlation_matrix'], text_auto=True, color_continuous_scale='RdBu_r')
            st.plotly_chart(fig_corr)

    # --- TAB 3: PREDICTION ---
    with tab3:
        st.subheader("Linear Regression Prediction")
        pred_asset = st.selectbox("Select Asset to Predict", tickers, key='pred')
        days = st.slider("Days to predict", 7, 90, 30)
        
        # Prepare Data (similar to Tab 1)
        # Simplified extraction for prediction (assuming 'Close' exists or is Series)
        try:
             # Try generic extraction
             if isinstance(df.columns, pd.MultiIndex):
                 target_series = df.xs(pred_asset, level=1, axis=1)['Close']
             else:
                 target_series = df['Close']
        except:
             # Fallback
             target_series = df[pred_asset] if pred_asset in df.columns else df.iloc[:,0]

        df_pred_input = pd.DataFrame({'Close': target_series})
        
        # Predict
        df_forecast = prediction.predict_linear_regression(df_pred_input, days)
        
        # Plot
        st.write("Forecast vs History (Last 6 months focus)")
        # Combine for charting
        combined = pd.concat([df_pred_input.iloc[-150:], df_forecast])
        st.line_chart(combined)

else:
    st.info("Please enter tickers and click 'Load Data' in the sidebar.")