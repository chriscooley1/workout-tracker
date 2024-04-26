from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models
import schemas

from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The origin of the frontend app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

workouts: list[schemas.Workout] = []

@app.get("/", response_model=list[schemas.Workout])
async def get_workouts(db: Session = Depends(get_db)) -> list[schemas.Workout]:
    return crud.get_workouts(db)

@app.post("/", response_model=schemas.Workout)
async def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db)) -> schemas.Workout:
    return crud.create_workout(db=db, workout=workout)