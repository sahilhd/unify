#!/usr/bin/env python3
"""
UniLLM Dashboard Launcher
Launches the enhanced UI dashboard with all dependencies
"""

import subprocess
import sys
import os
import time
import requests

def print_banner():
    """Print the launcher banner"""
    print("🤖 UniLLM Dashboard Launcher")
    print("=" * 40)
    print()

def install_dependencies():
    """Install dashboard dependencies"""
    print("📦 Installing dashboard dependencies...")
    
    try:
        # Install requirements
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements_dashboard.txt"
        ], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_server():
    """Check if UniLLM server is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def launch_dashboard():
    """Launch the enhanced dashboard"""
    print("🚀 Launching UniLLM Dashboard...")
    
    # Check if server is running
    if not check_server():
        print("⚠️  UniLLM server is not running on port 8000")
        print("   Please start the server first with: python main_phase2.py")
        return False
    
    print("✅ UniLLM server is running!")
    
    try:
        # Launch the enhanced dashboard
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard_enhanced_ui.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
        return True
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
        return True
    except Exception as e:
        print(f"❌ Failed to launch dashboard: {e}")
        return False

def main():
    print_banner()
    
    # Install dependencies
    if not install_dependencies():
        return
    
    print()
    
    # Launch dashboard
    launch_dashboard()

if __name__ == "__main__":
    main() 