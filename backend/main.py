from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from database import get_db
from models import User, Goal, MuscleGroup, Equipment, Workout, Progress, IntensityLevel
from fastapi.responses import JSONResponse

app = FastAPI()

# Get operations for User
@app.get("/user")
async def get_users(db: Session = Depends(get_db)) -> list[User]:
    return db.exec(select(User)).all()

# Get operations for Goal
@app.get("/goal")
async def get_goals(db: Session = Depends(get_db)) -> list[Goal]:
    return db.exec(select(Goal)).all()

# Get operations for MuscleGroup
@app.get("/muscle_group")
async def get_muscle_groups(db: Session = Depends(get_db)) -> list[MuscleGroup]:
    return db.exec(select(MuscleGroup)).all()

# Get operations for Equipment
@app.get("/equipment")
async def get_equipment(db: Session = Depends(get_db)) -> list[Equipment]:
    return db.exec(select(Equipment)).all()

# Get operations for Workout
@app.get("/workout")
async def get_workouts(db: Session = Depends(get_db)) -> list[Workout]:
    return db.exec(select(Workout)).all()

# Get operations for Progress
@app.get("/progress")
async def get_progress(db: Session = Depends(get_db)) -> list[Progress]:
    return db.exec(select(Progress)).all()

# Get operations for IntensityLevel
@app.get("/intensity_level")
async def get_intensity_levels(db: Session = Depends(get_db)) -> list[IntensityLevel]:
    return db.exec(select(IntensityLevel)).all()

# Post operations for User
@app.post("/user")
async def create_user(user: User, db: Session = Depends(get_db)) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Post operations for Goal
@app.post("/goal")
async def create_goal(goal: Goal, db: Session = Depends(get_db)) -> Goal:
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

# Post operations for MuscleGroup
@app.post("/muscle_group")
async def create_muscle_group(muscle_group: MuscleGroup, db: Session = Depends(get_db)) -> MuscleGroup:
    db.add(muscle_group)
    db.commit()
    db.refresh(muscle_group)
    return muscle_group

# Post operations for Equipment
@app.post("/equipment")
async def create_equipment(equipment: Equipment, db: Session = Depends(get_db)) -> Equipment:
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment

# Post operations for Workout
@app.post("/workout")
async def create_workout(workout: Workout, db: Session = Depends(get_db)) -> Workout:
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

# Post operations for Progress
@app.post("/progress")
async def create_progress(progress: Progress, db: Session = Depends(get_db)) -> Progress:
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress

# Post operations for IntensityLevel
@app.post("/intensity_level")
async def create_intensity_level(intensity_level: IntensityLevel, db: Session = Depends(get_db)):
    db.add(intensity_level)
    db.commit()
    db.refresh(intensity_level)  # This will refresh the instance with the database's updated state
    return JSONResponse(status_code=200, content=intensity_level.model_dump())
    
# Update or create operations for User
@app.put("/user/{user_id}")
async def update_or_create_user(user_id: int, user: User, db: Session = Depends(get_db)) -> None:
    db_user = db.get(User, user_id)
    if not db_user:
        db_user = User(**user.dict(), user_id=user_id)
        db.add(db_user)
    else:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
    db.commit()

# Update or create operations for Goal
@app.put("/goal/{goal_id}")
async def update_or_create_goal(goal_id: int, goal: Goal, db: Session = Depends(get_db)) -> None:
    db_goal = db.get(Goal, goal_id)
    if not db_goal:
        db_goal = Goal(**goal.dict(), goal_id=goal_id)
        db.add(db_goal)
    else:
        for key, value in goal.dict().items():
            setattr(db_goal, key, value)
    db.commit()

# Update or create operations for MuscleGroup
@app.put("/muscle_group/{group_id}")
async def update_or_create_muscle_group(group_id: int, muscle_group: MuscleGroup, db: Session = Depends(get_db)) -> None:
    db_group = db.get(MuscleGroup, group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Muscle Group not found")
    for key, value in muscle_group.dict(exclude_unset=True).items():
        setattr(db_group, key, value)
    db.commit()

# Update or create operations for Equipment
@app.put("/equipment/{equipment_id}")
async def update_or_create_equipment(equipment_id: int, equipment: Equipment, db: Session = Depends(get_db)) -> None:
    db_equipment = db.get(Equipment, equipment_id)
    if not db_equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    for key, value in equipment.dict(exclude_unset=True).items():
        setattr(db_equipment, key, value)
    db.commit()

# Update or create operations for Workout
@app.put("/workout/{workout_id}")
async def update_or_create_workout(workout_id: int, workout: Workout, db: Session = Depends(get_db)) -> None:
    db_workout = db.get(Workout, workout_id)
    if not db_workout:
        db_workout = Workout(**workout.dict(), workout_id=workout_id)
        db.add(db_workout)
    else:
        for key, value in workout.dict().items():
            setattr(db_workout, key, value)
    db.commit()

# Update or create operations for Progress
@app.put("/progress/{progress_id}")
async def update_progress(progress_id: int, updated_progress: Progress, db: Session = Depends(get_db)) -> Progress:
    progress = db.get(Progress, progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    progress.date_completed = updated_progress.date_completed
    db.commit()
    db.refresh(progress)
    return progress

# Update or create operations for IntensityLevel
@app.put("/intensity_level/{intensity_id}")
async def update_or_create_intensity_level(intensity_id: int, intensity_level: IntensityLevel, db: Session = Depends(get_db)) -> None:
    db_intensity_level = db.get(IntensityLevel, intensity_id)
    if not db_intensity_level:
        db_intensity_level = IntensityLevel(**intensity_level.dict(), intensity_id=intensity_id)
        db.add(db_intensity_level)
    else:
        for key, value in intensity_level.model_dump(exclude_unset=True).items():
            setattr(db_intensity_level, key, value)
    db.commit()

# Delete operations for User
@app.delete("/user/{user_id}")
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Delete operations for Goal
@app.delete("/goal/{goal_id}")
async def remove_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted successfully"}

# Delete operations for MuscleGroup
@app.delete("/muscle_group/{group_id}")
async def remove_muscle_group(group_id: int, db: Session = Depends(get_db)):
    muscle_group = db.get(MuscleGroup, group_id)
    if not muscle_group:
        raise HTTPException(status_code=404, detail="Muscle Group not found")
    db.delete(muscle_group)
    db.commit()
    return {"message": "Muscle Group deleted successfully"}

# Delete operations for Equipment
@app.delete("/equipment/{equipment_id}")
async def remove_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    db.delete(equipment)
    db.commit()
    return {"message": "Equipment deleted successfully"}

# Delete operations for Workout
@app.delete("/workout/{workout_id}")
async def remove_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.get(Workout, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout)
    db.commit()
    return {"message": "Workout deleted successfully"}

# Delete operations for Progress
@app.delete("/progress/{progress_id}")
async def delete_progress(progress_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    progress = db.get(Progress, progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    db.delete(progress)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Progress deleted successfully"})

# Delete operations for IntensityLevel
@app.delete("/intensity_level/{intensity_id}")
async def remove_intensity_level(intensity_id: int, db: Session = Depends(get_db)):
    intensity_level = db.get(IntensityLevel, intensity_id)
    if not intensity_level:
        raise HTTPException(status_code=404, detail="Intensity Level not found")
    db.delete(intensity_level)
    db.commit()
    return {"message": "Intensity Level deleted successfully"}
