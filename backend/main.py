from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from datetime import datetime

from database import get_db
from models import Equipment, MuscleGroup, Workout, Progress, Goal


app = FastAPI()


### GET ###

@app.get("/workouts")
async def get_workouts(db: Session = Depends(get_db)) -> list[Workout]:
    return db.exec(select(Workout)).all()

@app.get("/equipment")
async def get_equipment(db: Session = Depends(get_db)) -> list[Equipment]:
    return db.exec(select(Equipment)).all()

@app.get("/muscle_groups")
async def get_muscle_groups(db: Session = Depends(get_db)) -> list[MuscleGroup]:
    return db.exec(select(MuscleGroup)).all()

@app.get("/workouts/{workout_id}/muscle_groups")
async def get_workout_muscle_groups(workout_id: int, db: Session = Depends(get_db)) -> list[MuscleGroup]:
    statement = select(Workout).where(Workout.workout_id == workout_id)
    workout = db.exec(statement).first()
    return workout.muscle_groups

@app.get("/workouts/{workout_id}/equipment")
async def get_workout_equipment(workout_id: int, db: Session = Depends(get_db)) -> list[Equipment]:
    statement = select(Workout).where(Workout.workout_id == workout_id)
    workout = db.exec(statement).first()
    return workout.equipment

@app.get("/workouts/{workout_id}/progress")
async def get_workout_progress(workout_id: int, db: Session = Depends(get_db)) -> float:
    return calculate_progress(workout_id, db)

@app.get("/goals/{goal_id}")
async def get_goal(goal_id: int, db: Session = Depends(get_db)) -> Goal:
    statement = select(Goal).where(Goal.goal_id == goal_id)
    return db.exec(statement).first()

### POST ###

@app.post("/workouts")
async def create_workout(workout: Workout, db: Session = Depends(get_db)) -> None:
    db.add(workout)
    db.commit()

@app.post("/equipment")
async def create_equipment(equipment: Equipment, db: Session = Depends(get_db)) -> None:
    db.add(equipment)
    db.commit()

@app.post("/muscle_groups")
async def create_muscle_group(group: MuscleGroup, db: Session = Depends(get_db)) -> None:
    db.add(group)
    db.commit()

@app.post("/workouts/{workout_id}/muscle_groups/{group_id}")
async def add_muscle_group_to_workout(workout_id: int, group_id: int, db: Session = Depends(get_db)) -> None:
    statement = select(MuscleGroup).where(MuscleGroup.group_id == group_id)
    muscle_group = db.exec(statement).first()

    statement = select(Workout).where(Workout.workout_id == workout_id)
    workout = db.exec(statement).first()

    workout.muscle_groups.append(muscle_group)
    db.commit()

@app.post("/workouts/{workout_id}/equipment/{equipment_id}")
async def add_equipment_to_workout(workout_id: int, equipment_id: int, db: Session = Depends(get_db)) -> None:
    statement = select(Equipment).where(Equipment.equipment_id == equipment_id)
    equip = db.exec(statement).first()

    statement = select(Workout).where(Workout.workout_id == workout_id)
    workout = db.exec(statement).first()

    workout.equipment.append(equip)
    db.commit()

@app.post("/goals")
async def create_goal(goal: Goal, db: Session = Depends(get_db)) -> Goal:
    return set_goal(goal.user_id, goal.goal_description, goal.target_date, db)

@app.post("/workouts/{workout_id}/progress")
async def add_workout_progress(workout_id: int, progress: Progress, db: Session = Depends(get_db)) -> None:
    progress.workout_id = workout_id
    db.add(progress)
    db.commit()


### Business Logic ###

def set_goal(user_id: int, goal_description: str, target_date: str, db: Session) -> Goal:
    goal = Goal(user_id=user_id, goal_description=goal_description, target_date=target_date)
    db.add(goal)
    db.commit()
    return goal

def calculate_progress(workout_id: int, db: Session) -> float:
    statement = select(Progress).where(Progress.workout_id == workout_id)
    progress_list = db.exec(statement).all()

    total_progress = 0
    num_progress_entries = 0

    for progress in progress_list:
        # Implement your logic to calculate progress based on the progress data
        # For example, you can calculate average progress based on reps, sets, weight lifted, etc.
        total_progress += progress.reps * progress.sets  # For simplicity, just multiplying reps and sets here
        num_progress_entries += 1

    if num_progress_entries == 0:
        return 0
    else:
        return total_progress / num_progress_entries

def set_goal_achieved(user_id: int, goal_id: int, db: Session) -> bool:
    statement = select(Progress).where(Progress.workout_id == goal_id)
    progress_list = db.exec(statement).all()

    # Implement logic to check if the goal has been achieved based on the progress made
    # For example, compare progress against the goal target
    # If goal achieved, return True; otherwise, return False
    return True  # Placeholder

def handle_skip_workout(workout_id: int, punishment_duration: int, db: Session) -> None:
    statement = select(Progress).where(Progress.workout_id == workout_id)
    progress = db.exec(statement).first()

    # Implement your logic to handle skip workouts and calculate punishments
    # For example, update progress and apply punishment duration
    progress.name = "Skipped"
    db.commit()



### GET ###

# @app.get("/students")
# async def get_students(db: Session = Depends(get_db)) -> list[Student]:
#     return db.exec(select(Student)).all()

# @app.get("/instructors")
# async def get_instructors(db: Session = Depends(get_db)) -> list[Instructor]:
#     return db.exec(select(Instructor)).all()

# @app.get("/courses")
# async def get_courses(db: Session = Depends(get_db)) -> list[Course]:
#     return db.exec(select(Course)).all()

# @app.get("/courses/{course_id}/students")
# async def get_course_student_list(course_id: int, db: Session = Depends(get_db)) -> list[Student]:
#     statement = select(Course).where(Course.course_id == course_id)
#     course = db.exec(statement).first()
#     return course.students


# ### POST ###

# @app.post("/students")
# async def create_student(student: Student, db: Session = Depends(get_db)) -> None:
#     db.add(student)
#     db.commit()

# @app.post("/instructors")
# async def create_instructor(instructor: Instructor, db: Session = Depends(get_db)) -> None:
#     db.add(instructor)
#     db.commit()

# @app.post("/courses")
# async def create_course(course: Course, db: Session = Depends(get_db)) -> None:
#     db.add(course)
#     db.commit()

# @app.post("/courses/{course_id}/students/{student_id}")
# async def add_student_to_course(course_id: int, student_id: int, db: Session = Depends(get_db)) -> None:
#     statement = select(Student).where(Student.student_id == student_id)
#     student = db.exec(statement).first()

#     statement = select(Course).where(Course.course_id == course_id)
#     course = db.exec(statement).first()

#     course.students.append(student)
#     db.commit()