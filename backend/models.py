from sqlmodel import Field, Relationship, SQLModel

class WorkoutMuscleGroupLink(SQLModel, table=True):
    workout_id: int = Field(foreign_key="workout.workout_id", primary_key=True)
    group_id: int = Field(foreign_key="muscle_group.group_id", primary_key=True)

class WorkoutEquipmentLink(SQLModel, table=True):
    workout_id: int = Field(foreign_key="workout.workout_id", primary_key=True)
    equipment_id: int = Field(foreign_key="equipment.equipment_id", primary_key=True)

class Equipment(SQLModel, table=True):
    equipment_id: int | None = Field(default=None, primary_key=True)
    name: str
    workouts: list["Workout"] = Relationship(back_populates="equipment")

class MuscleGroup(SQLModel, table=True):
    group_id: int | None = Field(default=None, primary_key=True)
    name: str
    workouts: list["Workout"] = Relationship(back_populates="muscle_groups")

class Workout(SQLModel, table=True):
    workout_id: int | None = Field(default=None, primary_key=True)
    name: str
    reps: int
    sets: int
    intensity_level: str
    muscle_groups: list[MuscleGroup] = Relationship(back_populates="workouts", link_model=WorkoutMuscleGroupLink)
    equipment: list[Equipment] = Relationship(back_populates="workouts", link_model=WorkoutEquipmentLink)


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
