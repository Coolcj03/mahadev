#!/usr/bin/env python3
"""
Database initialization script for Render deployment.
This script will create all tables and initial data.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_database():
    """Initialize the database on Render"""
    try:
        # Import database components
        from database import engine, init_database
        from models import Base
        
        print("🚀 Starting database initialization on Render...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Initialize with sample data if needed
        print("🎉 Database initialization completed!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
