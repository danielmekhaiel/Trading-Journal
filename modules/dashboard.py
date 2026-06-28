import streamlit as st
import plotly.express as px
import pandas as pd
from journal_db import get_all_trades

def render_dashboard():
    st.title("🎛️ Fadeaway Flow Core Performance")
    st.markdown("---")
    
    df = get_all_trades()
    
    if df.empty:
        st.info("No trades logged yet. Hit the 'Journal Entry' tab in the sidebar to get started.")
        return

    # High-level Math Calculations
    total_trades = len(df)
    net_pnl = df['pnl'].sum()
    winning_trades = df[df['pnl'] > 0]
    losing_trades = df[df['pnl'] < 0]
    
    win_rate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0.0
    avg_win = winning_trades['pnl'].mean() if not winning_trades.empty else 0.0
    avg_loss = losing_trades['pnl'].mean() if not losing_trades.empty else 0.0
    profit_factor = (winning_trades['pnl'].sum() / abs(losing_trades['pnl'].sum())) if not losing_trades.empty else float('inf')

    # Metric Cards display
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Net P&L", f"${net_pnl:,.2f}", delta=f"${net_pnl:,.2f}" if net_pnl >= 0 else f"-${abs(net_pnl):,.2f}")
    with col2:
        st.metric("Win Rate", f"{win_rate:.1f}%")
    with col3:
        st.metric("Profit Factor", f"{profit_factor:.2f}" if profit_factor != float('inf') else "∞")
    with col4:
        st.metric("Total Trades", total_trades)

    st.markdown("### 📈 Equity Curve")
    # Chronological sort for the cumulative sum tracking
    df_sorted = df.iloc[::-1].copy().reset_index(drop=True)
    df_sorted['Cumulative_PnL'] = df_sorted['pnl'].cumsum()
    
    fig = px.line(
        df_sorted, 
        x=df_sorted.index + 1, 
        y='Cumulative_PnL', 
        labels={'x': 'Trade #', 'Cumulative_PnL': 'Account Growth ($)'},
        title='Cumulative Equity Trajectory'
    )
    fig.update_traces(line_color='#FFD700', line_width=3) # Master Gold line
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF')
    st.plotly_chart(fig, use_container_width=True)
