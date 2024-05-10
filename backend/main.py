from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from datetime import datetime

from database import get_db
from models import Equipment, MuscleGroup, Workout, Progress, Goal, User


app = FastAPI()


### GET ###

@app.get("/workouts")
async def get_workouts(db: Session = Depends(get_db)) -> list[Workout]:
    return db.exec(select(Workout)).all()

@app.get("/equipment")
async def get_equipment(db: Session = Depends(get_db)) -> list[Equipment]:
    return db.exec(select(Equipment)).all()

@app.get("/muscle_groups")
async def get_muscle_groups(db: Session = Depends(get_db)) -> list[MuscleGroup]:
    return db.exec(select(MuscleGroup)).all()

@app.get("/workouts/{workout_id}/muscle_groups")
async def get_workout_muscle_groups(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.workout_id == workout_id).first()
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    muscle_groups = workout.workout_muscle_groups
    return muscle_groups

@app.get("/workouts/{workout_id}/equipment")
async def get_workout_equipment(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.workout_id == workout_id).first()
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    equipment = workout.workout_equipment_groups
    return equipment

@app.get("/workouts/{workout_id}/progress")
async def get_workout_progress(workout_id: int, db: Session = Depends(get_db)) -> float:
    return calculate_progress(workout_id, db)

@app.get("/goals/{goal_id}")
async def get_goal(goal_id: int, db: Session = Depends(get_db)) -> Goal:
    statement = select(Goal).where(Goal.goal_id == goal_id)
    return db.exec(statement).first()

### POST ###

@app.post("/workouts")
async def create_workout(workout: Workout, db: Session = Depends(get_db)) -> None:
    db.add(workout)
    db.commit()

@app.post("/equipment")
async def create_equipment(equipment: Equipment, db: Session = Depends(get_db)) -> None:
    db.add(equipment)
    db.commit()

@app.post("/muscle_groups")
async def create_muscle_group(group: MuscleGroup, db: Session = Depends(get_db)) -> None:
    db.add(group)
    db.commit()

@app.post("/workouts/{workout_id}/muscle_groups/{group_id}")
async def add_muscle_group_to_workout(workout_id: int, group_id: int, db: Session = Depends(get_db)) -> None:
    statement = select(MuscleGroup).where(MuscleGroup.group_id == group_id)
    muscle_group = db.exec(statement).first()

    statement = select(Workout).where(Workout.workout_id == workout_id)
    workout = db.exec(statement).first()

    workout.muscle_groups.append(muscle_group)
    db.commit()

@app.post("/workouts/{workout_id}/equipment/{equipment_id}")
async def add_equipment_to_workout(workout_id: int, equipment_id: int, db: Session = Depends(get_db)) -> None:
    statement = select(Equipment).where(Equipment.equipment_id == equipment_id)
    equip = db.exec(statement).first()

    statement = select(Workout).where(Workout.workout_id == workout_id)
    workout = db.exec(statement).first()

    workout.equipment.append(equip)
    db.commit()

@app.post("/goals")
async def create_goal(goal: Goal, db: Session = Depends(get_db)) -> Goal:
    return set_goal(goal.user_id, goal.goal_description, goal.target_date, db)

@app.post("/workouts/{workout_id}/progress")
async def add_workout_progress(workout_id: int, progress: Progress, db: Session = Depends(get_db)) -> None:
    progress.workout_id = workout_id
    db.add(progress)
    db.commit()


### Business Logic ###

def set_goal(user_id: int, goal_description: str, target_date: str, db: Session) -> Goal:
    goal = Goal(user_id=user_id, goal_description=goal_description, target_date=target_date)
    db.add(goal)
    db.commit()
    return goal

