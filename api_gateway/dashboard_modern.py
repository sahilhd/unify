#!/usr/bin/env python3
"""
UniLLM Modern Dashboard (Anthropic/OpenAI-inspired)
Dark theme, sidebar navigation, sectioned layout, modern UI
"""

import streamlit as st
import requests
import time
import base64
from datetime import datetime
import plotly.graph_objects as go

API_BASE_URL = "http://localhost:8000"

# --- Custom CSS for dark mode and modern look ---
def load_modern_css():
    st.markdown("""
    <style>
    body, .main, .stApp {
        background: #18181b !important;
        color: #f3f4f6 !important;
    }
    .stApp {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .sidebar .sidebar-content {
        background: #23232a !important;
        color: #f3f4f6 !important;
    }
    .css-1d391kg, .css-1lcbmhc, .css-1v0mbdj {
        background: #23232a !important;
    }
    .st-bb, .st-c6, .st-cg {
        background: #23232a !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #7f5af0 0%, #2cb67d 100%);
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.5em;
        font-weight: 600;
        font-size: 1em;
        margin: 0.5em 0;
        transition: 0.2s;
    }
    .stButton > button:hover {
        filter: brightness(1.1);
        box-shadow: 0 2px 8px #7f5af055;
    }
    .stTextInput > div > div > input, .stTextArea > div > textarea {
        background: #23232a !important;
        color: #f3f4f6 !important;
        border-radius: 8px;
        border: 1.5px solid #393953;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > textarea:focus {
        border: 1.5px solid #7f5af0;
        outline: none;
    }
    .stSelectbox > div > div > div {
        background: #23232a !important;
        color: #f3f4f6 !important;
        border-radius: 8px;
        border: 1.5px solid #393953;
    }
    .stMetric {
        background: #23232a !important;
        border-radius: 10px;
        padding: 1em;
        margin-bottom: 1em;
        box-shadow: 0 2px 8px #7f5af022;
    }
    .stDataFrame, .stTable {
        background: #23232a !important;
        color: #f3f4f6 !important;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #23232a !important;
        color: #f3f4f6 !important;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #18181b !important;
        color: #7f5af0 !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #fff !important;
    }
    .stMarkdown p, .stMarkdown li {
        color: #e5e7eb !important;
    }
    .stExpanderHeader {
        color: #fff !important;
    }
    .stCodeBlock {
        background: #23232a !important;
        color: #f3f4f6 !important;
        border-radius: 8px;
    }
    #MainMenu, header, footer {visibility: hidden;}
    .copy-btn {
        background: #393953;
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 0.3em 1em;
        font-size: 0.95em;
        margin-left: 0.5em;
        cursor: pointer;
        transition: 0.2s;
    }
    .copy-btn:hover {
        background: #7f5af0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Navigation ---
SECTIONS = [
    ("Analytics", "📊"),
    ("Chat", "💬"),
    ("API Keys", "🔑"),
    ("Billing", "💳"),
    ("Settings", "⚙️")
]

MODELS = {
    "OpenAI": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
    "Anthropic": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
    "Google": ["gemini-pro", "gemini-pro-vision"],
    "Mistral": ["mistral-large", "mistral-medium", "mistral-small"],
    "Cohere": ["command", "command-light"]
}

# --- API helpers ---
def login_user(email, password):
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
            return True
        return False
    except Exception as e:
        st.error(f"Login error: {e}")
        return False

def register_user(email, password):
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={"email": email, "password": password},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Registration error: {e}")
        return False

def send_chat_message(messages, model, temperature, max_tokens):
    try:
        headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
        data = {
            "model": model,
            "messages": messages,
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
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Chat error: {e}")
        return None

def get_usage_stats():
    try:
        headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
        response = requests.get(
            f"{API_BASE_URL}/billing/usage",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Usage stats error: {e}")
        return None

def get_user_info():
    try:
        headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
        response = requests.get(
            f"{API_BASE_URL}/auth/me",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"User info error: {e}")
        return None

def purchase_credits(amount):
    try:
        headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
        data = {"amount": amount, "payment_method": "dashboard"}
        response = requests.post(
            f"{API_BASE_URL}/billing/purchase-credits",
            headers=headers,
            json=data,
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Purchase error: {e}")
        return False

# --- Sidebar ---
def sidebar_nav():
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/OpenAI_Logo.svg", width=120)
    st.sidebar.markdown("<h2 style='color:#fff;'>UniLLM</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='border:1px solid #393953;'>", unsafe_allow_html=True)
    section = st.sidebar.radio(
        "Navigation",
        [f"{icon} {name}" for name, icon in SECTIONS],
        index=0,
        key="sidebar_section"
    )
    st.sidebar.markdown("<hr style='border:1px solid #393953;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<small style='color:#888;'>Inspired by Anthropic & OpenAI</small>", unsafe_allow_html=True)
    return section.split(" ", 1)[1]

# --- Section: Analytics ---
def section_analytics():
    st.markdown("## 📊 Analytics")
    st.markdown("View your usage statistics and trends.")
    usage_stats = get_usage_stats()
    if usage_stats:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Requests", usage_stats.get("total_requests", 0))
        col2.metric("Total Tokens", usage_stats.get("total_tokens", 0))
        col3.metric("Total Cost ($)", f"${usage_stats.get('total_cost', 0):.4f}")
        # Daily chart
        fig = go.Figure(data=[
            go.Bar(
                x=["Requests Today", "Tokens Today", "Cost Today ($)"],
                y=[usage_stats.get("requests_today", 0), usage_stats.get("tokens_today", 0), usage_stats.get("cost_today", 0)],
                marker_color=["#7f5af0", "#2cb67d", "#f3f4f6"]
            )
        ])
        fig.update_layout(
            plot_bgcolor="#23232a",
            paper_bgcolor="#23232a",
            font_color="#f3f4f6",
            title="Today's Usage"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("### 📅 Usage Over Time (Coming Soon)")
        st.info("Advanced analytics and export coming soon.")
    else:
        st.info("No usage data available.")

# --- Section: Chat ---
def section_chat():
    st.markdown("## 💬 Chat")
    st.markdown("Chat with any available model.")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "gpt-3.5-turbo"
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""
    # Model selection
    provider = st.selectbox("Provider", list(MODELS.keys()), key="provider_select")
    model = st.selectbox("Model", MODELS[provider], key="model_select")
    st.session_state.selected_model = model
    # Chat history
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        align = "flex-end" if role == "user" else "flex-start"
        bubble_color = "#7f5af0" if role == "user" else "#23232a"
        text_color = "#fff" if role == "user" else "#f3f4f6"
        st.markdown(f"""
        <div style='display: flex; justify-content: {align}; margin-bottom: 8px;'>
            <div style='background: {bubble_color}; color: {text_color}; border-radius: 12px; padding: 10px 18px; max-width: 70%; box-shadow: 0 2px 8px #7f5af022;'>
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    # Chat input
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area("Your message", value=st.session_state.chat_input, key="chat_input_area")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.01)
        max_tokens = st.slider("Max Tokens", 16, 2048, 256, 8)
        submitted = st.form_submit_button("Send", use_container_width=True)
        if submitted and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            messages = st.session_state.chat_history[-10:]  # last 10 messages
            response = send_chat_message(messages, model, temperature, max_tokens)
            if response and response.get("response"):
                st.session_state.chat_history.append({"role": "assistant", "content": response["response"]})
            elif response and response.get("error"):
                st.error(response["error"])
            else:
                st.error("No response from model.")

