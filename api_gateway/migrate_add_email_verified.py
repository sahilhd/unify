#!/usr/bin/env python3
"""
Migration script to add email_verified column to users table
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migration():
    """Add email_verified column to users table"""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    try:
        # Create database engine
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            # Check if column already exists
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
        return False

if __name__ == "__main__":
    success = run_migration()
    if success:
        print("\n🎉 Database migration completed!")
        print("   The email_verified column has been added to the users table.")
        print("   Existing users have been marked as email_verified = true.")
    else:
        print("\n💥 Migration failed. Please check the error above.")
        sys.exit(1) 