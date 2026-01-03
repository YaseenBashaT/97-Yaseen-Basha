"""
UI Styling Module
Provides CSS styling functions for the Streamlit application.
"""

import streamlit as st


def apply_modern_styling():
    """Apply clean, minimalistic CSS styling to the application"""
    st.markdown("""
    <style>
    /* Import clean font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Global Styles with professional background */
    .main {
        font-family: 'Inter', sans-serif;
        padding: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Professional page background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Professional sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* Professional metric containers */
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Professional data frames */
    .stDataFrame {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Simple Header with professional colors */
    .modern-header {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        margin: 0 0 2rem 0;
        text-align: center;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: #2c3e50;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .header-subtitle {
        color: #5d6d7e;
        font-size: 1rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
    }
    
    /* Professional Input Section */
    .input-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Enhanced Professional Metrics */
    .enhanced-metric {
        background: linear-gradient(135deg, #ffffff 0%, #f1f3f4 100%);
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 1rem;
        text-align: center;
        display: inline-block;
        min-width: 120px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .enhanced-metric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .metric-icon {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        color: #3498db;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0.25rem 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #5d6d7e;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Professional Architecture Section */
    .architecture-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .architecture-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e9ecef;
    }
    
    .architecture-icon {
        font-size: 1.2rem;
        color: #3498db;
    }
    
    .architecture-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2c3e50 !important;
        margin: 0;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.4);
    }
    
    /* Professional Cards with classic color palette */
    .insight-card {
        background: linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%);
        border-left: 4px solid #3498db;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
        color: #2c3e50;
    }
    
    .insight-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .insight-warning {
        border-left-color: #e74c3c;
        background: linear-gradient(135deg, #fadbd8 0%, #f1948a 100%);
        color: #722f37;
    }
    
    .insight-success {
        border-left-color: #27ae60;
        background: linear-gradient(135deg, #d5f4e6 0%, #82e0aa 100%);
        color: #1e8449;
    }
    
    .insight-info {
        border-left-color: #3498db;
        background: linear-gradient(135deg, #d6eaf8 0%, #85c1e9 100%);
        color: #1f618d;
    }
    
    /* Professional input styling */
    .stTextInput > div > div > input {
        border: 2px solid #bdc3c7;
        border-radius: 6px;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    .stSelectbox > div > div > div {
        border: 2px solid #bdc3c7;
        border-radius: 6px;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div > div:focus-within {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    /* Typography - Professional color palette */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Professional heading hierarchy */
    .stApp h1, .stMarkdown h1 {
        color: #2c3e50;  /* Deep navy blue */
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .stApp h2, .stMarkdown h2 {
        color: #34495e;  /* Slate gray */
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        margin-bottom: 1rem;
    }
    
    .stApp h3, .stMarkdown h3 {
        color: #5d6d7e;  /* Cool gray */
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        margin-bottom: 0.8rem;
    }
    
    .stApp h4, .stMarkdown h4, .stApp h5, .stMarkdown h5, .stApp h6, .stMarkdown h6 {
        color: #34495e;  /* Darker gray instead of muted */
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        margin-bottom: 0.6rem;
    }
    
    /* Headings on dark/colored backgrounds */
    .insight-card h1, .insight-card h2, .insight-card h3, .insight-card h4, .insight-card h5, .insight-card h6,
    .architecture-section h1, .architecture-section h2, .architecture-section h3, .architecture-section h4, .architecture-section h5, .architecture-section h6 {
        color: #2c3e50 !important;  /* Force dark color for architecture sections */
    }
    
    /* Headings in gradient backgrounds */
    [style*="background: linear-gradient"] h1,
    [style*="background: linear-gradient"] h2,
    [style*="background: linear-gradient"] h3,
    [style*="background: linear-gradient"] h4,
    [style*="background: linear-gradient"] h5,
    [style*="background: linear-gradient"] h6 {
        color: #ffffff;
    }
    
    /* Alert headings inherit appropriate colors */
    .stAlert h1, .stAlert h2, .stAlert h3, .stAlert h4, .stAlert h5, .stAlert h6 {
        color: inherit;
    }
    
    p, div, span {
        font-family: 'Inter', sans-serif;
        color: #2c3e50;
    }
    
    /* Ensure proper text contrast everywhere */
    .stApp, .stApp p, .stApp div, .stApp span {
        color: #2c3e50;
    }
    
    /* Fix small text visibility */
    small, .small {
        color: #34495e !important;
        font-weight: 500;
    }
    
    /* Improve metric text contrast */
    .metric-value {
        color: #2c3e50 !important;
    }
    
    /* Fix chart annotations */
    .js-plotly-plot .annotation-text {
        color: #2c3e50 !important;
    }
    
    /* Ensure all text is visible */
    .stDataFrame table {
        color: #2c3e50 !important;
    }
    
    .stDataFrame th {
        background-color: #34495e !important;
        color: #ffffff !important;
        font-weight: 600;
    }
    
    .stDataFrame td {
        color: #2c3e50 !important;
    }
    
    /* Fix expander text */
    .streamlit-expanderHeader {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    
    /* Fix alert text contrast */
    .stAlert {
        border-radius: 6px;
    }
    
    .stSuccess {
        background-color: #d4edda !important;
        color: #155724 !important;
        border-color: #c3e6cb !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        color: #856404 !important;
        border-color: #ffeaa7 !important;
    }
    
    .stInfo {
        background-color: #d1ecf1 !important;
        color: #0c5460 !important;
        border-color: #bee5eb !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border-color: #f5c6cb !important;
    }
    </style>
    """, unsafe_allow_html=True)
