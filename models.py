from app import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User's tracking data
    calorie_entries = db.relationship('CalorieEntry', backref='user', lazy=True)
    workout_logs = db.relationship('WorkoutLog', backref='user', lazy=True)
    profile = db.relationship('UserProfile', backref='user', uselist=False, lazy=True)
    
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    fitness_goal = db.Column(db.String(100))
    profile_image = db.Column(db.String(255))  # URL to profile image


class ExercisePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., "strength", "cardio", "powerlifting"
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # "beginner", "intermediate", "advanced"
    exercises = db.relationship('Exercise', backref='plan', lazy=True)


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.String(50))  # Can be "10-12" or just "10"
    rest = db.Column(db.String(20))  # Rest time, e.g., "60 seconds"
    plan_id = db.Column(db.Integer, db.ForeignKey('exercise_plan.id'), nullable=False)
    muscle_group = db.Column(db.String(50))  # e.g., "chest", "bicep", "shoulder", "tricep", "legs", "back", "core"
    image_url = db.Column(db.String(255))  # URL to exercise image
    video_url = db.Column(db.String(255))  # URL to exercise demonstration video


class DietPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    goal = db.Column(db.String(50), nullable=False)  # e.g., "weight loss", "muscle gain", "maintenance"
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)  # in grams
    carbs = db.Column(db.Integer, nullable=False)  # in grams
    fats = db.Column(db.Integer, nullable=False)  # in grams
    meals = db.relationship('Meal', backref='diet_plan', lazy=True)


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)  # in grams
    carbs = db.Column(db.Integer, nullable=False)  # in grams
    fats = db.Column(db.Integer, nullable=False)  # in grams
    diet_plan_id = db.Column(db.Integer, db.ForeignKey('diet_plan.id'), nullable=False)


class CalorieEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)  # in grams
    description = db.Column(db.String(200))


class WorkoutLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    exercise_name = db.Column(db.String(100), nullable=False)
    sets_completed = db.Column(db.Integer, nullable=False)
    reps_per_set = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.String(50))  # Can be "bodyweight" or a number + unit
    notes = db.Column(db.Text)


