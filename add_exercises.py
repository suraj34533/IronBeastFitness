from app import app, db
from models import Exercise, ExercisePlan
from datetime import datetime

# Add specific exercises for each muscle group
def add_muscle_exercises():
    with app.app_context():
        print("Adding specific exercises for each muscle group...")
        
        # Get plans for each muscle group
        chest_plan = ExercisePlan.query.filter_by(name="Chest Builder").first()
        bicep_plan = ExercisePlan.query.filter_by(name="Arm Blaster").first()
        shoulder_plan = ExercisePlan.query.filter_by(name="Boulder Shoulders").first()
        tricep_plan = ExercisePlan.query.filter_by(name="Tricep Builder").first()
        legs_plan = ExercisePlan.query.filter_by(name="Lower Body Power").first()
        
        if not chest_plan or not bicep_plan or not shoulder_plan or not tricep_plan or not legs_plan:
            print("One or more plans not found, no exercises added.")
            return
        
        # Delete existing exercises for these plans
        for plan in [chest_plan, bicep_plan, shoulder_plan, tricep_plan, legs_plan]:
            db.session.query(Exercise).filter_by(plan_id=plan.id).delete()
        
        # Chest exercises
        chest_exercises = [
            Exercise(
                name="Barbell Bench Press",
                description="A compound chest exercise that targets the pectoralis major.",
                sets=4,
                reps="8-10",
                rest="90 seconds",
                plan_id=chest_plan.id,
                muscle_group="chest",
                image_url="/static/images/exercises/barbell_bench_press.jpg",
                video_url="https://www.youtube.com/embed/rT7DgCr-3pg"
            ),
            Exercise(
                name="Incline Dumbbell Press",
                description="Targets the upper chest muscles.",
                sets=3,
                reps="10-12",
                rest="60 seconds",
                plan_id=chest_plan.id,
                muscle_group="chest",
                image_url="/static/images/exercises/incline_dumbbell_press.jpg",
                video_url="https://www.youtube.com/embed/8iPEnn-ltC8"
            ),
            Exercise(
                name="Dumbbell Flyes",
                description="Isolation exercise for chest that stretches and contracts the pectoral muscles.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=chest_plan.id,
                muscle_group="chest",
                image_url="/static/images/exercises/dumbbell_flyes.jpg",
                video_url="https://www.youtube.com/embed/eozdVDA78K0"
            ),
            Exercise(
                name="Cable Crossover",
                description="Isolation exercise that works on chest definition.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=chest_plan.id,
                muscle_group="chest",
                image_url="/static/images/exercises/cable_crossover.jpg",
                video_url="https://www.youtube.com/embed/taI4XduLpTk"
            ),
            Exercise(
                name="Push-ups",
                description="Bodyweight exercise targeting chest, shoulders, and triceps.",
                sets=4,
                reps="Max",
                rest="60 seconds",
                plan_id=chest_plan.id,
                muscle_group="chest",
                image_url="/static/images/exercises/push_ups.jpg",
                video_url="https://www.youtube.com/embed/IODxDxX7oi4"
            )
        ]
        
        # Bicep exercises
        bicep_exercises = [
            Exercise(
                name="Barbell Curl",
                description="Classic bicep exercise using a barbell.",
                sets=4,
                reps="10-12",
                rest="60 seconds",
                plan_id=bicep_plan.id,
                muscle_group="bicep",
                image_url="/static/images/exercises/barbell_curl.jpg",
                video_url="https://www.youtube.com/embed/LY1V6UbRHFM"
            ),
            Exercise(
                name="Strict Curl",
                description="Strict form barbell curl, competition style.",
                sets=3,
                reps="8-10",
                rest="90 seconds",
                plan_id=bicep_plan.id,
                muscle_group="bicep",
                image_url="/static/images/exercises/strict_curl.jpg",
                video_url="https://www.youtube.com/embed/vsCkbGBiOcI"
            ),
            Exercise(
                name="Hammer Curl",
                description="Targets the brachialis muscle with neutral grip.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=bicep_plan.id,
                muscle_group="bicep",
                image_url="/static/images/exercises/hammer_curl.jpg",
                video_url="https://www.youtube.com/embed/zC3nLlEvin4"
            ),
            Exercise(
                name="Preacher Curl",
                description="Isolated bicep exercise that removes body momentum.",
                sets=3,
                reps="10-12",
                rest="60 seconds",
                plan_id=bicep_plan.id,
                muscle_group="bicep",
                image_url="/static/images/exercises/preacher_curl.jpg",
                video_url="https://www.youtube.com/embed/fIWP-FRFNU0"
            ),
            Exercise(
                name="Concentration Curl",
                description="Seated single-arm curl for maximum bicep peak.",
                sets=3,
                reps="12-15",
                rest="45 seconds",
                plan_id=bicep_plan.id,
                muscle_group="bicep",
                image_url="/static/images/exercises/concentration_curl.jpg",
                video_url="https://www.youtube.com/embed/Jvj2wV0vOYU"
            )
        ]
        
        # Shoulder exercises
        shoulder_exercises = [
            Exercise(
                name="Military Press",
                description="Compound exercise for shoulders using a barbell.",
                sets=4,
                reps="8-10",
                rest="90 seconds",
                plan_id=shoulder_plan.id,
                muscle_group="shoulder",
                image_url="/static/images/exercises/military_press.jpg",
                video_url="https://www.youtube.com/embed/2yjwXTZQDDI"
            ),
            Exercise(
                name="Lateral Raises",
                description="Isolation exercise for the lateral deltoids.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=shoulder_plan.id,
                muscle_group="shoulder",
                image_url="/static/images/exercises/lateral_raises.jpg",
                video_url="https://www.youtube.com/embed/3VcKaXpzqRo"
            ),
            Exercise(
                name="Front Raises",
                description="Targets the anterior deltoids.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=shoulder_plan.id,
                muscle_group="shoulder",
                image_url="/static/images/exercises/front_raises.jpg",
                video_url="https://www.youtube.com/embed/sxeMSVQgZfA"
            ),
            Exercise(
                name="Rear Delt Flyes",
                description="Isolation movement for the posterior deltoids.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=shoulder_plan.id,
                muscle_group="shoulder",
                image_url="/static/images/exercises/rear_delt_flyes.jpg",
                video_url="https://www.youtube.com/embed/EA7u4Q_8HQ0"
            ),
            Exercise(
                name="Face Pulls",
                description="Compound movement for rear delts, traps, and rotator cuffs.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=shoulder_plan.id,
                muscle_group="shoulder",
                image_url="/static/images/exercises/face_pulls.jpg",
                video_url="https://www.youtube.com/embed/V8dZ3pyiCBo"
            )
        ]
        
        # Tricep exercises
        tricep_exercises = [
            Exercise(
                name="Close-Grip Bench Press",
                description="Compound movement targeting triceps using barbell.",
                sets=4,
                reps="8-10",
                rest="90 seconds",
                plan_id=tricep_plan.id,
                muscle_group="tricep",
                image_url="/static/images/exercises/close_grip_bench.jpg",
                video_url="https://www.youtube.com/embed/nEF0bv2FW94"
            ),
            Exercise(
                name="Tricep Dips",
                description="Bodyweight exercise for triceps.",
                sets=3,
                reps="10-12",
                rest="60 seconds",
                plan_id=tricep_plan.id,
                muscle_group="tricep",
                image_url="/static/images/exercises/tricep_dips.jpg",
                video_url="https://www.youtube.com/embed/wjUmnZH528Y"
            ),
            Exercise(
                name="Tricep Pushdown",
                description="Cable exercise isolating the triceps.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=tricep_plan.id,
                muscle_group="tricep",
                image_url="/static/images/exercises/tricep_pushdown.jpg",
                video_url="https://www.youtube.com/embed/2-LAMcpzODU"
            ),
            Exercise(
                name="Skull Crushers",
                description="Lying tricep extension targeting all three heads.",
                sets=3,
                reps="10-12",
                rest="60 seconds",
                plan_id=tricep_plan.id,
                muscle_group="tricep",
                image_url="/static/images/exercises/skull_crushers.jpg",
                video_url="https://www.youtube.com/embed/d_KZxkY_0cM"
            ),
            Exercise(
                name="Overhead Tricep Extension",
                description="Isolation exercise emphasizing the long head of the triceps.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=tricep_plan.id,
                muscle_group="tricep",
                image_url="/static/images/exercises/overhead_extension.jpg",
                video_url="https://www.youtube.com/embed/X-iV-cG8cYs"
            )
        ]
        
        # Leg exercises
        leg_exercises = [
            Exercise(
                name="Barbell Squat",
                description="Compound leg exercise targeting quads, hamstrings, and glutes.",
                sets=4,
                reps="8-10",
                rest="90 seconds",
                plan_id=legs_plan.id,
                muscle_group="legs",
                image_url="/static/images/exercises/barbell_squat.jpg",
                video_url="https://www.youtube.com/embed/1oed-UmAxFs"
            ),
            Exercise(
                name="Romanian Deadlift",
                description="Hip-hinge movement targeting hamstrings and glutes.",
                sets=3,
                reps="10-12",
                rest="90 seconds",
                plan_id=legs_plan.id,
                muscle_group="legs",
                image_url="/static/images/exercises/romanian_deadlift.jpg",
                video_url="https://www.youtube.com/embed/jEy_czb3RKA"
            ),
            Exercise(
                name="Leg Press",
                description="Machine compound movement for quadriceps development.",
                sets=3,
                reps="10-12",
                rest="90 seconds",
                plan_id=legs_plan.id,
                muscle_group="legs",
                image_url="/static/images/exercises/leg_press.jpg",
                video_url="https://www.youtube.com/embed/IZxyjW7MPJQ"
            ),
            Exercise(
                name="Leg Extensions",
                description="Isolation exercise for quadriceps.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=legs_plan.id,
                muscle_group="legs",
                image_url="/static/images/exercises/leg_extensions.jpg",
                video_url="https://www.youtube.com/embed/YyvSfVjQeL0"
            ),
            Exercise(
                name="Leg Curls",
                description="Isolation exercise for hamstrings.",
                sets=3,
                reps="12-15",
                rest="60 seconds",
                plan_id=legs_plan.id,
                muscle_group="legs",
                image_url="/static/images/exercises/leg_curls.jpg",
                video_url="https://www.youtube.com/embed/1Tq3QdYUuHs"
            )
        ]
        
        # Add all exercises to the database
        all_exercises = chest_exercises + bicep_exercises + shoulder_exercises + tricep_exercises + leg_exercises
        db.session.add_all(all_exercises)
        db.session.commit()
        
        print(f"Added {len(all_exercises)} exercises successfully!")
        print(f"- {len(chest_exercises)} chest exercises")
        print(f"- {len(bicep_exercises)} bicep exercises")
        print(f"- {len(shoulder_exercises)} shoulder exercises")
        print(f"- {len(tricep_exercises)} tricep exercises")
        print(f"- {len(leg_exercises)} leg exercises")

if __name__ == "__main__":
    add_muscle_exercises()