from fastapi import FastAPI

from models import Workout


app = FastAPI()

workouts: list[Workout] = []


@app.get("/workouts")
async def get_workouts() -> None:
    return workouts

@app.post("/workouts")
async def create_workouts() -> None:
    pass

@app.put("/workouts")
async def update_workouts() -> None:
    pass

@app.delete("/workouts")
async def delete_workouts() -> None:
    pass