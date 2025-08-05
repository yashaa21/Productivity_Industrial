import streamlit as st
import math
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Productivity Calculator Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for modern, attractive design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header with animated gradient */
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease infinite;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(238, 119, 82, 0.3);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    .metric-card h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #f8f9fa;
    }
    
    .metric-card h2 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Enhanced input sections */
    .input-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 25px;
        margin: 1.5rem 0;
        border: none;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .input-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    
    .input-section:hover::before {
        transform: translateX(100%);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 25px rgba(255, 107, 107, 0.4);
        background: linear-gradient(45deg, #4ecdc4, #ff6b6b);
    }
    
    /* Enhanced sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Section headers */
    .section-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 20px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.3);
    }
    
    /* Tips section */
    .tips-section {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        padding: 1.5rem;
        border-radius: 20px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.2);
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #e9ecef;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 15px;
        border: 2px solid #e9ecef;
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        border-radius: 15px;
        padding: 1rem;
        color: white;
        font-weight: 600;
    }
    
    /* Info message styling */
    .stInfo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1rem;
        color: white;
        font-weight: 600;
    }
    
    /* Background gradient */
    .main .block-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 2rem;
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Floating animation for elements */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Pulse animation for important elements */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# Productivity calculation functions
def total_productivity(output, total_input):
    return output / total_input if total_input != 0 else 0

def labour_productivity(output, labour_input):
    return output / labour_input if labour_input != 0 else 0

def material_productivity(output, material_input):
    return output / material_input if material_input != 0 else 0

def capital_productivity(output, capital_input):
    return output / capital_input if capital_input != 0 else 0

def machine_productivity(output, machine_input):
    return output / machine_input if machine_input != 0 else 0

def miscellaneous_productivity(output, misc_input):
    return output / misc_input if misc_input != 0 else 0

def multifactor_productivity(output, human, material, capital, energy, misc):
    total_input = human + material + capital + energy + misc
    return output / total_input if total_input != 0 else 0

def total_factor_productivity(net_output, worker_input, machine_input):
    total_input = worker_input + machine_input
    return net_output / total_input if total_input != 0 else 0

def calculate_eoq(demand, ordering_cost, holding_cost):
    return math.sqrt((2 * demand * ordering_cost) / holding_cost) if holding_cost != 0 else 0

