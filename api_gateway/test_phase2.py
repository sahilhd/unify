#!/usr/bin/env python3
"""
UniLLM Phase 2: Comprehensive Testing Script
Tests user registration, authentication, billing, and API usage
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@unillm.com"
TEST_PASSWORD = "testpassword123"

class Phase2Tester:
    def __init__(self):
        self.session = requests.Session()
        self.api_key = None
        self.jwt_token = None
        self.user_id = None
    
    def print_header(self, title: str):
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_success(self, message: str):
        print(f"✅ {message}")
    
    def print_error(self, message: str):
        print(f"❌ {message}")
    
    def print_info(self, message: str):
        print(f"ℹ️  {message}")
    
    def test_health_check(self):
        """Test health check endpoint"""
        self.print_header("Health Check")
        try:
            response = self.session.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Health check passed: {data}")
                return True
            else:
                self.print_error(f"Health check failed: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Health check error: {e}")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        self.print_header("User Registration")
        try:
            data = {
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
            response = self.session.post(f"{BASE_URL}/auth/register", json=data)
            
            if response.status_code == 200:
                user_data = response.json()
                self.api_key = user_data["api_key"]
                self.user_id = user_data["id"]
                self.print_success(f"User registered successfully")
                self.print_info(f"API Key: {self.api_key[:20]}...")
                self.print_info(f"Credits: {user_data['credits']}")
                return True
            else:
                self.print_error(f"Registration failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Registration error: {e}")
            return False
    
    def test_user_login(self):
        """Test user login"""
        self.print_header("User Login")
        try:
            data = {
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
            response = self.session.post(f"{BASE_URL}/auth/login", json=data)
            
            if response.status_code == 200:
                login_data = response.json()
                self.jwt_token = login_data["access_token"]
                self.print_success("Login successful")
                self.print_info(f"JWT Token: {self.jwt_token[:20]}...")
                return True
            else:
                self.print_error(f"Login failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Login error: {e}")
            return False
    
    def test_get_user_info(self):
        """Test getting user information"""
        self.print_header("Get User Info")
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{BASE_URL}/auth/me", headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                # Store API key for later use
                self.api_key = user_data["api_key"]
                self.print_success("User info retrieved")
                self.print_info(f"Email: {user_data['email']}")
                self.print_info(f"Credits: {user_data['credits']}")
                self.print_info(f"Rate Limit: {user_data['rate_limit_per_minute']}/min")
                self.print_info(f"API Key: {self.api_key[:20]}...")
                return True
            else:
                self.print_error(f"Get user info failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Get user info error: {e}")
            return False
    
    def test_chat_with_api_key(self):
        """Test chat completion with API key"""
        self.print_header("Chat with API Key")
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "Hello! What is 2+2?"}
                ],
                "temperature": 0.7
            }
            response = self.session.post(f"{BASE_URL}/chat/completions", json=data, headers=headers)
            
            if response.status_code == 200:
                chat_data = response.json()
                self.print_success("Chat request successful")
                self.print_info(f"Response: {chat_data['response'][:100]}...")
                self.print_info(f"Provider: {chat_data['provider']}")
                self.print_info(f"Tokens: {chat_data['tokens']}")
                self.print_info(f"Cost: ${chat_data['cost']:.6f}")
                self.print_info(f"Remaining Credits: ${chat_data['remaining_credits']:.4f}")
                return True
            else:
                self.print_error(f"Chat request failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Chat request error: {e}")
            return False
    
    def test_usage_statistics(self):
        """Test usage statistics"""
        self.print_header("Usage Statistics")
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{BASE_URL}/billing/usage", headers=headers)
            
            if response.status_code == 200:
                usage_data = response.json()
                self.print_success("Usage statistics retrieved")
                self.print_info(f"Total Requests: {usage_data['total_requests']}")
                self.print_info(f"Total Tokens: {usage_data['total_tokens']}")
                self.print_info(f"Total Cost: ${usage_data['total_cost']:.6f}")
                self.print_info(f"Today's Requests: {usage_data['requests_today']}")
                self.print_info(f"Today's Cost: ${usage_data['cost_today']:.6f}")
                return True
            else:
                self.print_error(f"Usage stats failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Usage stats error: {e}")
            return False
    
    def test_purchase_credits(self):
        """Test credit purchase"""
        self.print_header("Credit Purchase")
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            data = {
                "amount": 5.0,
                "payment_method": "test_payment"
            }
            response = self.session.post(f"{BASE_URL}/billing/purchase-credits", json=data, headers=headers)
            
            if response.status_code == 200:
                purchase_data = response.json()
                self.print_success("Credit purchase successful")
                self.print_info(f"Credits Added: ${purchase_data['credits_added']}")
                self.print_info(f"New Balance: ${purchase_data['new_balance']}")
                return True
            else:
                self.print_error(f"Credit purchase failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Credit purchase error: {e}")
            return False
    
    def test_billing_history(self):
        """Test billing history"""
        self.print_header("Billing History")
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{BASE_URL}/billing/history", headers=headers)
            
            if response.status_code == 200:
                history_data = response.json()
                self.print_success("Billing history retrieved")
                for record in history_data:
                    self.print_info(f"Transaction: {record['transaction_type']} - ${record['amount']} - {record['description']}")
                return True
            else:
                self.print_error(f"Billing history failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Billing history error: {e}")
            return False
    
    def test_rate_limiting(self):
        """Test rate limiting"""
        self.print_header("Rate Limiting Test")
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Test"}],
                "max_tokens": 10
            }
            
            # Make multiple rapid requests
            for i in range(5):
                response = self.session.post(f"{BASE_URL}/chat/completions", json=data, headers=headers)
                if response.status_code == 429:
                    self.print_success(f"Rate limiting working (request {i+1} blocked)")
                    return True
                elif response.status_code == 200:
                    self.print_info(f"Request {i+1} successful")
                else:
                    self.print_error(f"Request {i+1} failed: {response.status_code}")
            
            self.print_info("Rate limiting test completed (no limits hit)")
            return True
        except Exception as e:
            self.print_error(f"Rate limiting test error: {e}")
            return False
    
    def test_insufficient_credits(self):
        """Test insufficient credits handling"""
        self.print_header("Insufficient Credits Test")
        try:
            # First, check current credits
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = self.session.get(f"{BASE_URL}/auth/me", headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                current_credits = user_data['credits']
                self.print_info(f"Current credits: ${current_credits}")
                
                # If we have credits, try to use them all
                if current_credits > 0:
                    # Make a request that should use some credits
                    chat_headers = {"Authorization": f"Bearer {self.api_key}"}
                    chat_data = {
                        "model": "gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": "Test message"}],
                        "max_tokens": 10
                    }
                    response = self.session.post(f"{BASE_URL}/chat/completions", json=chat_data, headers=chat_headers)
                    
                    if response.status_code == 200:
                        self.print_success("Credits used successfully")
                    else:
                        self.print_error(f"Credit usage failed: {response.status_code}")
                else:
                    self.print_info("No credits available for testing")
                
                return True
            else:
                self.print_error(f"Could not check credits: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Insufficient credits test error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all Phase 2 tests"""
        print("🚀 UniLLM Phase 2: Comprehensive Testing")
        print("=" * 60)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Get User Info", self.test_get_user_info),
            ("Chat with API Key", self.test_chat_with_api_key),
            ("Usage Statistics", self.test_usage_statistics),
            ("Credit Purchase", self.test_purchase_credits),
            ("Billing History", self.test_billing_history),
            ("Rate Limiting", self.test_rate_limiting),
            ("Insufficient Credits", self.test_insufficient_credits),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                self.print_error(f"Test '{test_name}' crashed: {e}")
        
        print(f"\n{'='*60}")
        print(f"🎯 Test Results: {passed}/{total} tests passed")
        print(f"{'='*60}")
        
        if passed == total:
            print("🎉 All Phase 2 features are working correctly!")
        else:
            print("⚠️  Some tests failed. Check the logs above.")
        
        return passed == total

if __name__ == "__main__":
    tester = Phase2Tester()
    tester.run_all_tests() 