from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    goals: list['Goal'] = Relationship(back_populates="user")

class Goal(SQLModel, table=True):
    __tablename__ = "goals"
    goal_id: int = Field(default=None, primary_key=True)
    name: str
    goal_description: str
    user_id: int = Field(foreign_key="users.user_id")

    user: User = Relationship(back_populates="goals")

class MuscleGroup(SQLModel, table=True):
    group_id: int = Field(default=None, primary_key=True)
    name: str

class Equipment(SQLModel, table=True):
    equipment_id: int = Field(default=None, primary_key=True)
    name: str
    description: str

class Workout(SQLModel, table=True):
    __tablename__ = "workouts"
    workout_id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    muscle_group_id: int = Field(foreign_key="muscle_groups.group_id")
    equipment_id: int = Field(foreign_key="equipment.equipment_id")

class Progress(SQLModel, table=True):
    __tablename__ = "progress"
    progress_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    workout_id: int = Field(foreign_key="workouts.workout_id")
    date_completed: str

class IntensityLevel(SQLModel, table=True):
    intensity_id: int = Field(default=None, primary_key=True)
    name: str
    description: str
