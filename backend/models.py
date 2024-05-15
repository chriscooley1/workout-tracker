from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional

class UserBase(SQLModel):
    username: str
    email: str
    password: str

class User(UserBase, table=True):
    __tablename__ = "users"
    user_id: Optional[int] = Field(default=None, primary_key=True)
    goals: List["Goal"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    pass

class GoalBase(SQLModel):
    name: str
    goal_description: str
    user_id: int

class Goal(GoalBase, table=True):
    __tablename__ = "goals"
    goal_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    user: User = Relationship(back_populates="goals")

class GoalCreate(GoalBase):
    pass

class MuscleGroupBase(SQLModel):
    name: str

class MuscleGroup(MuscleGroupBase, table=True):
    __tablename__ = "muscle_groups"
    group_id: Optional[int] = Field(default=None, primary_key=True)

class MuscleGroupCreate(MuscleGroupBase):
    pass

class EquipmentBase(SQLModel):
    name: str
    description: str

class Equipment(EquipmentBase, table=True):
    __tablename__ = "equipment"
    equipment_id: Optional[int] = Field(default=None, primary_key=True)

class EquipmentCreate(EquipmentBase):
    pass

class WorkoutBase(SQLModel):
    name: str
    description: str
    group_id: int
    equipment_id: int
    reps: Optional[int] = Field(default=None)
    sets: Optional[int] = Field(default=None)
    weights: Optional[float] = Field(default=None)

class Workout(WorkoutBase, table=True):
    __tablename__ = "workouts"
    workout_id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="muscle_groups.group_id")
    equipment_id: int = Field(foreign_key="equipment.equipment_id")

class WorkoutCreate(WorkoutBase):
    pass

class ProgressBase(SQLModel):
    user_id: int
    workout_id: int
    date_completed: str

class Progress(ProgressBase, table=True):
    __tablename__ = "progress"
    progress_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    workout_id: int = Field(foreign_key="workouts.workout_id")

class ProgressCreate(ProgressBase):
    pass

class IntensityLevelBase(SQLModel):
    name: str
    description: str

class IntensityLevel(IntensityLevelBase, table=True):
    __tablename__ = "intensity_levels"
    intensity_id: Optional[int] = Field(default=None, primary_key=True)

class IntensityLevelCreate(IntensityLevelBase):
    pass
