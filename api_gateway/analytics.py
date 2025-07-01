#!/usr/bin/env python3
"""
UniLLM Analytics System
Advanced analytics and reporting for the UniLLM marketplace
"""

import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit as st
import requests
from typing import Dict, List, Optional

class UniLLMAnalytics:
    def __init__(self, db_path: str = "unillm.db"):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_usage_data(self, days: int = 30) -> pd.DataFrame:
        """Get usage data for the last N days"""
        query = """
        SELECT 
            ul.user_id,
            u.email,
            ul.model,
            ul.provider,
            ul.tokens_used,
            ul.cost,
            ul.response_time_ms,
            ul.success,
            ul.error_message,
            ul.created_at,
            DATE(ul.created_at) as date
        FROM usage_log ul
        JOIN users u ON ul.user_id = u.id
        WHERE ul.created_at >= datetime('now', '-{} days')
        ORDER BY ul.created_at DESC
        """.format(days)
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def get_user_summary(self) -> pd.DataFrame:
        """Get user summary statistics"""
        query = """
        SELECT 
            u.email,
            COUNT(ul.id) as total_requests,
            SUM(ul.tokens_used) as total_tokens,
            SUM(ul.cost) as total_cost,
            AVG(ul.response_time_ms) as avg_response_time,
            SUM(CASE WHEN ul.success = 1 THEN 1 ELSE 0 END) as successful_requests,
            SUM(CASE WHEN ul.success = 0 THEN 1 ELSE 0 END) as failed_requests
        FROM users u
        LEFT JOIN usage_log ul ON u.id = ul.user_id
        GROUP BY u.id, u.email
        ORDER BY total_cost DESC
        """
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def get_provider_stats(self) -> pd.DataFrame:
        """Get provider performance statistics"""
        query = """
        SELECT 
            provider,
            COUNT(*) as total_requests,
            SUM(tokens_used) as total_tokens,
            SUM(cost) as total_cost,
            AVG(response_time_ms) as avg_response_time,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_requests,
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed_requests,
            (SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as success_rate
        FROM usage_log
        GROUP BY provider
        ORDER BY total_cost DESC
        """
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def get_model_stats(self) -> pd.DataFrame:
        """Get model usage statistics"""
        query = """
        SELECT 
            model,
            provider,
            COUNT(*) as total_requests,
            SUM(tokens_used) as total_tokens,
            SUM(cost) as total_cost,
            AVG(response_time_ms) as avg_response_time,
            AVG(cost / tokens_used) as cost_per_token
        FROM usage_log
        WHERE tokens_used > 0
        GROUP BY model, provider
        ORDER BY total_cost DESC
        """
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def get_daily_trends(self, days: int = 30) -> pd.DataFrame:
        """Get daily usage trends"""
        query = """
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as requests,
            SUM(tokens_used) as tokens,
            SUM(cost) as cost,
            COUNT(DISTINCT user_id) as active_users
        FROM usage_log
        WHERE created_at >= datetime('now', '-{} days')
        GROUP BY DATE(created_at)
        ORDER BY date
        """.format(days)
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)

def create_analytics_dashboard():
    """Create Streamlit analytics dashboard"""
    st.set_page_config(
        page_title="UniLLM Analytics",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 UniLLM Analytics Dashboard")
    st.markdown("Advanced analytics and reporting for the UniLLM marketplace")
    
    # Initialize analytics
    analytics = UniLLMAnalytics()
    
    # Sidebar filters
    st.sidebar.header("📅 Filters")
    days = st.sidebar.slider("Time Period (days)", 1, 90, 30)
    
    # Get data
    try:
        usage_data = analytics.get_usage_data(days)
        user_summary = analytics.get_user_summary()
        provider_stats = analytics.get_provider_stats()
        model_stats = analytics.get_model_stats()
        daily_trends = analytics.get_daily_trends(days)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_requests = usage_data['total_requests'].sum() if not usage_data.empty else 0
            st.metric("Total Requests", f"{total_requests:,}")
        
        with col2:
            total_cost = usage_data['cost'].sum() if not usage_data.empty else 0
            st.metric("Total Cost", f"${total_cost:.2f}")
        
        with col3:
            total_tokens = usage_data['tokens_used'].sum() if not usage_data.empty else 0
            st.metric("Total Tokens", f"{total_tokens:,}")
        
        with col4:
            active_users = len(usage_data['user_id'].unique()) if not usage_data.empty else 0
            st.metric("Active Users", active_users)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Daily Usage Trends")
            if not daily_trends.empty:
                fig = px.line(daily_trends, x='date', y=['requests', 'cost'], 
                            title="Daily Requests and Cost")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected period")
        
        with col2:
            st.subheader("💰 Provider Cost Distribution")
            if not provider_stats.empty:
                fig = px.pie(provider_stats, values='total_cost', names='provider',
                           title="Cost by Provider")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No provider data available")
        
        # Provider performance
        st.subheader("🏆 Provider Performance")
        if not provider_stats.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(provider_stats, x='provider', y='success_rate',
                           title="Success Rate by Provider (%)")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(provider_stats, x='provider', y='avg_response_time',
                           title="Average Response Time (ms)")
                st.plotly_chart(fig, use_container_width=True)
        
        # Model usage
        st.subheader("🤖 Model Usage Statistics")
        if not model_stats.empty:
            st.dataframe(
                model_stats.round(4),
                use_container_width=True,
                hide_index=True
            )
        
        # User summary
        st.subheader("👥 User Summary")
        if not user_summary.empty:
            st.dataframe(
                user_summary.round(4),
                use_container_width=True,
                hide_index=True
            )
        
        # Raw usage data
        with st.expander("📋 Raw Usage Data"):
            if not usage_data.empty:
                st.dataframe(usage_data, use_container_width=True)
            else:
                st.info("No usage data available")
    
    except Exception as e:
        st.error(f"Error loading analytics data: {e}")
        st.info("Make sure the UniLLM server is running and the database exists.")

def create_user_analytics_dashboard(api_key: str):
    """Create user-specific analytics dashboard"""
    st.set_page_config(
        page_title="My Analytics",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 My Usage Analytics")
    
    # Get user data from API
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Get usage stats
        response = requests.get("http://localhost:8000/billing/usage", headers=headers)
        if response.status_code == 200:
            usage_stats = response.json()
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Requests", usage_stats.get('total_requests', 0))
            
            with col2:
                st.metric("Total Cost", f"${usage_stats.get('total_cost', 0):.4f}")
            
            with col3:
                st.metric("Requests Today", usage_stats.get('requests_today', 0))
            
            with col4:
                st.metric("Cost Today", f"${usage_stats.get('cost_today', 0):.4f}")
            
            # Get billing history
            response = requests.get("http://localhost:8000/billing/history", headers=headers)
            if response.status_code == 200:
                billing_history = response.json()
                
                st.subheader("💰 Billing History")
                if billing_history:
                    df = pd.DataFrame(billing_history)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No billing history available")
        
        else:
            st.error("Failed to load usage data")
    
    except Exception as e:
        st.error(f"Error loading user analytics: {e}")

if __name__ == "__main__":
    create_analytics_dashboard() 