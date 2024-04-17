from pydantic import BaseModel


class Workout(BaseModel):
    exercise: str
    set: int
    rep: int
    weight: int