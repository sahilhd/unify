#!/usr/bin/env python3
"""
UniLLM Web Dashboard - Fixed Version
A simple web interface for the UniLLM marketplace with proper usage stats updates
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
import base64

# Configuration
API_BASE_URL = "http://localhost:8000"

# Available models by provider
MODELS = {
    "OpenAI": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
    "Anthropic": ["claude-3-sonnet", "claude-3-haiku", "claude-3-opus"],
    "Google": ["gemini-pro", "gemini-flash"],
    "Mistral": ["mistral-7b", "mixtral-8x7b"],
    "Cohere": ["command", "command-r"]
}

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
        # Try multiple persistence methods
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

def save_chat_history():
    """Save chat history to session storage"""
    try:
        st.session_state['_chat_history'] = st.session_state.chat_history
    except:
        pass

def load_chat_history():
    """Load chat history from session storage"""
    try:
        if '_chat_history' in st.session_state:
            st.session_state.chat_history = st.session_state['_chat_history']
    except:
        st.session_state.chat_history = []

def main():
    st.set_page_config(
        page_title="UniLLM Marketplace",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize session state
    init_session_state()
    
    # Load chat history
    load_chat_history()
    
    st.title("🤖 UniLLM Marketplace")
    st.markdown("Unified LLM API with multiple providers")
    
    # Sidebar for authentication
    with st.sidebar:
        st.header("🔐 Authentication")
        
        if st.session_state.api_key is None:
            # Login/Register form
            auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])
            
            with auth_tab1:
                st.subheader("Login")
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                
                if st.button("Login"):
                    if login_user(email, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Login failed. Check your credentials.")
            
            with auth_tab2:
                st.subheader("Register")
                reg_email = st.text_input("Email", key="reg_email")
                reg_password = st.text_input("Password", type="password", key="reg_password")
                
                if st.button("Register"):
                    if register_user(reg_email, reg_password):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed. Email might already exist.")
        else:
            # User is logged in
            st.success(f"Logged in as: {st.session_state.user_email}")
            
            # Show full API key in a copyable format
            st.subheader("🔑 Your API Key")
            st.info("Copy this API key to use in your applications:")
            
            # Create a text input that shows the full API key and allows copying
            api_key_display = st.text_input(
                "API Key (click to copy):",
                value=st.session_state.api_key,
                type="default",
                disabled=True,
                help="Click on the text field to select all, then copy (Cmd+C / Ctrl+C)"
            )
            
            # Alternative: Show API key in a code block for easy copying
            st.code(st.session_state.api_key, language="text")
            
            if st.button("Logout"):
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
            st.header("💬 Chat Interface")
            
            # Model selection
            provider = st.selectbox("Select Provider", list(MODELS.keys()))
            model = st.selectbox("Select Model", MODELS[provider])
            
            # Chat interface
            user_message = st.text_area("Your message:", height=100)
            
            col3, col4 = st.columns([1, 1])
            with col3:
                temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
            with col4:
                max_tokens = st.slider("Max Tokens", 10, 4000, 1000, 10)
            
            if st.button("Send Message", type="primary"):
                if user_message.strip():
                    with st.spinner("Generating response..."):
                        response = send_chat_message(user_message, model, temperature, max_tokens)
                        if response:
                            st.success("Response received!")
                            st.text_area("AI Response:", response, height=200, disabled=True)
                            
                            # Add to chat history
                            st.session_state.chat_history.append({
                                'user': user_message,
                                'ai': response,
                                'model': model,
                                'timestamp': datetime.now().strftime("%H:%M:%S")
                            })
                            
                            # Save chat history
                            save_chat_history()
                            
                            # Force refresh of stats
                            st.session_state.force_refresh = True
                            st.session_state.usage_stats_cache = None
                            st.session_state.user_info_cache = None
                            st.session_state.last_chat_time = time.time()
                            
                            # Show updated stats immediately
                            st.rerun()
                        else:
                            st.error("Failed to get response. Check your credits or API key.")
                else:
                    st.warning("Please enter a message.")
            
            # Show chat history
            if st.session_state.chat_history:
                st.subheader("📝 Chat History")
                for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5 chats
                    with st.expander(f"Chat {len(st.session_state.chat_history) - i} - {chat['model']} ({chat['timestamp']})"):
                        st.write("**You:**")
                        st.write(chat['user'])
                        st.write("**AI:**")
                        st.write(chat['ai'])
        
        with col2:
            st.header("📊 Usage Stats")
            
            # Get usage stats (with forced refresh after chat)
            usage_stats = get_usage_stats()
            if usage_stats:
                st.metric("Total Requests", usage_stats.get('total_requests', 0))
                st.metric("Total Cost", f"${usage_stats.get('total_cost', 0):.4f}")
                st.metric("Requests Today", usage_stats.get('requests_today', 0))
                st.metric("Cost Today", f"${usage_stats.get('cost_today', 0):.4f}")
                
                # Add refresh button
                if st.button("🔄 Refresh Stats"):
                    st.session_state.usage_stats_cache = None
                    st.session_state.user_info_cache = None
                    st.session_state.force_refresh = True
                    st.rerun()
            else:
                st.error("Failed to load usage stats")
            
            st.header("💰 Credits")
            
            # Get user info (with forced refresh after chat)
            user_info = get_user_info()
            if user_info:
                st.metric("Available Credits", f"${user_info.get('credits', 0):.2f}")
                
                # Purchase credits
                st.subheader("Purchase Credits")
                amount = st.number_input("Amount ($)", min_value=1.0, value=10.0, step=1.0)
                if st.button("Purchase Credits"):
                    if purchase_credits(amount):
                        st.success(f"Successfully purchased ${amount} in credits!")
                        # Clear cache to refresh user info
                        st.session_state.user_info_cache = None
                        st.rerun()
                    else:
                        st.error("Failed to purchase credits")
            else:
                st.error("Failed to load user info")
        
        # Model information
        st.header("📋 Available Models")
        
        for provider_name, models_list in MODELS.items():
            with st.expander(f"{provider_name} Models"):
                for model_name in models_list:
                    st.write(f"• **{model_name}**")
                    # Add model descriptions here if available
    
    else:
        # Welcome screen for non-authenticated users
        st.markdown("""
        ## Welcome to UniLLM Marketplace! 🚀
        
        UniLLM provides a unified interface to multiple LLM providers with a single API key.
        
        ### Features:
        - 🤖 **Multiple Providers**: OpenAI, Anthropic, Google, Mistral, Cohere
        - 💳 **Credit-based Billing**: Pay only for what you use
        - 📊 **Usage Analytics**: Track your requests and costs
        - 🔄 **Provider Switching**: Seamlessly switch between models
        - 🛡️ **Rate Limiting**: Built-in protection against abuse
        
        ### Getting Started:
        1. Register an account using the sidebar
        2. Get your unique API key
        3. Start chatting with any available model!
        
        ### Supported Models:
        """)
        
        for provider, models in MODELS.items():
            st.markdown(f"**{provider}**: {', '.join(models)}")

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