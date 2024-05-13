from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from database import get_db
from models import User, Goal, MuscleGroup, Equipment, Workout, Progress, IntensityLevel

app = FastAPI()

# Get operations
@app.get("/user")
async def get_users(db: Session = Depends(get_db)) -> list[User]:
    return db.exec(select(User)).all()

@app.get("/goal")
async def get_goals(db: Session = Depends(get_db)) -> list[Goal]:
    return db.exec(select(Goal)).all()

@app.get("/muscle_group")
async def get_muscle_groups(db: Session = Depends(get_db)) -> list[MuscleGroup]:
    return db.exec(select(MuscleGroup)).all()

@app.get("/equipment")
async def get_equipment(db: Session = Depends(get_db)) -> list[Equipment]:
    return db.exec(select(Equipment)).all()

@app.get("/workout")
async def get_workouts(db: Session = Depends(get_db)) -> list[Workout]:
    return db.exec(select(Workout)).all()

@app.get("/progress")
async def get_progress(db: Session = Depends(get_db)) -> list[Progress]:
    return db.exec(select(Progress)).all()

@app.get("/intensity_level")
async def get_intensity_levels(db: Session = Depends(get_db)) -> list[IntensityLevel]:
    return db.exec(select(IntensityLevel)).all()

# Post operations
@app.post("/user")
async def create_user(user: User, db: Session = Depends(get_db)) -> None:
    db.add(user)
    db.commit()

@app.post("/goal")
async def create_goal(goal: Goal, db: Session = Depends(get_db)) -> None:
    db.add(goal)
    db.commit()

@app.post("/muscle_group")
async def create_muscle_group(muscle_group: MuscleGroup, db: Session = Depends(get_db)) -> None:
    db.add(muscle_group)
    db.commit()

@app.post("/equipment")
async def create_equipment(equipment: Equipment, db: Session = Depends(get_db)) -> None:
    db.add(equipment)
    db.commit()

@app.post("/workout")
async def create_workout(workout: Workout, db: Session = Depends(get_db)) -> None:
    db.add(workout)
    db.commit()

@app.post("/progress")
async def create_progress(progress: Progress, db: Session = Depends(get_db)) -> None:
    db.add(progress)
    db.commit()

@app.post("/intensity_level")
async def create_intensity_level(intensity_level: IntensityLevel, db: Session = Depends(get_db)) -> None:
    db.add(intensity_level)
    db.commit()

# Delete operation
@app.delete("/user/{user_id}")
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}