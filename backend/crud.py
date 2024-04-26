from sqlalchemy.orm import Session

import models
import schemas


def get_workouts(db: Session):
    return db.query(models.Workout).all()

def create_workout(db: Session, workout: schemas.WorkoutCreate):
    db_workout = models.Workout(**workout.model_dump())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout