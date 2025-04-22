from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, mongo
from models import ExercisePlan, Exercise, DietPlan, Meal, CalorieEntry, WorkoutLog, seed_data
from auth import User
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
    plans = ExercisePlan.query.all()
    return render_template('exercise_plans.html', plans=plans)

@app.route('/exercise-plan/<int:plan_id>')
def exercise_plan_detail(plan_id):
    plan = ExercisePlan.query.get_or_404(plan_id)
    exercises = Exercise.query.filter_by(plan_id=plan_id).all()
    return render_template('exercise_plans.html', plan=plan, exercises=exercises, is_detail=True)

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


# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Check if input is email or username
        if '@' in form.username.data:
            user = User.get_by_email(form.username.data)
        else:
            user = User.get_by_username(form.username.data)
        
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
    if form.validate_on_submit():
        user = User.register(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        
        if user:
            flash(f'Account created for {form.username.data}! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists. Please try a different one.', 'error')
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    # For future implementation
    return "Profile page - coming soon!"
