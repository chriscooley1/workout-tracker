from pydantic import BaseModel


class Workout(BaseModel):
    id: int
    name: str
    set: int
    rep: int
    weight: int