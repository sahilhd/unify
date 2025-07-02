#!/usr/bin/env python3
"""
Database Migration Script for UniLLM
Migrates from SQLite to PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine, text
from database import Base, DATABASE_URL, engine

def check_database_connection():
    """Check if we can connect to the database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_tables():
    """Create all tables in the database"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def verify_tables():
    """Verify that all required tables exist"""
    required_tables = ['users', 'usage_logs', 'billing_history']
    
    try:
        with engine.connect() as conn:
            for table in required_tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"✅ Table '{table}' exists with {count} records")
        return True
    except Exception as e:
        print(f"❌ Table verification failed: {e}")
        return False

def main():
    print("🗄️  UniLLM Database Migration")
    print("=" * 40)
    
    # Check database type
    if DATABASE_URL.startswith("postgresql://"):
        print("📊 Using PostgreSQL database")
    elif DATABASE_URL.startswith("sqlite://"):
        print("📱 Using SQLite database (local development)")
    else:
        print(f"🔗 Using database: {DATABASE_URL}")
    
    print(f"🔗 Database URL: {DATABASE_URL[:50]}...")
    
    # Step 1: Check connection
    print("\n1️⃣ Checking database connection...")
    if not check_database_connection():
        sys.exit(1)
    
    # Step 2: Create tables
    print("\n2️⃣ Creating database tables...")
    if not create_tables():
        sys.exit(1)
    
    # Step 3: Verify tables
    print("\n3️⃣ Verifying tables...")
    if not verify_tables():
        sys.exit(1)
    
    print("\n🎉 Database migration completed successfully!")
    print("Your UniLLM backend is ready to use with persistent storage!")

if __name__ == "__main__":
    main() 