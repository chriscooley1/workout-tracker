from sqlalchemy import Column, Integer, String

from database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    set = Column(Integer)
    rep = Column(Integer)
    weight = Column(Integer)