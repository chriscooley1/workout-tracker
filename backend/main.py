from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import get_db
from models import User, UserCreate, Goal, GoalCreate, MuscleGroup, MuscleGroupCreate, Equipment, EquipmentCreate, Workout, WorkoutCreate, Progress, ProgressCreate, IntensityLevel, IntensityLevelCreate
from fastapi.responses import JSONResponse

app = FastAPI()

# Get operations for User
@app.get("/user")
async def get_users(db: Session = Depends(get_db)) -> list[User]:
    return db.exec(select(User)).all()

# Post operations for User
@app.post("/user", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = User.model_validate(user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Put operations for User
@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete operations for User
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> User:
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

# Get operations for Goal
@app.get("/goal")
async def get_goals(db: Session = Depends(get_db)) -> list[Goal]:
    return db.exec(select(Goal)).all()

# Post operations for Goal
@app.post("/goal", response_model=Goal)
async def create_goal(goal: GoalCreate, db: Session = Depends(get_db)) -> Goal:
    db_goal = Goal.model_validate(goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

# Put operations for Goal
@app.put("/goal/{goal_id}", response_model=Goal)
async def update_goal(goal_id: int, updated_goal: GoalCreate, db: Session = Depends(get_db)) -> Goal:
    db_goal = db.get(Goal, goal_id)
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for key, value in updated_goal.model_dump().items():
        setattr(db_goal, key, value)
    db.commit()
    db.refresh(db_goal)
    return db_goal

# Delete operations for Goal
@app.delete("/goal/{goal_id}", response_model=Goal)
async def delete_goal(goal_id: int, db: Session = Depends(get_db)) -> Goal:
    db_goal = db.get(Goal, goal_id)
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(db_goal)
    db.commit()
    return db_goal

# Get operations for Muscle Group
@app.get("/muscle_group")
async def get_muscle_groups(db: Session = Depends(get_db)) -> list[MuscleGroup]:
    return db.exec(select(MuscleGroup)).all()

# Post operations for Muscle Group
@app.post("/muscle_group", response_model=MuscleGroup)
async def create_muscle_group(muscle_group: MuscleGroupCreate, db: Session = Depends(get_db)) -> MuscleGroup:
    db_muscle_group = MuscleGroup.model_validate(muscle_group.model_dump())
    db.add(db_muscle_group)
    db.commit()
    db.refresh(db_muscle_group)
    return db_muscle_group

# Get operations for Equipment
@app.get("/equipment")
async def get_equipment(db: Session = Depends(get_db)) -> list[Equipment]:
    return db.exec(select(Equipment)).all()

# Post operations for Equipment
@app.post("/equipment", response_model=Equipment)
async def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)) -> Equipment:
    db_equipment = Equipment.model_validate(equipment.model_dump())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

# Get operations for Workout
@app.get("/workout")
async def get_workouts(db: Session = Depends(get_db)) -> list[Workout]:
    return db.exec(select(Workout)).all()

# Post operations for Workout
@app.post("/workout", response_model=Workout)
async def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)) -> Workout:
    db_workout = Workout.model_validate(workout.model_dump())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

# Put operations for Workout
@app.put("/workout/{workout_id}", response_model=Workout)
async def update_workout(workout_id: int, updated_workout: WorkoutCreate, db: Session = Depends(get_db)) -> Workout:
    db_workout = db.get(Workout, workout_id)
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    for key, value in updated_workout.dict().items():
        setattr(db_workout, key, value)
    db.commit()
    db.refresh(db_workout)
    return db_workout

# Delete operations for Workout
@app.delete("/workout/{workout_id}", response_model=Workout)
async def delete_workout(workout_id: int, db: Session = Depends(get_db)) -> Workout:
    db_workout = db.get(Workout, workout_id)
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(db_workout)
    db.commit()
    return db_workout

# Get operations for Progress
@app.get("/progress")
async def get_progress(db: Session = Depends(get_db)) -> list[Progress]:
    return db.exec(select(Progress)).all()

# Post operations for Progress
@app.post("/progress", response_model=Progress)
async def create_progress(progress: ProgressCreate, db: Session = Depends(get_db)) -> Progress:
    db_progress = Progress.model_validate(progress.model_dump())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

# Put operations for Progress
@app.put("/progress/{progress_id}", response_model=Progress)
async def update_progress(progress_id: int, updated_progress: ProgressCreate, db: Session = Depends(get_db)) -> Progress:
    db_progress = db.get(Progress, progress_id)
    if not db_progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    for key, value in updated_progress.dict().items():
        setattr(db_progress, key, value)
    db.commit()
    db.refresh(db_progress)
    return db_progress

# Delete operations for Progress
@app.delete("/progress/{progress_id}", response_model=Progress)
async def delete_progress(progress_id: int, db: Session = Depends(get_db)) -> Progress:
    db_progress = db.get(Progress, progress_id)
    if not db_progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    db.delete(db_progress)
    db.commit()
    return db_progress

# Get operations for IntensityLevel
@app.get("/intensity_level")
async def get_intensity_levels(db: Session = Depends(get_db)) -> list[IntensityLevel]:
    return db.exec(select(IntensityLevel)).all()

# Post operations for IntensityLevel
@app.post("/intensity_level", response_model=IntensityLevel)
async def create_intensity_level(intensity_level: IntensityLevelCreate, db: Session = Depends(get_db)) -> IntensityLevel:
    db_intensity_level = IntensityLevel.model_validate(intensity_level.model_dump())
    db.add(db_intensity_level)
    db.commit()
    db.refresh(db_intensity_level)
    return db_intensity_level
