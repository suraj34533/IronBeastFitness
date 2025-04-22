from app import app, db
from models import ExercisePlan

def add_exercise_plans():
    with app.app_context():
        print("Adding exercise plans for different muscle groups...")
        
        # Muscle-specific plans
        plans = [
            ExercisePlan(
                name="Chest Builder",
                category="strength",
                description="Specialized chest training program to build impressive pectoral muscles.",
                difficulty="intermediate"
            ),
            ExercisePlan(
                name="Arm Blaster",
                category="strength",
                description="Focused bicep training to build sleeve-busting arms.",
                difficulty="intermediate"
            ),
            ExercisePlan(
                name="Boulder Shoulders",
                category="strength",
                description="Comprehensive shoulder workout for width and strength.",
                difficulty="intermediate"
            ),
            ExercisePlan(
                name="Tricep Builder",
                category="strength",
                description="Specialized tricep training for arm size and strength.",
                difficulty="intermediate"
            ),
            ExercisePlan(
                name="Lower Body Power",
                category="strength",
                description="Complete leg training program for size and strength.",
                difficulty="intermediate"
            ),
            ExercisePlan(
                name="Core Crusher",
                category="strength",
                description="Intensive core workout for developing visible abs and functional strength.",
                difficulty="intermediate"
            )
        ]
        
        for plan in plans:
            existing_plan = ExercisePlan.query.filter_by(name=plan.name).first()
            if not existing_plan:
                db.session.add(plan)
                print(f"Added plan: {plan.name}")
            else:
                print(f"Plan already exists: {plan.name}")
        
        db.session.commit()
        print("Exercise plans added successfully!")

if __name__ == "__main__":
    add_exercise_plans()