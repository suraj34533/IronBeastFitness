from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import app, db, login_manager
from models import User, UserProfile, ExercisePlan, Exercise, DietPlan, Meal, CalorieEntry, WorkoutLog, seed_data
from forms import LoginForm, RegistrationForm
from datetime import datetime

# Seed the database with initial data
with app.app_context():
    seed_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercise-plans')
def exercise_plans():
    muscle_group = request.args.get('muscle_group')
    
    # Get all plans
    plans = ExercisePlan.query.all()
    
    # Get all muscle groups for filtering
    muscle_groups = db.session.query(Exercise.muscle_group).distinct().all()
    muscle_groups = [m[0] for m in muscle_groups if m[0]]  # Extract unique muscle groups
    
    return render_template(
        'exercise_plans.html', 
        plans=plans, 
        muscle_groups=muscle_groups,
        selected_muscle_group=muscle_group
    )

@app.route('/exercise-plan/<int:plan_id>')
def exercise_plan_detail(plan_id):
    muscle_group = request.args.get('muscle_group')
    
    plan = ExercisePlan.query.get_or_404(plan_id)
    
    # Filter exercises by muscle group if specified
    if muscle_group:
        exercises = Exercise.query.filter_by(plan_id=plan_id, muscle_group=muscle_group).all()
    else:
        exercises = Exercise.query.filter_by(plan_id=plan_id).all()
    
    # Get all muscle groups for this plan for filtering
    plan_muscle_groups = (
        db.session.query(Exercise.muscle_group)
        .filter_by(plan_id=plan_id)
        .distinct()
        .all()
    )
    plan_muscle_groups = [m[0] for m in plan_muscle_groups if m[0]]
    
    return render_template(
        'exercise_plans.html', 
        plan=plan, 
        exercises=exercises, 
        is_detail=True,
        muscle_groups=plan_muscle_groups,
        selected_muscle_group=muscle_group
    )

@app.route('/muscle-groups/<muscle_group>')
def muscle_group_exercises(muscle_group):
    # Get exercises for the specific muscle group
    exercises = Exercise.query.filter_by(muscle_group=muscle_group).all()
    
    # Get all plans that have exercises for this muscle group
    plan_ids = db.session.query(Exercise.plan_id).filter_by(muscle_group=muscle_group).distinct().all()
    plan_ids = [p[0] for p in plan_ids]
    plans = ExercisePlan.query.filter(ExercisePlan.id.in_(plan_ids)).all()
    
    return render_template(
        'muscle_group.html', 
        muscle_group=muscle_group, 
        exercises=exercises,
        plans=plans
    )

@app.route('/diet-plans')
def diet_plans():
    plans = DietPlan.query.all()
    return render_template('diet_plans.html', plans=plans)

@app.route('/diet-plan/<int:plan_id>')
def diet_plan_detail(plan_id):
    plan = DietPlan.query.get_or_404(plan_id)
    meals = Meal.query.filter_by(diet_plan_id=plan_id).all()
    return render_template('diet_plans.html', plan=plan, meals=meals, is_detail=True)

@app.route('/powerlifting')
def powerlifting():
    # Get the powerlifting specific plans
    plans = ExercisePlan.query.filter_by(category='powerlifting').all()
    return render_template('powerlifting.html', plans=plans)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        # Handle form submission for tracking calories and protein
        try:
            calories = int(request.form.get('calories', 0))
            protein = int(request.form.get('protein', 0))
            description = request.form.get('description', '')
            
            # In a real app, we would associate this with a logged-in user
            # For now, just store it in the database without a user_id
            entry = CalorieEntry(
                calories=calories,
                protein=protein,
                description=description,
                date=datetime.utcnow().date(),
                user_id=1  # This would normally be the current user's ID
            )
            db.session.add(entry)
            db.session.commit()
            
            flash('Your calorie and protein intake has been recorded!', 'success')
        except ValueError:
            flash('Please enter valid numbers for calories and protein.', 'error')
        
        return redirect(url_for('calculator'))
    
    # For GET requests, just render the calculator page
    return render_template('calculator.html')

