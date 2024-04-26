from pydantic import BaseModel


class WorkoutBase(BaseModel):
    number: int
    description: str

class WorkoutCreate(WorkoutBase):
    pass

class Workout(WorkoutBase):
    id: int

    class Config:
        from_attributes = True