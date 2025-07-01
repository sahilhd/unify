#!/usr/bin/env python3
"""
UniLLM Web Dashboard - Enhanced UI Version
A modern, professional web interface for the UniLLM marketplace
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
import base64
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Configuration
API_BASE_URL = "http://localhost:8000"

# Available models by provider with descriptions
MODELS = {
    "OpenAI": {
        "gpt-3.5-turbo": {"description": "Fast and efficient for most tasks", "cost": "$0.0024/1K tokens"},
        "gpt-4": {"description": "Most capable model for complex reasoning", "cost": "$0.036/1K tokens"},
        "gpt-4-turbo": {"description": "Latest GPT-4 with improved performance", "cost": "$0.01/1K tokens"}
    },
    "Anthropic": {
        "claude-3-sonnet": {"description": "Balanced performance and speed", "cost": "$0.018/1K tokens"},
        "claude-3-haiku": {"description": "Fastest and most cost-effective", "cost": "$0.0008/1K tokens"},
        "claude-3-opus": {"description": "Most capable Claude model", "cost": "$0.15/1K tokens"}
    },
    "Google": {
        "gemini-pro": {"description": "Google's most capable model", "cost": "$0.0012/1K tokens"},
        "gemini-flash": {"description": "Fast and efficient Gemini model", "cost": "$0.0006/1K tokens"}
    },
    "Mistral": {
        "mistral-7b": {"description": "Open source model with good performance", "cost": "$0.0007/1K tokens"},
        "mixtral-8x7b": {"description": "High-performance open source model", "cost": "$0.0014/1K tokens"}
    },
    "Cohere": {
        "command": {"description": "Cohere's flagship model", "cost": "$0.015/1K tokens"},
        "command-r": {"description": "Latest Command model with RAG capabilities", "cost": "$0.015/1K tokens"}
    }
}

# Custom CSS for enhanced styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Main styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Header styling */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

def encode_api_key(api_key):
    """Encode API key for URL storage"""
    return base64.b64encode(api_key.encode()).decode()

def decode_api_key(encoded_key):
    """Decode API key from URL storage"""
    try:
        return base64.b64decode(encoded_key.encode()).decode()
    except:
        return None

def init_session_state():
    """Initialize session state with multiple persistence methods"""
    if 'api_key' not in st.session_state:
        api_key = None
        
        # Method 1: Try URL parameters (base64 encoded)
        try:
            encoded_key = st.query_params.get('key', None)
            if encoded_key:
                api_key = decode_api_key(encoded_key)
        except:
            pass
        
        # Method 2: Try session storage
        if not api_key:
            try:
                api_key = st.session_state.get('_api_key', None)
            except:
                pass
        
        st.session_state.api_key = api_key
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    
    if 'last_chat_time' not in st.session_state:
        st.session_state.last_chat_time = None
    
    if 'usage_stats_cache' not in st.session_state:
        st.session_state.usage_stats_cache = None
    
    if 'user_info_cache' not in st.session_state:
        st.session_state.user_info_cache = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'force_refresh' not in st.session_state:
        st.session_state.force_refresh = False

def save_api_key(api_key):
    """Save API key using multiple persistence methods"""
    # Method 1: URL parameters (base64 encoded)
    try:
        encoded_key = encode_api_key(api_key)
        st.query_params["key"] = encoded_key
    except:
        pass
    
    # Method 2: Session storage
    try:
        st.session_state['_api_key'] = api_key
    except:
        pass

def clear_api_key():
    """Clear API key from all storage methods"""
    try:
        if "key" in st.query_params:
            del st.query_params["key"]
    except:
        pass
    
    try:
        if '_api_key' in st.session_state:
            del st.session_state['_api_key']
    except:
        pass

def create_usage_charts(usage_stats):
    """Create beautiful usage charts"""
    if not usage_stats:
        return None, None
    
    # Daily usage chart
    daily_data = {
        'Requests': usage_stats.get('requests_today', 0),
        'Tokens': usage_stats.get('tokens_today', 0),
        'Cost': usage_stats.get('cost_today', 0)
    }
    
    fig_daily = go.Figure(data=[
        go.Bar(
            x=list(daily_data.keys()),
            y=list(daily_data.values()),
            marker_color=['#667eea', '#764ba2', '#f093fb'],
            text=[f"{v:.2f}" if isinstance(v, float) else str(v) for v in daily_data.values()],
            textposition='auto',
        )
    ])
    
    fig_daily.update_layout(
        title="Today's Usage",
        template="plotly_white",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )
    
    # Total usage pie chart
    total_requests = usage_stats.get('total_requests', 0)
    total_cost = usage_stats.get('total_cost', 0)
    
    fig_total = go.Figure(data=[
        go.Pie(
            labels=['Total Requests', 'Total Cost ($)'],
            values=[total_requests, total_cost * 1000],  # Scale cost for visibility
            marker_colors=['#667eea', '#f093fb'],
            textinfo='label+percent',
            hole=0.4
        )
    ])
    
    fig_total.update_layout(
        title="Overall Usage",
        template="plotly_white",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )
    
    return fig_daily, fig_total

def main():
    st.set_page_config(
        page_title="UniLLM Marketplace",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Main header
    st.markdown("""
    <div class="main-header fade-in">
        <h1 style="text-align: center; color: #333; margin-bottom: 10px;">
            🤖 UniLLM Marketplace
        </h1>
        <p style="text-align: center; color: #666; font-size: 18px; margin: 0;">
            Unified LLM API with Multiple Providers
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for authentication
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h3 style="color: white; margin-bottom: 5px;">🔐 Authentication</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.api_key is None:
            # Login/Register form
            auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])
            
            with auth_tab1:
                st.markdown("### Login")
                email = st.text_input("Email", key="login_email", placeholder="Enter your email")
                password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
                
                if st.button("Login", key="login_btn"):
                    if login_user(email, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Login failed. Check your credentials.")
            
            with auth_tab2:
                st.markdown("### Register")
                reg_email = st.text_input("Email", key="reg_email", placeholder="Enter your email")
                reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="Choose a password")
                
                if st.button("Register", key="reg_btn"):
                    if register_user(reg_email, reg_password):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed. Email might already exist.")
        else:
            # User is logged in
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #333; margin-bottom: 10px;">👤 {st.session_state.user_email}</h4>
                <p style="color: #666; font-size: 14px;">Logged in successfully</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show API key
            st.markdown("### 🔑 Your API Key")
            api_key_display = st.text_input(
                "API Key (click to copy):",
                value=st.session_state.api_key,
                type="default",
                disabled=True,
                help="Click on the text field to select all, then copy (Cmd+C / Ctrl+C)"
            )
            
            # Alternative: Show API key in a code block
            st.code(st.session_state.api_key, language="text")
            
            if st.button("Logout", key="logout_btn"):
                st.session_state.api_key = None
                st.session_state.user_email = None
                st.session_state.usage_stats_cache = None
                st.session_state.user_info_cache = None
                st.session_state.chat_history = []
                clear_api_key()
                st.rerun()
    
    # Main content
    if st.session_state.api_key is not None:
        # User dashboard
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Chat interface
            st.markdown("""
            <div class="chat-container">
                <h3 style="color: #333; margin-bottom: 20px;">💬 Chat with AI</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Model selection
            model_col1, model_col2 = st.columns([1, 1])
            
            with model_col1:
                provider = st.selectbox(
                    "Select Provider",
                    list(MODELS.keys()),
                    key="provider_select"
                )
            
            with model_col2:
                models_list = list(MODELS[provider].keys())
                model = st.selectbox(
                    "Select Model",
                    models_list,
                    key="model_select"
                )
            
            # Show model info
            if provider and model:
                model_info = MODELS[provider][model]
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #333; margin-bottom: 10px;">📋 {model}</h4>
                    <p style="color: #666; margin-bottom: 5px;">{model_info['description']}</p>
                    <p style="color: #667eea; font-weight: 600;">{model_info['cost']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Chat parameters
            param_col1, param_col2 = st.columns(2)
            with param_col1:
                temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1, key="temp_slider")
            with param_col2:
                max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100, key="tokens_slider")
            
            # Chat input
            user_message = st.text_area(
                "Your message:",
                placeholder="Type your message here...",
                height=100,
                key="chat_input"
            )
            
            # Send button
            if st.button("Send Message", key="send_btn", use_container_width=True):
                if user_message.strip():
                    with st.spinner("🤖 AI is thinking..."):
                        response = send_chat_message(user_message, model, temperature, max_tokens)
                        if response:
                            # Add to chat history
                            st.session_state.chat_history.append({
                                "role": "user",
                                "content": user_message,
                                "timestamp": datetime.now()
                            })
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": response,
                                "timestamp": datetime.now()
                            })
                            st.session_state.last_chat_time = time.time()
                            st.session_state.force_refresh = True
                            st.rerun()
                        else:
                            st.error("Failed to get response. Please try again.")
                else:
                    st.warning("Please enter a message.")
            
            # Chat history display
            if st.session_state.chat_history:
                st.markdown("### 💬 Chat History")
                chat_container = st.container()
                
                with chat_container:
                    for i, message in enumerate(st.session_state.chat_history):
                        if message["role"] == "user":
                            st.markdown(f"""
                            <div class="user-message">
                                <strong>You:</strong><br>
                                {message["content"]}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="assistant-message">
                                <strong>AI:</strong><br>
                                {message["content"]}
                            </div>
                            """, unsafe_allow_html=True)
        
        with col2:
            # Usage statistics
            st.markdown("### 📊 Usage Statistics")
            
            usage_stats = get_usage_stats()
            if usage_stats:
                # Create charts
                fig_daily, fig_total = create_usage_charts(usage_stats)
                
                # Display charts
                if fig_daily:
                    st.plotly_chart(fig_daily, use_container_width=True)
                if fig_total:
                    st.plotly_chart(fig_total, use_container_width=True)
                
                # Manual refresh button
                if st.button("🔄 Refresh Stats", key="refresh_stats"):
                    st.session_state.usage_stats_cache = None
                    st.rerun()
            
            # User info and credits
            user_info = get_user_info()
            if user_info:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #333; margin-bottom: 10px;">💰 Available Credits</h4>
                    <h2 style="color: #667eea; margin: 0;">${user_info.get('credits', 0):.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Purchase credits
                st.markdown("### 💳 Purchase Credits")
                amount = st.number_input("Amount ($)", min_value=1.0, value=10.0, step=1.0, key="credit_amount")
                if st.button("Purchase Credits", key="purchase_btn", use_container_width=True):
                    if purchase_credits(amount):
                        st.success(f"Successfully purchased ${amount} in credits!")
                        st.session_state.user_info_cache = None
                        st.rerun()
                    else:
                        st.error("Failed to purchase credits")
            else:
                st.error("Failed to load user info")
        
        # Model information section
        st.markdown("### 📋 Available Models")
        
        for provider_name, models_dict in MODELS.items():
            with st.expander(f"🤖 {provider_name} Models"):
                for model_name, model_info in models_dict.items():
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.8); padding: 15px; border-radius: 10px; margin: 10px 0;">
                        <h4 style="color: #333; margin-bottom: 5px;">{model_name}</h4>
                        <p style="color: #666; margin-bottom: 5px;">{model_info['description']}</p>
                        <p style="color: #667eea; font-weight: 600; margin: 0;">{model_info['cost']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    else:
        # Welcome screen for non-authenticated users
        st.markdown("""
        <div class="main-header fade-in">
            <h2 style="text-align: center; color: #333; margin-bottom: 20px;">
                🚀 Welcome to UniLLM Marketplace!
            </h2>
            <p style="text-align: center; color: #666; font-size: 18px; line-height: 1.6;">
                UniLLM provides a unified interface to multiple LLM providers with a single API key.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4 style="color: #333;">🤖 Multiple Providers</h4>
                <p style="color: #666;">OpenAI, Anthropic, Google, Mistral, Cohere</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
                <h4 style="color: #333;">💳 Credit-based Billing</h4>
                <p style="color: #666;">Pay only for what you use</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4 style="color: #333;">📊 Usage Analytics</h4>
                <p style="color: #666;">Track your requests and costs</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
                <h4 style="color: #333;">🛡️ Rate Limiting</h4>
                <p style="color: #666;">Built-in protection against abuse</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Getting Started")
        st.markdown("""
        1. **Register an account** using the sidebar
        2. **Get your unique API key**
        3. **Start chatting** with any available model!
        """)
        
        st.markdown("### 🤖 Supported Models")
        for provider, models in MODELS.items():
            st.markdown(f"**{provider}**: {', '.join(models.keys())}")

def login_user(email, password):
    """Login user and store API key"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            api_key = data['user']['api_key']
            st.session_state.api_key = api_key
            st.session_state.user_email = email
            save_api_key(api_key)
            return True
        return False
    except Exception as e:
        st.error(f"Login error: {e}")
        return False

def register_user(email, password):
    """Register new user"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        st.error(f"Registration error: {e}")
        return False

def send_chat_message(message, model, temperature, max_tokens):
    """Send chat message to API"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
        data = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            f"{API_BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', 'No response received')
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Chat error: {e}")
        return None

def get_usage_stats():
    """Get user usage statistics with proper refresh logic"""
    try:
        # Always refresh if force_refresh is True
        if st.session_state.force_refresh:
            st.session_state.usage_stats_cache = None
            st.session_state.force_refresh = False
        
        # Check if we have cached stats and they're recent
        if (st.session_state.usage_stats_cache and 
            st.session_state.last_chat_time and 
            time.time() - st.session_state.last_chat_time < 2):  # Cache for only 2 seconds after chat
            return st.session_state.usage_stats_cache
        
        headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
        response = requests.get(
            f"{API_BASE_URL}/billing/usage",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            stats = response.json()
            st.session_state.usage_stats_cache = stats
            return stats
        return None
    except Exception as e:
        st.error(f"Usage stats error: {e}")
        return None

def get_user_info():
    """Get current user information with proper refresh logic"""
    try:
        # Always refresh if force_refresh is True
        if st.session_state.force_refresh:
            st.session_state.user_info_cache = None
        
        # Check if we have cached user info and it's recent
        if (st.session_state.user_info_cache and 
            st.session_state.last_chat_time and 
            time.time() - st.session_state.last_chat_time < 2):  # Cache for only 2 seconds after chat
            return st.session_state.user_info_cache
        
        headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
        response = requests.get(
            f"{API_BASE_URL}/auth/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            st.session_state.user_info_cache = user_info
            return user_info
        return None
    except Exception as e:
        st.error(f"User info error: {e}")
        return None

def purchase_credits(amount):
    """Purchase credits"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
        data = {"amount": amount, "payment_method": "dashboard"}
        
        response = requests.post(
            f"{API_BASE_URL}/billing/purchase-credits",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        st.error(f"Purchase error: {e}")
        return False

if __name__ == "__main__":
    main() 