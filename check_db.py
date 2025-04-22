from app import app, db
import models

with app.app_context():
    print("Tables in the database:")
    # Get all table names from sqlite_master
    result = db.session.execute(db.text('SELECT name FROM sqlite_master WHERE type="table"'))
    for row in result:
        print(f"- {row[0]}")
    
    # Check if Exercise table has muscle_group column
    try:
        print("\nChecking Exercise table structure:")
        result = db.session.execute(db.text("PRAGMA table_info(exercise)"))
        for row in result:
            print(f"- {row[1]}: {row[2]}")
    except Exception as e:
        print(f"Error checking table: {e}")