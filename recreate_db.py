from app import app, db
import os

# Delete the current database file
db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace('sqlite:///', '')
if os.path.exists(db_path):
    print(f"Removing existing database at {db_path}")
    os.remove(db_path)
else:
    print(f"No database found at {db_path}, will create a new one")

# Create all tables and seed the database
with app.app_context():
    print("Creating all tables...")
    import models
    db.create_all()
    
    print("Seeding database...")
    models.seed_data()
    
    print("Database has been recreated and seeded!")