# --- Section: API Keys ---
def section_api_keys():
    st.markdown("## 🔑 API Keys")
    st.markdown("View and manage your API keys.")
    user_info = get_user_info()
    if user_info:
        api_key = user_info.get("api_key", "N/A")
        st.code(api_key, language="text")
        if st.button("Copy API Key"):
            st.write("<script>navigator.clipboard.writeText('" + api_key + "');</script>", unsafe_allow_html=True)
            st.success("API Key copied to clipboard!")
        st.markdown(f"**Email:** {user_info.get('email', 'N/A')}")
        st.markdown(f"**Created:** {user_info.get('created_at', 'N/A')}")
        st.markdown(f"**Last Used:** {user_info.get('last_used', 'N/A')}")
    else:
        st.info("No API key found.")

# --- Section: Billing ---
def section_billing():
    st.markdown("## 💳 Billing")
    st.markdown("View credits and purchase history.")
    user_info = get_user_info()
    if user_info:
        st.metric("Available Credits", f"${user_info.get('credits', 0):.2f}")
        amount = st.number_input("Amount ($)", min_value=1.0, value=10.0, step=1.0)
        if st.button("Purchase Credits"):
            if purchase_credits(amount):
                st.success(f"Successfully purchased ${amount} in credits!")
            else:
                st.error("Failed to purchase credits")
        st.markdown("### 🧾 Billing History (Coming Soon)")
        st.info("Detailed billing history and invoices coming soon.")
    else:
        st.info("No billing info available.")

# --- Section: Settings ---
def section_settings():
    st.markdown("## ⚙️ Settings")
    st.markdown("Configure your account and preferences.")
    st.info("Settings UI coming soon. Account management and preferences will be available here.")

# --- Main App ---
def main():
    st.set_page_config(page_title="UniLLM Modern Dashboard", page_icon="🤖", layout="wide")
    load_modern_css()
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if not st.session_state.api_key:
        st.title("🔐 Login to UniLLM Dashboard")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login = st.form_submit_button("Login")
            if login:
                if login_user(email, password):
                    st.success("Login successful! Reloading...")
                    st.rerun()
                else:
                    st.error("Login failed. Check your credentials.")
        st.markdown("---")
        st.markdown("Don't have an account? Register below:")
        with st.form("register_form"):
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            register = st.form_submit_button("Register")
            if register:
                if register_user(reg_email, reg_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Registration failed. Try a different email.")
        return
    section = sidebar_nav()
    if section == "Analytics":
        section_analytics()
    elif section == "Chat":
        section_chat()
    elif section == "API Keys":
        section_api_keys()
    elif section == "Billing":
        section_billing()
    elif section == "Settings":
        section_settings()

if __name__ == "__main__":
    main() 