import streamlit as st
import datetime
from journal_db import add_trade, get_all_trades

def render_journal():
    st.title("📝 Technical Journal Ledger")
    st.markdown("---")
    
    st.markdown("### Log New Position")
    with st.form("trade_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            trade_date = st.date_input("Trade Date", datetime.date.today())
            ticker = st.selectbox("Symbol", ["TSLA", "NVDA", "MSFT", "AAPL", "GOOGL", "COIN", "MSTR", "IWM", "SPY", "QQQ", "CRM"])
            side = st.selectbox("Option Contract Side", ["CALL", "PUT"])
        with col2:
            setup = st.selectbox("Primary Setup Logic", ["Break-Imbalance-Retest", "Range Boundary Rejection", "Liquidity Sweep", "Orbs Breakout"])
            contracts = st.number_input("Contract Quantity", min_value=1, step=1, value=1)
            entry_price = st.number_input("Average Entry Price ($)", min_value=0.01, step=0.01, value=1.00)
        with col3:
            exit_price = st.number_input("Average Exit Price ($)", min_value=0.01, step=0.01, value=1.10)
            max_contract_price = st.number_input("Contract High Watermark ($)", min_value=0.01, step=0.01, value=1.50, help="The highest price this option contract hit while you were in it or shortly after you exited.")
            notes = st.text_area("Intraday Execution Notes", placeholder="E.g., Switched to 15m chart to filter out opening chop. Left runner at breakeven stop out.")
            
        submit_button = st.form_submit_button("Commit Position to Database")
        
        if submit_button:
            # Automatic realization of P&L: (Exit - Entry) * Contracts * Multiplier
            pnl = (exit_price - entry_price) * contracts * 100.0
            add_trade(
                trade_date.strftime("%Y-%m-%d"), ticker, side, setup, 
                int(contracts), entry_price, exit_price, max_contract_price, pnl, notes
            )
            st.success(st.session_state.get('brand_handle', 'FadeawayFlow') + " — Position successfully committed to ledger!")
            st.rerun()

    st.markdown("---")
    st.markdown("### Historical Position History")
    df = get_all_trades()
    if not df.empty:
        st.dataframe(df.drop(columns=['id']), use_container_width=True)
    else:
        st.info("No historical positions currently populated in SQLite storage.")
