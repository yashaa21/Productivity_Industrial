import streamlit as st
import math
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Productivity Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, formal CSS styling
st.markdown("""
<style>
    /* Import clean, professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 1rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e9ecef;
        padding: 1.5rem;
        border-radius: 8px;
        color: #2c3e50;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card h3 {
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        color: #6c757d;
    }
    
    .metric-card h2 {
        font-size: 2.5rem;
        font-weight: 600;
        margin: 0;
        color: #2c3e50;
    }
    
    /* Input sections */
    .input-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    /* Buttons */
    .stButton > button {
        background: #007bff;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 1rem;
        transition: background-color 0.2s ease;
        margin: 1rem 0;
    }
    
    .stButton > button:hover {
        background: #0056b3;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        border-bottom: 1px solid #ecf0f1;
        padding-bottom: 0.5rem;
    }
    
    /* Stats cards */
    .stats-card {
        background: #ffffff;
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 6px;
        color: #2c3e50;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Tips section */
    .tips-section {
        background: #e3f2fd;
        border: 1px solid #bbdefb;
        padding: 1rem;
        border-radius: 6px;
        color: #1565c0;
        margin: 0.5rem 0;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        border-radius: 4px;
        border: 1px solid #ced4da;
        padding: 0.5rem 0.75rem;
        font-size: 1rem;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 4px;
        border: 1px solid #ced4da;
    }
    
    /* Success message styling */
    .stSuccess {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 4px;
        padding: 0.75rem;
        color: #155724;
        margin: 1rem 0;
    }
    
    /* Info message styling */
    .stInfo {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 4px;
        padding: 0.75rem;
        color: #0c5460;
        margin: 1rem 0;
    }
    
    /* Background */
    .main .block-container {
        background: #ffffff;
        padding: 1rem;
    }
    
    /* Chart containers */
    .chart-container {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Remove extra spacing */
    .stMarkdown {
        margin-bottom: 0;
    }
    
    /* Compact layout */
    .element-container {
        margin-bottom: 0.5rem;
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
    # Clean Header
    st.markdown('<h1 class="main-header">Productivity Calculator</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Calculator Type")
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
        st.markdown("### Features")
        st.markdown("• Interactive calculations")
        st.markdown("• Visual charts & graphs")
        st.markdown("• Historical tracking")
        st.markdown("• Export results")
        st.markdown("• Real-time analytics")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This calculator helps you measure various types of productivity metrics and optimize your operations with clear visualizations.")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f'<h2 class="section-header">{calc_type}</h2>', unsafe_allow_html=True)
        
        # Input section based on calculation type
        if calc_type == "Total Productivity":
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            output = st.number_input("Total Output", min_value=0.0, value=1000.0, step=0.000001, format="%.6f")
            total_input = st.number_input("Total Input", min_value=0.0, value=800.0, step=0.000001, format="%.6f")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Calculate Total Productivity", key="calc_total"):
                result = total_productivity(output, total_input)
                st.markdown(f'<div class="metric-card"><h3>Total Productivity</h3><h2>{result:.8f}</h2></div>', unsafe_allow_html=True)
                
                # Visualization
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig = go.Figure()
                fig.add_trace(go.Indicator(
                    mode="gauge+number+delta",
                    value=result,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Productivity Value", 'font': {'size': 20}},
                    delta={'reference': 1.0},
                    gauge={
                        'axis': {'range': [None, 2.0], 'tickwidth': 1, 'tickcolor': "#2c3e50"},
                        'bar': {'color': "#007bff"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "#2c3e50",
                        'steps': [
                            {'range': [0, 0.5], 'color': "#dc3545"},
                            {'range': [0.5, 1.0], 'color': "#ffc107"},
                            {'range': [1.0, 2.0], 'color': "#28a745"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 1.0
                        }
                    }
                ))
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#2c3e50'}
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Labour Productivity":
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            output = st.number_input("Total Output", min_value=0.0, value=1000.0, step=100.0)
            labour = st.number_input("Labour Input", min_value=0.0, value=200.0, step=50.0)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Calculate Labour Productivity", key="calc_labour"):
                result = labour_productivity(output, labour)
                st.markdown(f'<div class="metric-card"><h3>Labour Productivity</h3><h2>{result:.8f}</h2></div>', unsafe_allow_html=True)
                
                # Bar chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                data = pd.DataFrame({
                    'Metric': ['Output', 'Labour Input'],
                    'Value': [output, labour]
                })
                fig = px.bar(data, x='Metric', y='Value', 
                            title="Output vs Labour Input",
                            color='Metric',
                            color_discrete_map={'Output': '#007bff', 'Labour Input': '#6c757d'})
                fig.update_layout(
                    title_font_size=18,
                    title_font_color='#2c3e50',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#2c3e50'}
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Material Productivity":
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            output = st.number_input("Total Output", min_value=0.0, value=1000.0, step=100.0)
            material = st.number_input("Material Input", min_value=0.0, value=300.0, step=50.0)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Calculate Material Productivity", key="calc_material"):
                result = material_productivity(output, material)
                st.markdown(f'<div class="metric-card"><h3>Material Productivity</h3><h2>{result:.8f}</h2></div>', unsafe_allow_html=True)
                
                # Pie chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig = go.Figure(data=[go.Pie(
                    labels=['Output', 'Material Input'], 
                    values=[output, material],
                    hole=0.4,
                    marker_colors=['#007bff', '#6c757d'],
                    textinfo='label+percent',
                    textfont_size=14
                )])
                fig.update_layout(
                    title="Output vs Material Input Distribution",
                    title_font_size=18,
                    title_font_color='#2c3e50',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Capital Productivity":
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            output = st.number_input("Total Output", min_value=0.0, value=1000.0, step=100.0)
            capital = st.number_input("Capital Input", min_value=0.0, value=250.0, step=50.0)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Calculate Capital Productivity", key="calc_capital"):
                result = capital_productivity(output, capital)
                st.markdown(f'<div class="metric-card"><h3>Capital Productivity</h3><h2>{result:.8f}</h2></div>', unsafe_allow_html=True)
                
                # Line chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=['Capital Input', 'Output'], 
                    y=[capital, output], 
                    mode='lines+markers', 
                    name='Productivity Flow',
                    line=dict(color='#007bff', width=3),
                    marker=dict(size=10, color='#6c757d')
                ))
                fig.update_layout(
                    title="Capital Input to Output Flow",
                    title_font_size=18,
                    title_font_color='#2c3e50',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#2c3e50'}
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Machine Productivity":
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            output = st.number_input("Total Output", min_value=0.0, value=1000.0, step=100.0)
            machine_input = st.number_input("Machine Input", min_value=0.0, value=150.0, step=25.0)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Calculate Machine Productivity", key="calc_machine"):
                result = machine_productivity(output, machine_input)
                st.markdown(f'<div class="metric-card"><h3>Machine Productivity</h3><h2>{result:.8f}</h2></div>', unsafe_allow_html=True)
                
                # Scatter plot
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig = px.scatter(
                    x=[machine_input], 
                    y=[output], 
                    title="Machine Input vs Output",
                    labels={'x': 'Machine Input', 'y': 'Output'},
                    color_discrete_sequence=['#007bff']
                )
                fig.add_trace(go.Scatter(
                    x=[0, machine_input*1.5], 
                    y=[0, output*1.5], 
                    mode='lines', 
                    name='Efficiency Line',
                    line=dict(color='#6c757d', width=2, dash='dash')
                ))
                fig.update_layout(
                    title_font_size=18,
                    title_font_color='#2c3e50',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#2c3e50'}
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Miscellaneous Productivity":
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            output = st.number_input("Total Output", min_value=0.0, value=1000.0, step=100.0)
            misc = st.number_input("Miscellaneous Input", min_value=0.0, value=100.0, step=25.0)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Calculate Miscellaneous Productivity", key="calc_misc"):
                result = miscellaneous_productivity(output, misc)
                st.markdown(f'<div class="metric-card"><h3>Miscellaneous Productivity</h3><h2>{result:.8f}</h2></div>', unsafe_allow_html=True)
                
                # Area chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=['Misc Input', 'Output'], 
                    y=[misc, output], 
                    fill='tonexty', 
                    name='Productivity Area',
                    fillcolor='rgba(0, 123, 255, 0.2)',
                    line=dict(color='#007bff', width=2)
                ))
                fig.update_layout(
                    title="Miscellaneous Input to Output",
                    title_font_size=18,
                    title_font_color='#2c3e50',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#2c3e50'}
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Multifactor Productivity":
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            output = st.number_input("Total Output", min_value=0.0, value=1000.0, step=100.0)
            human = st.number_input("Human Input", min_value=0.0, value=200.0, step=50.0)
            material = st.number_input("Material Input", min_value=0.0, value=300.0, step=50.0)
            capital = st.number_input("Capital Input", min_value=0.0, value=250.0, step=50.0)
            energy = st.number_input("Energy Input", min_value=0.0, value=150.0, step=50.0)
            misc = st.number_input("Miscellaneous Input", min_value=0.0, value=100.0, step=25.0)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Calculate Multifactor Productivity", key="calc_multifactor"):
                result = multifactor_productivity(output, human, material, capital, energy, misc)
                st.markdown(f'<div class="metric-card"><h3>Multifactor Productivity</h3><h2>{result:.8f}</h2></div>', unsafe_allow_html=True)
                
                # Stacked bar chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                factors = ['Human', 'Material', 'Capital', 'Energy', 'Misc']
                values = [human, material, capital, energy, misc]
                
                fig = go.Figure(data=[
                    go.Bar(
                        name='Input Factors', 
                        x=factors, 
                        y=values,
                        marker_color=['#007bff', '#6c757d', '#28a745', '#ffc107', '#dc3545']
                    )
                ])
                fig.update_layout(
                    title="Input Factors Breakdown",
                    title_font_size=18,
                    title_font_color='#2c3e50',
                    barmode='stack',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#2c3e50'}
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Total Factor Productivity":
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            net_output = st.number_input("Net Output", min_value=0.0, value=800.0, step=100.0)
            worker_input = st.number_input("Worker Input", min_value=0.0, value=200.0, step=50.0)
            machine_input = st.number_input("Machine Input", min_value=0.0, value=150.0, step=25.0)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Calculate Total Factor Productivity", key="calc_tfp"):
                result = total_factor_productivity(net_output, worker_input, machine_input)
                st.markdown(f'<div class="metric-card"><h3>Total Factor Productivity</h3><h2>{result:.8f}</h2></div>', unsafe_allow_html=True)
                
                # Donut chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig = go.Figure(data=[go.Pie(
                    labels=['Worker Input', 'Machine Input'], 
                    values=[worker_input, machine_input],
                    hole=0.6,
                    marker_colors=['#007bff', '#6c757d'],
                    textinfo='label+percent',
                    textfont_size=14
                )])
                fig.update_layout(
                    title="Input Distribution",
                    title_font_size=18,
                    title_font_color='#2c3e50',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif calc_type == "Economic Order Quantity (EOQ)":
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            demand = st.number_input("Annual Demand (D)", min_value=0.0, value=1000.0, step=100.0)
            ordering_cost = st.number_input("Ordering Cost per Order (S)", min_value=0.0, value=50.0, step=10.0)
            holding_cost = st.number_input("Holding Cost per Unit per Year (H)", min_value=0.0, value=2.0, step=0.5)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Calculate EOQ", key="calc_eoq"):
                result = calculate_eoq(demand, ordering_cost, holding_cost)
                st.markdown(f'<div class="metric-card"><h3>Economic Order Quantity</h3><h2>{result:.2f} units</h2></div>', unsafe_allow_html=True)
                
                # Cost analysis chart
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
                    line=dict(color='#007bff', width=2),
                    marker=dict(size=6, color='#6c757d')
                ))
                fig.add_vline(
                    x=result, 
                    line_dash="dash", 
                    line_color="red", 
                    annotation_text=f"EOQ = {result:.0f}",
                    annotation_font_size=14
                )
                fig.update_layout(
                    title="Total Cost vs Order Quantity", 
                    xaxis_title="Order Quantity", 
                    yaxis_title="Total Cost",
                    title_font_size=18,
                    title_font_color='#2c3e50',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#2c3e50'}
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Right sidebar
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.markdown("### Quick Stats")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample data for demonstration
        if 'calculation_history' not in st.session_state:
            st.session_state.calculation_history = []
        
        if st.button("Add Sample Data"):
            sample_data = {
                'timestamp': datetime.now(),
                'type': calc_type,
                'result': 0.85
            }
            st.session_state.calculation_history.append(sample_data)
            st.success("Sample data added successfully!")
        
        if st.session_state.calculation_history:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("#### Recent Calculations")
            for i, calc in enumerate(st.session_state.calculation_history[-5:]):
                st.write(f"**{calc['type']}**: {calc['result']:.8f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<div class="tips-section">', unsafe_allow_html=True)
        st.markdown("### Tips")
        if calc_type == "Total Productivity":
            st.info("Total productivity measures overall efficiency of all inputs combined.")
        elif calc_type == "Labour Productivity":
            st.info("Labour productivity indicates how efficiently human resources are utilized.")
        elif calc_type == "Material Productivity":
            st.info("Material productivity shows how effectively materials are converted to output.")
        elif calc_type == "EOQ":
            st.info("EOQ helps optimize inventory costs by balancing ordering and holding costs.")
        else:
            st.info("Use these metrics to identify areas for improvement and optimization.")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 