# Add some initial data for the exercise plans, diet plans, etc.
def seed_data():
    # Exercise Plans
    if ExercisePlan.query.count() == 0:
        # Strength Training Plan
        strength_plan = ExercisePlan(
            name="Full Body Strength",
            category="strength",
            description="A comprehensive full body strength training program designed to build muscle and increase overall strength.",
            difficulty="intermediate"
        )
        
        # Powerlifting Plan
        powerlifting_plan = ExercisePlan(
            name="5/3/1 Powerlifting",
            category="powerlifting",
            description="Jim Wendler's 5/3/1 program focused on the big three lifts: squat, bench press, and deadlift.",
            difficulty="advanced"
        )
        
        # HIIT Plan
        hiit_plan = ExercisePlan(
            name="High Intensity Interval Training",
            category="cardio",
            description="Short bursts of intense exercise alternated with low-intensity recovery periods.",
            difficulty="beginner"
        )
        
        db.session.add_all([strength_plan, powerlifting_plan, hiit_plan])
        db.session.commit()
        
        # Muscle-specific plans
        chest_plan = ExercisePlan(
            name="Chest Builder",
            category="strength",
            description="Specialized chest training program to build impressive pectoral muscles.",
            difficulty="intermediate"
        )
        
        bicep_plan = ExercisePlan(
            name="Arm Blaster",
            category="strength",
            description="Focused bicep training to build sleeve-busting arms.",
            difficulty="intermediate"
        )
        
        shoulder_plan = ExercisePlan(
            name="Boulder Shoulders",
            category="strength",
            description="Comprehensive shoulder workout for width and strength.",
            difficulty="intermediate"
        )
        
        tricep_plan = ExercisePlan(
            name="Tricep Builder",
            category="strength",
            description="Specialized tricep training for arm size and strength.",
            difficulty="intermediate"
        )
        
        legs_plan = ExercisePlan(
            name="Lower Body Power",
            category="strength",
            description="Complete leg training program for size and strength.",
            difficulty="intermediate"
        )
        
        db.session.add_all([chest_plan, bicep_plan, shoulder_plan, tricep_plan, legs_plan])
        db.session.commit()
        
        # Exercises for Strength Plan
        exercises_strength = [
            Exercise(
                name="Barbell Squat", 
                description="A compound exercise targeting the quadriceps, hamstrings, and glutes.", 
                sets=4, 
                reps="8-10", 
                rest="90 seconds", 
                plan_id=strength_plan.id, 
                muscle_group="legs",
                image_url="/static/images/exercises/barbell_squat.jpg",
                video_url="https://www.youtube.com/embed/watch?v=1oed-UmAxFs"
            ),
            Exercise(
                name="Bench Press", 
                description="A compound upper body exercise targeting the chest, shoulders, and triceps.", 
                sets=4, 
                reps="8-10", 
                rest="90 seconds", 
                plan_id=strength_plan.id, 
                muscle_group="chest",
                image_url="/static/images/exercises/bench_press.jpg",
                video_url="https://www.youtube.com/embed/watch?v=rT7DgCr-3pg"
            ),
            Exercise(
                name="Deadlift", 
                description="A compound exercise targeting the back, glutes, and hamstrings.", 
                sets=3, 
                reps="6-8", 
                rest="120 seconds", 
                plan_id=strength_plan.id, 
                muscle_group="back",
                image_url="/static/images/exercises/deadlift.jpg",
                video_url="https://www.youtube.com/embed/watch?v=ytGaGIn3SjE"
            ),
            Exercise(
                name="Pull-ups", 
                description="An upper body exercise targeting the back and biceps.", 
                sets=3, 
                reps="8-12", 
                rest="60 seconds", 
                plan_id=strength_plan.id, 
                muscle_group="back",
                image_url="/static/images/exercises/pull_ups.jpg",
                video_url="https://www.youtube.com/embed/watch?v=eGo4IYlbE5g"
            ),
            Exercise(
                name="Military Press", 
                description="A shoulder exercise targeting the deltoids and triceps.", 
                sets=3, 
                reps="8-10", 
                rest="60 seconds", 
                plan_id=strength_plan.id, 
                muscle_group="shoulder",
                image_url="/static/images/exercises/military_press.jpg",
                video_url="https://www.youtube.com/embed/watch?v=2yjwXTZQDDI"
            )
        ]
        
        # Exercises for Powerlifting Plan
        exercises_powerlifting = [
            Exercise(
                name="Squat - Main", 
                description="5/3/1 progression for squats.", 
                sets=3, 
                reps="5/3/1", 
                rest="3-5 minutes", 
                plan_id=powerlifting_plan.id, 
                muscle_group="legs",
                image_url="/static/images/exercises/squat_main.jpg",
                video_url="https://www.youtube.com/embed/watch?v=1oed-UmAxFs"
            ),
            Exercise(
                name="Bench Press - Main", 
                description="5/3/1 progression for bench press.", 
                sets=3, 
                reps="5/3/1", 
                rest="3-5 minutes", 
                plan_id=powerlifting_plan.id, 
                muscle_group="chest",
                image_url="/static/images/exercises/bench_main.jpg",
                video_url="https://www.youtube.com/embed/watch?v=rT7DgCr-3pg"
            ),
            Exercise(
                name="Deadlift - Main", 
                description="5/3/1 progression for deadlifts.", 
                sets=3, 
                reps="5/3/1", 
                rest="3-5 minutes", 
                plan_id=powerlifting_plan.id, 
                muscle_group="back",
                image_url="/static/images/exercises/deadlift_main.jpg",
                video_url="https://www.youtube.com/embed/watch?v=ytGaGIn3SjE"
            ),
            Exercise(
                name="Squat - Assistance", 
                description="5x10 at 50-60% of training max.", 
                sets=5, 
                reps="10", 
                rest="60-90 seconds", 
                plan_id=powerlifting_plan.id, 
                muscle_group="legs",
                image_url="/static/images/exercises/squat_assistance.jpg",
                video_url="https://www.youtube.com/embed/watch?v=1oed-UmAxFs"
            ),
            Exercise(
                name="Bench Press - Assistance", 
                description="5x10 at 50-60% of training max.", 
                sets=5, 
                reps="10", 
                rest="60-90 seconds", 
                plan_id=powerlifting_plan.id, 
                muscle_group="chest",
                image_url="/static/images/exercises/bench_assistance.jpg",
                video_url="https://www.youtube.com/embed/watch?v=rT7DgCr-3pg"
            ),
            Exercise(
                name="Deadlift - Assistance", 
                description="5x10 at 50-60% of training max.", 
                sets=5, 
                reps="10", 
                rest="60-90 seconds", 
                plan_id=powerlifting_plan.id, 
                muscle_group="back",
                image_url="/static/images/exercises/deadlift_assistance.jpg",
                video_url="https://www.youtube.com/embed/watch?v=ytGaGIn3SjE"
            )
        ]
        
        # Exercises for HIIT Plan
        exercises_hiit = [
            Exercise(
                name="Burpees", 
                description="A full body exercise combining a squat, push-up, and jump.", 
                sets=4, 
                reps="30 seconds", 
                rest="30 seconds", 
                plan_id=hiit_plan.id, 
                muscle_group="full body",
                image_url="/static/images/exercises/burpees.jpg",
                video_url="https://www.youtube.com/embed/watch?v=TU8QYVW0gDU"
            ),
            Exercise(
                name="Mountain Climbers", 
                description="A cardio exercise targeting the core, shoulders, and legs.", 
                sets=4, 
                reps="30 seconds", 
                rest="30 seconds", 
                plan_id=hiit_plan.id, 
                muscle_group="core",
                image_url="/static/images/exercises/mountain_climbers.jpg",
                video_url="https://www.youtube.com/embed/watch?v=nmwgirgXLYM"
            ),
            Exercise(
                name="Jumping Jacks", 
                description="A classic cardio exercise targeting the whole body.", 
                sets=4, 
                reps="30 seconds", 
                rest="30 seconds", 
                plan_id=hiit_plan.id, 
                muscle_group="full body",
                image_url="/static/images/exercises/jumping_jacks.jpg",
                video_url="https://www.youtube.com/embed/watch?v=c4DAnQ6DtF8"
            ),
            Exercise(
                name="High Knees", 
                description="A cardio exercise targeting the lower body and core.", 
                sets=4, 
                reps="30 seconds", 
                rest="30 seconds", 
                plan_id=hiit_plan.id, 
                muscle_group="legs",
                image_url="/static/images/exercises/high_knees.jpg",
                video_url="https://www.youtube.com/embed/watch?v=TX4FXb0HP4w"
            ),
            Exercise(
                name="Plank", 
                description="A core exercise targeting the abs, back, and shoulders.", 
                sets=4, 
                reps="30 seconds", 
                rest="30 seconds", 
                plan_id=hiit_plan.id, 
                muscle_group="core",
                image_url="/static/images/exercises/plank.jpg",
                video_url="https://www.youtube.com/embed/watch?v=pSHjTRCQxIw"
            )
        ]
        
        # Muscle-specific exercises
        # Chest exercises
        chest_exercises = [
            Exercise(
                name="Dumbbell Bench Press", 
                description="A chest exercise that allows for greater range of motion than barbell bench press.", 
                sets=4, 
                reps="10-12", 
                rest="60 seconds", 
                plan_id=chest_plan.id, 
                muscle_group="chest",
                image_url="/static/images/exercises/dumbbell_bench_press.jpg",
                video_url="https://www.youtube.com/embed/watch?v=QsYre__-aro"
            ),
            Exercise(
                name="Incline Bench Press", 
                description="A chest exercise that targets the upper chest.", 
                sets=3, 
                reps="10-12", 
                rest="60 seconds", 
                plan_id=chest_plan.id, 
                muscle_group="chest",
                image_url="/static/images/exercises/incline_bench_press.jpg",
                video_url="https://www.youtube.com/embed/watch?v=SrqOu55lrYU"
            ),
            Exercise(
                name="Cable Flyes", 
                description="An isolation exercise for the chest.", 
                sets=3, 
                reps="12-15", 
                rest="45 seconds", 
                plan_id=chest_plan.id, 
                muscle_group="chest",
                image_url="/static/images/exercises/cable_flyes.jpg",
                video_url="https://www.youtube.com/embed/watch?v=Iwe6AmxVf7o"
            ),
            Exercise(
                name="Push-Ups", 
                description="A bodyweight exercise for the chest, shoulders, and triceps.", 
                sets=3, 
                reps="15-20", 
                rest="45 seconds", 
                plan_id=chest_plan.id, 
                muscle_group="chest",
                image_url="/static/images/exercises/push_ups.jpg",
                video_url="https://www.youtube.com/embed/watch?v=IODxDxX7oi4"
            )
        ]
        
        # Bicep exercises
        bicep_exercises = [
            Exercise(
                name="Barbell Curls", 
                description="A compound exercise for the biceps.", 
                sets=4, 
                reps="10-12", 
                rest="60 seconds", 
                plan_id=bicep_plan.id, 
                muscle_group="bicep",
                image_url="/static/images/exercises/barbell_curls.jpg",
                video_url="https://www.youtube.com/embed/watch?v=LY1V6UbRHFM"
            ),
            Exercise(
                name="Hammer Curls", 
                description="An exercise that targets the brachialis and brachioradialis muscles.", 
                sets=3, 
                reps="10-12", 
                rest="45 seconds", 
                plan_id=bicep_plan.id, 
                muscle_group="bicep",
                image_url="/static/images/exercises/hammer_curls.jpg",
                video_url="https://www.youtube.com/embed/watch?v=zC3nLlEvin4"
            ),
            Exercise(
                name="Concentration Curls", 
                description="An isolation exercise for the biceps.", 
                sets=3, 
                reps="12-15", 
                rest="45 seconds", 
                plan_id=bicep_plan.id, 
                muscle_group="bicep",
                image_url="/static/images/exercises/concentration_curls.jpg",
                video_url="https://www.youtube.com/embed/watch?v=Jvj2wV0vOYU"
            ),
            Exercise(
                name="Cable Curls", 
                description="A bicep exercise with constant tension.", 
                sets=3, 
                reps="12-15", 
                rest="45 seconds", 
                plan_id=bicep_plan.id, 
                muscle_group="bicep",
                image_url="/static/images/exercises/cable_curls.jpg",
                video_url="https://www.youtube.com/embed/watch?v=NFzTWp2qpiE"
            )
        ]
        
        # Shoulder exercises
        shoulder_exercises = [
            Exercise(
                name="Seated Dumbbell Press", 
                description="A compound exercise for the shoulders.", 
                sets=4, 
                reps="10-12", 
                rest="60 seconds", 
                plan_id=shoulder_plan.id, 
                muscle_group="shoulder",
                image_url="/static/images/exercises/seated_dumbbell_press.jpg",
                video_url="https://www.youtube.com/embed/watch?v=qEwKCR5JCog"
            ),
            Exercise(
                name="Lateral Raises", 
                description="An isolation exercise for the lateral deltoids.", 
                sets=3, 
                reps="12-15", 
                rest="45 seconds", 
                plan_id=shoulder_plan.id, 
                muscle_group="shoulder",
                image_url="/static/images/exercises/lateral_raises.jpg",
                video_url="https://www.youtube.com/embed/watch?v=3VcKaXpzqRo"
            ),
            Exercise(
                name="Front Raises", 
                description="An isolation exercise for the anterior deltoids.", 
                sets=3, 
                reps="12-15", 
                rest="45 seconds", 
                plan_id=shoulder_plan.id, 
                muscle_group="shoulder",
                image_url="/static/images/exercises/front_raises.jpg",
                video_url="https://www.youtube.com/embed/watch?v=sxeY7kMYhLc"
            ),
            Exercise(
                name="Reverse Flyes", 
                description="An isolation exercise for the posterior deltoids.", 
                sets=3, 
                reps="12-15", 
                rest="45 seconds", 
                plan_id=shoulder_plan.id, 
                muscle_group="shoulder",
                image_url="/static/images/exercises/reverse_flyes.jpg",
                video_url="https://www.youtube.com/embed/watch?v=ttvfGg9d76c"
            )
        ]
        
        # Tricep exercises
        tricep_exercises = [
            Exercise(
                name="Tricep Dips", 
                description="A compound exercise for the triceps.", 
                sets=4, 
                reps="10-12", 
                rest="60 seconds", 
                plan_id=tricep_plan.id, 
                muscle_group="tricep",
                image_url="/static/images/exercises/tricep_dips.jpg",
                video_url="https://www.youtube.com/embed/watch?v=6kALZikXxLc"
            ),
            Exercise(
                name="Skull Crushers", 
                description="An isolation exercise for the triceps.", 
                sets=3, 
                reps="10-12", 
                rest="60 seconds", 
                plan_id=tricep_plan.id, 
                muscle_group="tricep",
                image_url="/static/images/exercises/skull_crushers.jpg",
                video_url="https://www.youtube.com/embed/watch?v=d_KZxkY_0cM"
            ),
            Exercise(
                name="Tricep Pushdowns", 
                description="An isolation exercise for the triceps using a cable machine.", 
                sets=3, 
                reps="12-15", 
                rest="45 seconds", 
                plan_id=tricep_plan.id, 
                muscle_group="tricep",
                image_url="/static/images/exercises/tricep_pushdowns.jpg",
                video_url="https://www.youtube.com/embed/watch?v=2-LAMcpzODU"
            ),
            Exercise(
                name="Overhead Tricep Extension", 
                description="An isolation exercise for the triceps that stretches the long head.", 
                sets=3, 
                reps="12-15", 
                rest="45 seconds", 
                plan_id=tricep_plan.id, 
                muscle_group="tricep",
                image_url="/static/images/exercises/overhead_tricep_extension.jpg",
                video_url="https://www.youtube.com/embed/watch?v=_gsUck-7M74"
            )
        ]
        
        # Leg exercises
        leg_exercises = [
            Exercise(
                name="Leg Press", 
                description="A compound exercise for the legs using a machine.", 
                sets=4, 
                reps="10-12", 
                rest="90 seconds", 
                plan_id=legs_plan.id, 
                muscle_group="legs",
                image_url="/static/images/exercises/leg_press.jpg",
                video_url="https://www.youtube.com/embed/watch?v=IZxyjW7MPJQ"
            ),
            Exercise(
                name="Romanian Deadlift", 
                description="A compound exercise targeting the hamstrings and glutes.", 
                sets=3, 
                reps="10-12", 
                rest="90 seconds", 
                plan_id=legs_plan.id, 
                muscle_group="legs",
                image_url="/static/images/exercises/romanian_deadlift.jpg",
                video_url="https://www.youtube.com/embed/watch?v=JCXUYuzwNrM"
            ),
            Exercise(
                name="Leg Extensions", 
                description="An isolation exercise for the quadriceps.", 
                sets=3, 
                reps="12-15", 
                rest="60 seconds", 
                plan_id=legs_plan.id, 
                muscle_group="legs",
                image_url="/static/images/exercises/leg_extensions.jpg",
                video_url="https://www.youtube.com/embed/watch?v=YyvSfVjQeL0"
            ),
            Exercise(
                name="Leg Curls", 
                description="An isolation exercise for the hamstrings.", 
                sets=3, 
                reps="12-15", 
                rest="60 seconds", 
                plan_id=legs_plan.id, 
                muscle_group="legs",
                image_url="/static/images/exercises/leg_curls.jpg",
                video_url="https://www.youtube.com/embed/watch?v=1Tq3QdYUuHs"
            ),
            Exercise(
                name="Calf Raises", 
                description="An isolation exercise for the calves.", 
                sets=4, 
                reps="15-20", 
                rest="45 seconds", 
                plan_id=legs_plan.id, 
                muscle_group="legs",
                image_url="/static/images/exercises/calf_raises.jpg",
                video_url="https://www.youtube.com/embed/watch?v=gwLzBJYoWlI"
            )
        ]
        
        all_exercises = (
            exercises_strength + 
            exercises_powerlifting + 
            exercises_hiit + 
            chest_exercises + 
            bicep_exercises + 
            shoulder_exercises + 
            tricep_exercises + 
            leg_exercises
        )
        
        db.session.add_all(all_exercises)
        db.session.commit()
        
        db.session.add_all(exercises_strength + exercises_powerlifting + exercises_hiit)
        db.session.commit()
    
    # Diet Plans
    if DietPlan.query.count() == 0:
        # Bulking Diet
        bulking_diet = DietPlan(
            name="Muscle Building",
            description="High protein, calorie surplus diet designed to maximize muscle growth.",
            goal="muscle gain",
            calories=3000,
            protein=200,
            carbs=350,
            fats=83
        )
        
        # Cutting Diet
        cutting_diet = DietPlan(
            name="Fat Loss",
            description="Protein-sparing diet designed to preserve muscle while losing fat.",
            goal="weight loss",
            calories=2000,
            protein=180,
            carbs=150,
            fats=67
        )
        
        # Maintenance Diet
        maintenance_diet = DietPlan(
            name="Maintenance",
            description="Balanced diet designed to maintain current body composition.",
            goal="maintenance",
            calories=2500,
            protein=180,
            carbs=250,
            fats=83
        )
        
        db.session.add_all([bulking_diet, cutting_diet, maintenance_diet])
        db.session.commit()
        
        # Meals for Bulking Diet
        meals_bulking = [
            Meal(name="Breakfast", description="Oatmeal with protein powder, banana, and peanut butter.", calories=650, protein=40, carbs=80, fats=20, diet_plan_id=bulking_diet.id),
            Meal(name="Lunch", description="Chicken breast, brown rice, and mixed vegetables.", calories=700, protein=50, carbs=80, fats=15, diet_plan_id=bulking_diet.id),
            Meal(name="Dinner", description="Salmon, sweet potato, and broccoli.", calories=650, protein=40, carbs=60, fats=25, diet_plan_id=bulking_diet.id),
            Meal(name="Snack 1", description="Greek yogurt with berries and honey.", calories=300, protein=20, carbs=40, fats=5, diet_plan_id=bulking_diet.id),
            Meal(name="Snack 2", description="Protein shake with almond milk and banana.", calories=350, protein=30, carbs=40, fats=8, diet_plan_id=bulking_diet.id),
            Meal(name="Pre-Workout", description="Banana and protein bar.", calories=350, protein=20, carbs=50, fats=10, diet_plan_id=bulking_diet.id)
        ]
        
        # Meals for Cutting Diet
        meals_cutting = [
            Meal(name="Breakfast", description="Egg whites with spinach and whole grain toast.", calories=350, protein=30, carbs=30, fats=10, diet_plan_id=cutting_diet.id),
            Meal(name="Lunch", description="Tuna salad with mixed greens and olive oil dressing.", calories=400, protein=40, carbs=20, fats=20, diet_plan_id=cutting_diet.id),
            Meal(name="Dinner", description="Lean ground turkey with quinoa and roasted vegetables.", calories=450, protein=40, carbs=40, fats=15, diet_plan_id=cutting_diet.id),
            Meal(name="Snack 1", description="Protein shake with water.", calories=150, protein=25, carbs=5, fats=2, diet_plan_id=cutting_diet.id),
            Meal(name="Snack 2", description="Cottage cheese with cucumber slices.", calories=200, protein=25, carbs=10, fats=5, diet_plan_id=cutting_diet.id),
            Meal(name="Pre-Workout", description="Apple with a small amount of almond butter.", calories=150, protein=5, carbs=25, fats=5, diet_plan_id=cutting_diet.id)
        ]
        
        # Meals for Maintenance Diet
        meals_maintenance = [
            Meal(name="Breakfast", description="Greek yogurt with granola and berries.", calories=450, protein=30, carbs=50, fats=15, diet_plan_id=maintenance_diet.id),
            Meal(name="Lunch", description="Turkey sandwich on whole grain bread with side salad.", calories=550, protein=40, carbs=60, fats=20, diet_plan_id=maintenance_diet.id),
            Meal(name="Dinner", description="Stir-fry with tofu, brown rice, and vegetables.", calories=600, protein=35, carbs=70, fats=20, diet_plan_id=maintenance_diet.id),
            Meal(name="Snack 1", description="Trail mix with nuts and dried fruit.", calories=300, protein=10, carbs=30, fats=15, diet_plan_id=maintenance_diet.id),
            Meal(name="Snack 2", description="Protein bar.", calories=250, protein=20, carbs=25, fats=8, diet_plan_id=maintenance_diet.id),
            Meal(name="Pre-Workout", description="Banana and small protein shake.", calories=250, protein=20, carbs=30, fats=5, diet_plan_id=maintenance_diet.id)
        ]
        
        db.session.add_all(meals_bulking + meals_cutting + meals_maintenance)
        db.session.commit()