@app.route('/calculate-tdee', methods=['POST'])
def calculate_tdee():
    data = request.json
    
    weight = float(data.get('weight', 0))
    height = float(data.get('height', 0))
    age = int(data.get('age', 0))
    gender = data.get('gender', 'male')
    activity_level = data.get('activityLevel', 'sedentary')
    
    # Calculate BMR (Basal Metabolic Rate) using the Mifflin-St Jeor Equation
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Apply activity multiplier to get TDEE (Total Daily Energy Expenditure)
    activity_multipliers = {
        'sedentary': 1.2,        # Little or no exercise
        'light': 1.375,          # Light exercise 1-3 days/week
        'moderate': 1.55,        # Moderate exercise 3-5 days/week
        'active': 1.725,         # Hard exercise 6-7 days/week
        'very_active': 1.9       # Very hard exercise & physical job or 2x training
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)
    
    # Calculate recommended protein intake (0.8g - 1.2g per pound of bodyweight)
    protein_min = round(weight * 0.8)
    protein_max = round(weight * 1.2)
    
    return jsonify({
        'bmr': round(bmr),
        'tdee': round(tdee),
        'protein_min': protein_min,
        'protein_max': protein_max
    })

@app.route('/hints')
def hints():
    return render_template('hints.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        # Check if input is email or username
        username_or_email = form.username.data
        user = None
        
        if username_or_email and '@' in username_or_email:
            user = User.query.filter_by(email=username_or_email).first()
        else:
            user = User.query.filter_by(username=username_or_email).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username/email and password.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('Username or email already exists. Please try a different one.', 'error')
            return render_template('register.html', form=form)
        
        # Create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Create user profile
        profile = UserProfile(
            user_id=new_user.id,
            full_name=form.username.data
        )
        
        db.session.add(profile)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    # Get user profile, or create if it doesn't exist
    user_profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    if not user_profile:
        user_profile = UserProfile(user_id=current_user.id)
        db.session.add(user_profile)
        db.session.commit()
    
    # Get user details as a dictionary for template
    user_details = {
        'full_name': user_profile.full_name or '',
        'phone': user_profile.phone or '',
        'bio': user_profile.bio or '',
        'fitness_goal': user_profile.fitness_goal or '',
        'profile_image': user_profile.profile_image or ''
    }
    
    # Get recent workout logs
    recent_workouts = WorkoutLog.query.filter_by(user_id=current_user.id).order_by(WorkoutLog.date.desc()).limit(5).all()
    
    # Calculate stats
    today = datetime.utcnow().date()
    
    # Get calorie entries for today and calculate stats
    daily_calories = CalorieEntry.query.filter_by(user_id=current_user.id, date=today).all()
    calories_today = sum(entry.calories for entry in daily_calories) if daily_calories else 0
    protein_today = sum(entry.protein for entry in daily_calories) if daily_calories else 0
    
    # Calculate averages (placeholder data for now)
    avg_calories = 2100  # Sample data
    avg_protein = 150  # Sample data
    
    # Workout stats
    workouts_this_week = 3  # Sample data
    total_workouts = WorkoutLog.query.filter_by(user_id=current_user.id).count()
    
    stats = {
        'daily_calories': calories_today,
        'daily_protein': protein_today,
        'avg_calories': avg_calories,
        'avg_protein': avg_protein,
        'workouts_this_week': workouts_this_week,
        'total_workouts': total_workouts
    }
    
    return render_template('profile.html', 
                          user_details=user_details, 
                          recent_workouts=recent_workouts, 
                          stats=stats)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    full_name = request.form.get('full_name')
    phone = request.form.get('phone')
    bio = request.form.get('bio')
    fitness_goal = request.form.get('fitness_goal')
    
    # Get or create user profile
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.session.add(profile)
    
    # Update profile information
    profile.full_name = full_name
    profile.phone = phone
    if bio:
        profile.bio = bio
    if fitness_goal:
        profile.fitness_goal = fitness_goal
    
    db.session.commit()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))
