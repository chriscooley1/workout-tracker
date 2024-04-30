from sqlmodel import Field, SQLModel, create_engine, Session
from decouple import config

from models import Workout

DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    with Session(engine) as session:
        workout = Workout(name="Bench", set=3, rep=3, weight=40)
        session.add(workout)
        session.commit()