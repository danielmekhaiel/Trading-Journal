import streamlit as st
import plotly.express as px
import pandas as pd
from journal_db import get_all_trades

def render_analytics():
    st.title("🧬 Optimization Engine: Runner Left-On-Table Analysis")
    st.markdown("---")
    
    df = get_all_trades()
    
    if df.empty:
        st.info("Insufficient data to generate runner capture modeling.")
        return

    # Filter trades that have valid high watermark tracking data
    df_valid = df[df['max_contract_price'].notna() & (df['max_contract_price'] > 0)].copy()
    
    if df_valid.empty:
        st.warning("Please populate the 'Contract High Watermark' metric in your journal logging to model runner retention.")
        return

    # Calculate theoretical maximum yield per contract entry
    df_valid['Max_Possible_PnL'] = (df_valid['max_contract_price'] - df_valid['entry_price']) * df_valid['contracts'] * 100.0
    df_valid['Left_On_Table'] = df_valid['Max_Possible_PnL'] - df_valid['pnl']
    
    total_left_on_table = df_valid['Left_On_Table'].sum()
    total_realized_pnl = df_valid['pnl'].sum()
    
    # Statistical Summary Blocks
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Realized Cash Capital", f"${total_realized_pnl:,.2f}")
    with col2:
        st.metric("Total Alpha Left On Table", f"${total_left_on_table:,.2f}", delta=f"${total_left_on_table:,.2f}", delta_color="inverse")
    with col3:
        avg_efficiency = (df_valid['pnl'].sum() / df_valid['Max_Possible_PnL'].sum() * 100) if df_valid['Max_Possible_PnL'].sum() > 0 else 0
        st.metric("Runner Capture Efficiency", f"{avg_efficiency:.1f}%")

    st.markdown("### 📊 Realized P&L vs. Maximum Theoretical Expansion")
    
    # Restructure chart coordinates for clean plotting side-by-side
    chart_data = []
    for idx, row in df_valid.iterrows():
        chart_data.append({"Trade Group": f"#{row['ticker']} ({row['date']})", "PnL Type": "Realized Profit", "Value ($)": row['pnl']})
        chart_data.append({"Trade Group": f"#{row['ticker']} ({row['date']})", "PnL Type": "Max Potential", "Value ($)": row['Max_Possible_PnL']})
        
    chart_df = pd.DataFrame(chart_data)
    
    fig = px.bar(
        chart_df, 
        x="Trade Group", 
        y="Value ($)", 
        color="PnL Type", 
        barmode="group",
        color_discrete_map={"Realized Profit": "#552583", "Max Potential": "#FDB927"} # Technical Master Purple & Gold
    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    > **Structural Playbook Tip:** If your Capture Efficiency is consistently hovering below 40%, it indicates your entry timing is highly accurate, but your 5-minute breakeven trailing stop is sitting directly inside the asset's typical market noise layer. Consider locking your protective stops under **15-minute structural swing lows** or structural gray imbalance boxes instead.
    """)
