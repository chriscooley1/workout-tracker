from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from database import get_db
# from models import Course, Instructor, Student
from models import Equipment, MuscleGroup, Workout, WorkoutEquipmentLink, WorkoutMuscleGroupLink


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
    statement = select(WorkoutMuscleGroupLink).where(WorkoutMuscleGroupLink.workout_id == workout_id)
    result = db.exec(statement).all()
    if not result:
        raise HTTPException(status_code=404, detail="Workout not found")
    group_ids = [link.group_id for link in result]
    statement = select(MuscleGroup).where(MuscleGroup.group_id.in_(group_ids))
    return db.exec(statement).all()

@app.get("/workouts/{workout_id}/equipment")
async def get_workout_equipment(workout_id: int, db: Session = Depends(get_db)) -> list[Equipment]:
    statement = select(WorkoutEquipmentLink).where(WorkoutEquipmentLink.workout_id == workout_id)
    result = db.exec(statement).all()
    if not result:
        raise HTTPException(status_code=404, detail="Workout not found")
    equipment_ids = [link.equipment_id for link in result]
    statement = select(Equipment).where(Equipment.equipment_id.in_(equipment_ids))
    return db.exec(statement).all()

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
    link = WorkoutMuscleGroupLink(workout_id=workout_id, group_id=group_id)
    db.add(link)
    db.commit()

@app.post("/workouts/{workout_id}/equipment/{equipment_id}")
async def add_equipment_to_workout(workout_id: int, equipment_id: int, db: Session = Depends(get_db)) -> None:
    link = WorkoutEquipmentLink(workout_id=workout_id, equipment_id=equipment_id)
    db.add(link)
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