def calculate_progress(workout_id: int, db: Session) -> float:
    # Retrieve all progress entries related to the workout
    statement = select(Progress).where(Progress.workout_id == workout_id)
    progress_list = db.exec(statement).all()

    total_reps = 0
    total_sets = 0
    num_entries = len(progress_list)

    # Calculate the total reps and sets
    for progress in progress_list:
        total_reps += progress.reps
        total_sets += progress.sets

    # Calculate the average reps and sets
    average_reps = total_reps / num_entries if num_entries > 0 else 0
    average_sets = total_sets / num_entries if num_entries > 0 else 0

    # You can calculate progress based on other metrics as needed
    # For example, you can calculate progress based on weight lifted, duration, etc.

    # For simplicity, let's calculate progress as the average of reps and sets
    progress = (average_reps + average_sets) / 2

    return progress

def set_goal_achieved(user_id: int, goal_id: int, db: Session) -> bool:
    # Retrieve the goal from the database
    goal = db.get(Goal, goal_id)
    if not goal:
        return False  # Goal not found

    # Ensure that the goal belongs to the specified user
    if goal.user_id != user_id:
        return False  # Goal does not belong to the user

    # Retrieve all progress entries related to the goal
    statement = select(Progress).where(Progress.workout_id == goal_id)
    progress_list = db.exec(statement).all()

    # Calculate the total progress made towards the goal
    total_progress = 0
    for progress in progress_list:
        # Implement your logic to calculate progress towards the goal
        # For example, you can sum up reps, sets, or any other relevant metric
        total_progress += progress.reps * progress.sets

    # Check if the total progress meets or exceeds the goal target
    if total_progress >= goal.target:
        return True  # Goal achieved
    else:
        return False  # Goal not achieved
    
def calculate_progress_towards_goal(workout_id: int, goal_id: int, db: Session) -> float:
    # Retrieve all progress entries related to the workout
    statement = select(Progress).where(Progress.workout_id == workout_id)
    progress_list = db.exec(statement).all()

    total_progress = 0

    # Calculate the total progress based on relevant metrics (e.g., reps, sets, weight lifted, etc.)
    for progress in progress_list:
        total_progress += progress.reps * progress.sets  # For simplicity, just multiplying reps and sets here

    # Retrieve the goal from the database
    goal_statement = select(Goal).where(Goal.goal_id == goal_id)
    goal = db.exec(goal_statement).first()

    # Compare the accumulated progress with the target set in the goal
    progress_towards_goal = (total_progress / goal.target) * 100  # Assuming the target is in the same units as progress

    return progress_towards_goal

def handle_skip_workout(workout_id: int, punishment_duration: int, db: Session) -> None:
    # Retrieve the progress entry related to the skipped workout
    statement = select(Progress).where(Progress.workout_id == workout_id)
    progress = db.exec(statement).first()

    if progress:
        # Update the progress entry to indicate that the workout was skipped
        progress.name = "Skipped"
        
        # Apply punishment duration (e.g., subtract from duration_minutes)
        progress.duration_minutes -= punishment_duration
        
        # Commit the changes to the database
        db.commit()
    else:
        # Handle the case where no progress entry is found for the workout
        raise HTTPException(status_code=404, detail="Progress entry not found for the specified workout")





# from sqlalchemy.orm import relationship, selectinload


# @app.get("/workouts/{workout_id}/muscle_groups")
# async def get_workout_muscle_groups(workout_id: int, db: Session = Depends(get_db)):
#     # Query for the Workout object and load the workout_muscle_groups relationship
#     workout = db.query(Workout).filter(Workout.workout_id == workout_id).options(selectinload(Workout.workout_muscle_groups)).first()
#     if workout is None:
#         raise HTTPException(status_code=404, detail="Workout not found")
#     muscle_groups = Workout.workout_muscle_groups
#     return muscle_groups

# @app.get("/workouts/{workout_id}/equipment")
# async def get_workout_equipment(workout_id: int, db: Session = Depends(get_db)):
#     workout = db.query(Workout).filter(Workout.workout_id == workout_id).options(selectinload(Workout.workout_equipment_groups)).first()
#     if workout is None:
#         raise HTTPException(status_code=404, detail="Workout not found")
#     equipment = Workout.workout_equipment_groups
#     return equipment