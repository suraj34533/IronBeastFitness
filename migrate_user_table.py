from app import app, db
import models
from datetime import datetime

# Add missing created_at column to User table
with app.app_context():
    print("Adding missing created_at column to User table...")
    try:
        # Check if the column doesn't exist before adding it
        columns = db.session.execute(db.text("PRAGMA table_info(user)")).fetchall()
        column_names = [col[1] for col in columns]
        
        # Add created_at column if it doesn't exist
        if 'created_at' not in column_names:
            db.session.execute(db.text("ALTER TABLE user ADD COLUMN created_at DATETIME"))
            print("Added created_at column")
            
            # Set default values for existing rows
            db.session.execute(db.text("UPDATE user SET created_at = ?"), 
                              [datetime.utcnow()])
            print("Set default values for created_at")
        else:
            print("created_at column already exists")
        
        db.session.commit()
        print("User table migration completed successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error during migration: {e}")
        
    print("\nCurrent User table structure:")
    result = db.session.execute(db.text("PRAGMA table_info(user)"))
    for row in result:
        print(f"- {row[1]}: {row[2]}")