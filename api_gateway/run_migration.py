#!/usr/bin/env python3
"""
Migration script to add email_verified column to users table
This script can be run on Railway or locally
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migration():
    """Add email_verified column to users table"""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("   Available environment variables:")
        for key, value in os.environ.items():
            if 'DATABASE' in key or 'DB' in key:
                print(f"   {key}: {value[:20]}..." if len(str(value)) > 20 else f"   {key}: {value}")
        return False
    
    # Handle PostgreSQL URL format for Railway
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    try:
        print(f"🔗 Connecting to database...")
        print(f"   URL: {database_url[:50]}..." if len(database_url) > 50 else f"   URL: {database_url}")
        
        # Create database engine
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            # Check if column already exists
            print("🔍 Checking if email_verified column exists...")
            result = connection.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'email_verified'
            """))
            
            if result.fetchone():
                print("✅ email_verified column already exists")
                return True
            
            # Add the email_verified column
            print("🔧 Adding email_verified column to users table...")
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN email_verified BOOLEAN DEFAULT FALSE
            """))
            
            # Update existing users to have email_verified = true (for backward compatibility)
            print("🔄 Updating existing users to have email_verified = true...")
            connection.execute(text("""
                UPDATE users 
                SET email_verified = true 
                WHERE email_verified IS NULL
            """))
            
            connection.commit()
            print("✅ Migration completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🚀 Starting database migration...")
    print("=" * 50)
    
    success = run_migration()
    
    print("=" * 50)
    if success:
        print("🎉 Database migration completed successfully!")
        print("   The email_verified column has been added to the users table.")
        print("   Existing users have been marked as email_verified = true.")
    else:
        print("💥 Migration failed. Please check the error above.")
        sys.exit(1) 