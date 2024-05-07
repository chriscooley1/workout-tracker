from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    created_at: datetime = Field(default=datetime.utcnow)

class Goal(SQLModel, table=True):
    goal_id: int = Field(default=None, primary_key=True)
    user_id: int  # Linking to the user model
    goal_description: str
    target_date: str
    user: User = Relationship()

class IntensityLevel(SQLModel, table=True):
    level_id: int = Field(default=None, primary_key=True)
    name: str

class Progress(SQLModel, table=True):
    progress_id: int = Field(default=None, primary_key=True)
    workout_id: int
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

class Equipment(SQLModel, table=True):
    equipment_id: int | None = Field(default=None, primary_key=True)
    name: str
    workouts: list["Workout"] = Relationship(back_populates="equipment", link_model=WorkoutEquipmentLink)

class MuscleGroup(SQLModel, table=True):
    group_id: int | None = Field(default=None, primary_key=True)
    name: str
    workouts: list["Workout"] = Relationship(back_populates="muscle_groups", link_model=WorkoutMuscleGroupLink)

class Workout(SQLModel, table=True):
    workout_id: int | None = Field(default=None, primary_key=True)
    name: str
    reps: int
    sets: int
    intensity_level_id: int  # Foreign key to IntensityLevel
    muscle_groups: list[MuscleGroup] = Relationship(back_populates="workouts", link_model=WorkoutMuscleGroupLink)
    equipment: list[Equipment] = Relationship(back_populates="workouts", link_model=WorkoutEquipmentLink)
    progress: list[Progress] = Relationship(back_populates="workout")


# class WorkoutMuscleGroupLink(SQLModel, table=True):
#     workout_id: int = Field(primary_key=True)
#     group_id: int = Field(primary_key=True)

#     # Define foreign keys
#     workout: "Workout" = Field(foreign_key="workout.workout_id")
#     muscle_group: "MuscleGroup" = Field(foreign_key="muscle_group.group_id")

# class WorkoutEquipmentLink(SQLModel, table=True):
#     workout_id: int = Field(primary_key=True)
#     equipment_id: int = Field(primary_key=True)

#     # Define foreign keys
#     workout: "Workout" = Field(foreign_key="workout.workout_id")
#     equipment: "Equipment" = Field(foreign_key="equipment.equipment_id")





# class StudentCourseLink(SQLModel, table=True):
#     student_id: int = Field(foreign_key="student.student_id", primary_key=True)
#     course_id: int = Field(foreign_key="course.course_id", primary_key=True)

# class Student(SQLModel, table=True):
#     student_id: int | None = Field(default=None, primary_key=True)
#     name: str
#     courses: list["Course"] = Relationship(back_populates="students", link_model=StudentCourseLink)

# class Instructor(SQLModel, table=True):
#     instructor_id: int | None = Field(default=None, primary_key=True)
#     name: str
#     courses: list["Course"] = Relationship(back_populates="instructor")

# class Course(SQLModel, table=True):
#     course_id: int | None = Field(default=None, primary_key=True)
#     name: str
#     semester: str
#     students: list[Student] = Relationship(back_populates="courses", link_model=StudentCourseLink)

#     instructor_id: int = Field(default=None, foreign_key="instructor.instructor_id")
#     instructor: Instructor = Relationship(back_populates="courses")
