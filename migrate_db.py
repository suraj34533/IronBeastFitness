from app import app, db
import models

# Add the missing columns to the Exercise table
with app.app_context():
    print("Adding missing columns to Exercise table...")
    try:
        # Check if the columns don't exist before adding them
        columns = db.session.execute(db.text("PRAGMA table_info(exercise)")).fetchall()
        column_names = [col[1] for col in columns]
        
        # Add muscle_group column if it doesn't exist
        if 'muscle_group' not in column_names:
            db.session.execute(db.text("ALTER TABLE exercise ADD COLUMN muscle_group VARCHAR(50)"))
            print("Added muscle_group column")
        
        # Add image_url column if it doesn't exist
        if 'image_url' not in column_names:
            db.session.execute(db.text("ALTER TABLE exercise ADD COLUMN image_url VARCHAR(255)"))
            print("Added image_url column")
        
        # Add video_url column if it doesn't exist
        if 'video_url' not in column_names:
            db.session.execute(db.text("ALTER TABLE exercise ADD COLUMN video_url VARCHAR(255)"))
            print("Added video_url column")
        
        db.session.commit()
        print("Exercise table migration completed successfully!")
        
        # Re-seed the exercise data to populate the new columns
        print("Re-seeding exercise data...")
        # First, clear existing exercise data
        db.session.execute(db.text("DELETE FROM exercise"))
        db.session.commit()
        
        # Seed the data
        models.seed_data()
        print("Data re-seeded successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error during migration: {e}")