# Main app
def main():
    # Enhanced Header with floating animation
    st.markdown('<h1 class="main-header floating">🚀 Productivity Calculator Pro</h1>', unsafe_allow_html=True)
    
    # Enhanced Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Calculator Type")
        calc_type = st.selectbox(
            "Choose calculation type:",
            [
                "Total Productivity",
                "Labour Productivity", 
                "Material Productivity",
                "Capital Productivity",
                "Machine Productivity",
                "Miscellaneous Productivity",
                "Multifactor Productivity",
                "Total Factor Productivity",
                "Economic Order Quantity (EOQ)"
            ]
        )
        
        st.markdown("---")
        st.markdown("### ✨ Features")
        st.markdown("• 🎨 Interactive calculations")
        st.markdown("• 📊 Visual charts & graphs")
        st.markdown("• 📈 Historical tracking")
        st.markdown("• 💾 Export results")
        st.markdown("• 🎯 Real-time analytics")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("This advanced calculator helps you measure various types of productivity metrics and optimize your operations with beautiful visualizations.")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f'<h2 class="section-header pulse">{calc_type}</h2>', unsafe_allow_html=True)
        
        # Input section based on calculation type
        if calc_type == "Total Productivity":
            with st.container():
                st.markdown('<div class="input-section">', unsafe_allow_html=True)
                output = st.number_input("📈 Total Output", min_value=0.0, value=1000.0, step=100.0)
                total_input = st.number_input("📥 Total Input", min_value=0.0, value=800.0, step=100.0)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Calculate Total Productivity", key="calc_total"):
                    result = total_productivity(output, total_input)
                    st.markdown(f'<div class="metric-card"><h3>Total Productivity</h3><h2>{result:.2%}</h2></div>', unsafe_allow_html=True)
                    
                    # Enhanced visualization
                    with st.container():
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        fig = go.Figure()
                        fig.add_trace(go.Indicator(
                            mode="gauge+number+delta",
                            value=result * 100,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Productivity %", 'font': {'size': 24, 'color': '#667eea'}},
                            delta={'reference': 100, 'font': {'size': 16}},
                            gauge={
                                'axis': {'range': [None, 150], 'tickwidth': 1, 'tickcolor': "#667eea"},
                                'bar': {'color': "#667eea"},
                                'bgcolor': "white",
                                'borderwidth': 2,
                                'bordercolor': "#667eea",
                                'steps': [
                                    {'range': [0, 50], 'color': "#ff6b6b"},
                                    {'range': [50, 100], 'color': "#feca57"},
                                    {'range': [100, 150], 'color': "#48dbfb"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 100
                                }
                            }
                        ))
                        fig.update_layout(
                            height=400,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#667eea'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Labour Productivity":
            with st.container():
                st.markdown('<div class="input-section">', unsafe_allow_html=True)
                output = st.number_input("📈 Total Output", min_value=0.0, value=1000.0, step=100.0)
                labour = st.number_input("👥 Labour Input", min_value=0.0, value=200.0, step=50.0)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Calculate Labour Productivity", key="calc_labour"):
                    result = labour_productivity(output, labour)
                    st.markdown(f'<div class="metric-card"><h3>Labour Productivity</h3><h2>{result:.2%}</h2></div>', unsafe_allow_html=True)
                    
                    # Enhanced bar chart
                    with st.container():
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        data = pd.DataFrame({
                            'Metric': ['Output', 'Labour Input'],
                            'Value': [output, labour]
                        })
                        fig = px.bar(data, x='Metric', y='Value', 
                                    title="Output vs Labour Input",
                                    color='Metric',
                                    color_discrete_map={'Output': '#667eea', 'Labour Input': '#764ba2'})
                        fig.update_layout(
                            title_font_size=20,
                            title_font_color='#667eea',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#667eea'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Material Productivity":
            with st.container():
                st.markdown('<div class="input-section">', unsafe_allow_html=True)
                output = st.number_input("📈 Total Output", min_value=0.0, value=1000.0, step=100.0)
                material = st.number_input("📦 Material Input", min_value=0.0, value=300.0, step=50.0)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Calculate Material Productivity", key="calc_material"):
                    result = material_productivity(output, material)
                    st.markdown(f'<div class="metric-card"><h3>Material Productivity</h3><h2>{result:.2%}</h2></div>', unsafe_allow_html=True)
                    
                    # Enhanced pie chart
                    with st.container():
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        fig = go.Figure(data=[go.Pie(
                            labels=['Output', 'Material Input'], 
                            values=[output, material],
                            hole=0.4,
                            marker_colors=['#667eea', '#764ba2'],
                            textinfo='label+percent',
                            textfont_size=16
                        )])
                        fig.update_layout(
                            title="Output vs Material Input Distribution",
                            title_font_size=20,
                            title_font_color='#667eea',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Capital Productivity":
            with st.container():
                st.markdown('<div class="input-section">', unsafe_allow_html=True)
                output = st.number_input("📈 Total Output", min_value=0.0, value=1000.0, step=100.0)
                capital = st.number_input("💰 Capital Input", min_value=0.0, value=250.0, step=50.0)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Calculate Capital Productivity", key="calc_capital"):
                    result = capital_productivity(output, capital)
                    st.markdown(f'<div class="metric-card"><h3>Capital Productivity</h3><h2>{result:.2%}</h2></div>', unsafe_allow_html=True)
                    
                    # Enhanced line chart
                    with st.container():
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=['Capital Input', 'Output'], 
                            y=[capital, output], 
                            mode='lines+markers', 
                            name='Productivity Flow',
                            line=dict(color='#667eea', width=4),
                            marker=dict(size=12, color='#764ba2')
                        ))
                        fig.update_layout(
                            title="Capital Input to Output Flow",
                            title_font_size=20,
                            title_font_color='#667eea',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#667eea'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Machine Productivity":
            with st.container():
                st.markdown('<div class="input-section">', unsafe_allow_html=True)
                output = st.number_input("📈 Total Output", min_value=0.0, value=1000.0, step=100.0)
                machine_input = st.number_input("⚙️ Machine Input", min_value=0.0, value=150.0, step=25.0)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Calculate Machine Productivity", key="calc_machine"):
                    result = machine_productivity(output, machine_input)
                    st.markdown(f'<div class="metric-card"><h3>Machine Productivity</h3><h2>{result:.2%}</h2></div>', unsafe_allow_html=True)
                    
                    # Enhanced scatter plot
                    with st.container():
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        fig = px.scatter(
                            x=[machine_input], 
                            y=[output], 
                            title="Machine Input vs Output",
                            labels={'x': 'Machine Input', 'y': 'Output'},
                            color_discrete_sequence=['#667eea']
                        )
                        fig.add_trace(go.Scatter(
                            x=[0, machine_input*1.5], 
                            y=[0, output*1.5], 
                            mode='lines', 
                            name='Efficiency Line',
                            line=dict(color='#764ba2', width=3, dash='dash')
                        ))
                        fig.update_layout(
                            title_font_size=20,
                            title_font_color='#667eea',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#667eea'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Miscellaneous Productivity":
            with st.container():
                st.markdown('<div class="input-section">', unsafe_allow_html=True)
                output = st.number_input("📈 Total Output", min_value=0.0, value=1000.0, step=100.0)
                misc = st.number_input("🔧 Miscellaneous Input", min_value=0.0, value=100.0, step=25.0)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Calculate Miscellaneous Productivity", key="calc_misc"):
                    result = miscellaneous_productivity(output, misc)
                    st.markdown(f'<div class="metric-card"><h3>Miscellaneous Productivity</h3><h2>{result:.2%}</h2></div>', unsafe_allow_html=True)
                    
                    # Enhanced area chart
                    with st.container():
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=['Misc Input', 'Output'], 
                            y=[misc, output], 
                            fill='tonexty', 
                            name='Productivity Area',
                            fillcolor='rgba(102, 126, 234, 0.3)',
                            line=dict(color='#667eea', width=3)
                        ))
                        fig.update_layout(
                            title="Miscellaneous Input to Output",
                            title_font_size=20,
                            title_font_color='#667eea',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#667eea'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Multifactor Productivity":
            with st.container():
                st.markdown('<div class="input-section">', unsafe_allow_html=True)
                output = st.number_input("📈 Total Output", min_value=0.0, value=1000.0, step=100.0)
                human = st.number_input("👥 Human Input", min_value=0.0, value=200.0, step=50.0)
                material = st.number_input("📦 Material Input", min_value=0.0, value=300.0, step=50.0)
                capital = st.number_input("💰 Capital Input", min_value=0.0, value=250.0, step=50.0)
                energy = st.number_input("⚡ Energy Input", min_value=0.0, value=150.0, step=25.0)
                misc = st.number_input("🔧 Miscellaneous Input", min_value=0.0, value=100.0, step=25.0)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Calculate Multifactor Productivity", key="calc_multifactor"):
                    result = multifactor_productivity(output, human, material, capital, energy, misc)
                    st.markdown(f'<div class="metric-card"><h3>Multifactor Productivity</h3><h2>{result:.2%}</h2></div>', unsafe_allow_html=True)
                    
                    # Enhanced stacked bar chart
                    with st.container():
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        factors = ['Human', 'Material', 'Capital', 'Energy', 'Misc']
                        values = [human, material, capital, energy, misc]
                        
                        fig = go.Figure(data=[
                            go.Bar(
                                name='Input Factors', 
                                x=factors, 
                                y=values,
                                marker_color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
                            )
                        ])
                        fig.update_layout(
                            title="Input Factors Breakdown",
                            title_font_size=20,
                            title_font_color='#667eea',
                            barmode='stack',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#667eea'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Total Factor Productivity":
            with st.container():
                st.markdown('<div class="input-section">', unsafe_allow_html=True)
                net_output = st.number_input("📈 Net Output", min_value=0.0, value=800.0, step=100.0)
                worker_input = st.number_input("👷 Worker Input", min_value=0.0, value=200.0, step=50.0)
                machine_input = st.number_input("⚙️ Machine Input", min_value=0.0, value=150.0, step=25.0)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Calculate Total Factor Productivity", key="calc_tfp"):
                    result = total_factor_productivity(net_output, worker_input, machine_input)
                    st.markdown(f'<div class="metric-card"><h3>Total Factor Productivity</h3><h2>{result:.2%}</h2></div>', unsafe_allow_html=True)
                    
                    # Enhanced donut chart
                    with st.container():
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        fig = go.Figure(data=[go.Pie(
                            labels=['Worker Input', 'Machine Input'], 
                            values=[worker_input, machine_input],
                            hole=0.6,
                            marker_colors=['#667eea', '#764ba2'],
                            textinfo='label+percent',
                            textfont_size=16
                        )])
                        fig.update_layout(
                            title="Input Distribution",
                            title_font_size=20,
                            title_font_color='#667eea',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Economic Order Quantity (EOQ)":
            with st.container():
                st.markdown('<div class="input-section">', unsafe_allow_html=True)
                demand = st.number_input("📊 Annual Demand (D)", min_value=0.0, value=1000.0, step=100.0)
                ordering_cost = st.number_input("💳 Ordering Cost per Order (S)", min_value=0.0, value=50.0, step=10.0)
                holding_cost = st.number_input("📦 Holding Cost per Unit per Year (H)", min_value=0.0, value=2.0, step=0.5)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Calculate EOQ", key="calc_eoq"):
                    result = calculate_eoq(demand, ordering_cost, holding_cost)
                    st.markdown(f'<div class="metric-card"><h3>Economic Order Quantity</h3><h2>{result:.2f} units</h2></div>', unsafe_allow_html=True)
                    
                    # Enhanced cost analysis chart
                    with st.container():
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        order_quantities = list(range(50, int(result*2), 50))
                        total_costs = []
                        
                        for q in order_quantities:
                            if q > 0:
                                ordering_costs = (demand / q) * ordering_cost
                                holding_costs = (q / 2) * holding_cost
                                total_costs.append(ordering_costs + holding_costs)
                            else:
                                total_costs.append(0)
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=order_quantities, 
                            y=total_costs, 
                            mode='lines+markers', 
                            name='Total Cost',
                            line=dict(color='#667eea', width=3),
                            marker=dict(size=8, color='#764ba2')
                        ))
                        fig.add_vline(
                            x=result, 
                            line_dash="dash", 
                            line_color="red", 
                            annotation_text=f"EOQ = {result:.0f}",
                            annotation_font_size=16
                        )
                        fig.update_layout(
                            title="Total Cost vs Order Quantity", 
                            xaxis_title="Order Quantity", 
                            yaxis_title="Total Cost",
                            title_font_size=20,
                            title_font_color='#667eea',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#667eea'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced right sidebar
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Quick Stats")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample data for demonstration
        if 'calculation_history' not in st.session_state:
            st.session_state.calculation_history = []
        
        if st.button("➕ Add Sample Data"):
            sample_data = {
                'timestamp': datetime.now(),
                'type': calc_type,
                'result': 0.85
            }
            st.session_state.calculation_history.append(sample_data)
            st.success("✨ Sample data added successfully!")
        
        if st.session_state.calculation_history:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("#### 📈 Recent Calculations")
            for i, calc in enumerate(st.session_state.calculation_history[-5:]):
                st.write(f"**{calc['type']}**: {calc['result']:.2%}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<div class="tips-section">', unsafe_allow_html=True)
        st.markdown("### 💡 Tips")
        if calc_type == "Total Productivity":
            st.info("🎯 Total productivity measures overall efficiency of all inputs combined.")
        elif calc_type == "Labour Productivity":
            st.info("👥 Labour productivity indicates how efficiently human resources are utilized.")
        elif calc_type == "Material Productivity":
            st.info("📦 Material productivity shows how effectively materials are converted to output.")
        elif calc_type == "EOQ":
            st.info("📊 EOQ helps optimize inventory costs by balancing ordering and holding costs.")
        else:
            st.info("🚀 Use these metrics to identify areas for improvement and optimization.")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 