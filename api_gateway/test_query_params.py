#!/usr/bin/env python3
"""
Test script to verify st.query_params functionality
"""

import streamlit as st

def test_query_params():
    """Test the new st.query_params functionality"""
    st.title("🧪 Testing st.query_params")
    
    # Test getting query parameters
    st.subheader("Current Query Parameters")
    st.write("All query params:", dict(st.query_params))
    
    # Test setting a query parameter
    if st.button("Set test parameter"):
        st.query_params["test"] = "value123"
        st.rerun()
    
    # Test getting a specific parameter
    test_value = st.query_params.get("test", "Not set")
    st.write(f"Test parameter value: {test_value}")
    
    # Test deleting a parameter
    if st.button("Clear test parameter"):
        if "test" in st.query_params:
            del st.query_params["test"]
        st.rerun()
    
    # Test API key simulation
    st.subheader("API Key Persistence Test")
    
    # Get stored API key
    stored_key = st.query_params.get("api_key", None)
    st.write(f"Stored API key: {stored_key[:20] + '...' if stored_key else 'None'}")
    
    # Set a test API key
    if st.button("Set test API key"):
        st.query_params["api_key"] = "unillm_test_key_123456789"
        st.rerun()
    
    # Clear API key
    if st.button("Clear API key"):
        if "api_key" in st.query_params:
            del st.query_params["api_key"]
        st.rerun()
    
    st.subheader("Instructions")
    st.markdown("""
    1. Click 'Set test parameter' to add a query parameter
    2. Click 'Set test API key' to simulate API key storage
    3. Refresh the page to test persistence
    4. Use 'Clear' buttons to remove parameters
    
    The URL should update with the parameters, and they should persist across refreshes.
    """)

if __name__ == "__main__":
    test_query_params() 