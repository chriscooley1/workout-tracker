import json

from fastapi import FastAPI

from models import Workout


app = FastAPI()

with open("workout.json", "r") as f:
    data = json.load(f)

workouts: list[Workout] = []

for workout in data:
    workouts.append(Workout(**workout))


@app.get("/workouts")
async def get_workouts() -> list[Workout]:
    return workouts

@app.post("/workouts")
async def create_workouts(workout: Workout) -> None:
    workouts.append(workout)

@app.put("/workouts{workout_id}")
async def update_workouts(workout_id: int, updated_workout: Workout) -> None:
    for i, workout in enumerate(workouts):
        if workout.id == workout_id:
            workouts[i] = updated_workout
            return

@app.delete("/workouts{workout_id}")
async def delete_workouts(workout_id: int) -> None:
    for i, workout in enumerate(workouts):
        if workout.id == workout_id:
            workouts.pop(i)
            return