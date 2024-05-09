from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    created_at: datetime = Field(default=datetime.utcnow)
    goals: list["Goal"] = Relationship(back_populates="user")

class Goal(SQLModel, table=True):
    goal_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # Define foreign key constraint
    goal_description: str
    target_date: str
    user: User = Relationship(back_populates="goals")

class IntensityLevel(SQLModel, table=True):
    level_id: int = Field(default=None, primary_key=True)
    name: str

class Progress(SQLModel, table=True):
    progress_id: int = Field(default=None, primary_key=True)
    workout_id: int = Field(foreign_key="workout.workout_id")
    name: str
    reps: int
    sets: int
    intensity_level_id: int 
    weight_lifted: float
    duration_minutes: int

class WorkoutMuscleGroupLink(SQLModel, table=True):
    workout_id: int = Field(foreign_key="workout.workout_id", primary_key=True)
    group_id: int = Field(foreign_key="muscle_group.group_id", primary_key=True)

class WorkoutEquipmentLink(SQLModel, table=True):
    workout_id: int = Field(foreign_key="workout.workout_id", primary_key=True)
    equipment_id: int = Field(foreign_key="equipment.equipment_id", primary_key=True)

class MuscleGroup(SQLModel, table=True):
    group_id: int | None = Field(default=None, primary_key=True)
    name: str

class Equipment(SQLModel, table=True):
    equipment_id: int | None = Field(default=None, primary_key=True)
    name: str

class Workout(SQLModel, table=True):
    workout_id: int | None = Field(default=None, primary_key=True)
    name: str
    reps: int
    sets: int
    intensity_level_id: int = Field(foreign_key="intensity_level.level_id") # Foreign key to IntensityLevel

# Define the relationship between Workout and MuscleGroup
workout_muscle_groups = relationship(
    "MuscleGroup",
    secondary="workoutmusclegrouplink",
    primaryjoin="Workout.workout_id == WorkoutMuscleGroupLink.workout_id",
    secondaryjoin="MuscleGroup.group_id == WorkoutMuscleGroupLink.group_id",
    back_populates="workouts"
)

workout_equipment_groups = relationship(
    "MuscleGroup",
    secondary="workoutequipmentlink",
    primaryjoin="Workout.workout_id == WorkoutEquipmentLink.workout_id",
    secondaryjoin="MuscleGroup.group_id == WorkoutEquipmentLink.group_id",
    back_populates="workouts"
)
