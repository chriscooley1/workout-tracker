from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models import User, Goal, MuscleGroup, Equipment, Workout, Progress, IntensityLevel
from database import get_db
import sys


# Replace this with your PostgreSQL test database URL
SQLALCHEMY_TEST_DATABASE_URL = "postgresql://username:password@localhost/test_database"

# Creating a test database engine
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

# Creating a test database session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db function to use the test session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override get_db function to use the test session for tests
def override_get_test_db():
    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()

# Apply the appropriate override depending on whether it's a test or not
if "pytest" in sys.modules:
    app.dependency_overrides[get_db] = override_get_test_db
else:
    app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Create tables in the test database
def create_test_tables():
    with engine.connect() as connection:
        User.__table__.create(connection)
        Goal.__table__.create(connection)
        MuscleGroup.__table__.create(connection)
        Equipment.__table__.create(connection)
        Workout.__table__.create(connection)
        Progress.__table__.create(connection)
        IntensityLevel.__table__.create(connection)

# Cleanup function to delete test data from tables
def delete_test_data():
    with engine.connect() as connection:
        connection.execute('DELETE FROM users')
        connection.execute('DELETE FROM goals')
        connection.execute('DELETE FROM muscle_groups')
        connection.execute('DELETE FROM equipment')
        connection.execute('DELETE FROM workouts')
        connection.execute('DELETE FROM progress')
        connection.execute('DELETE FROM intensity_levels')

# Fixture to run setup and cleanup before and after tests
@pytest.fixture(autouse=True)
def setup_and_cleanup():
    create_test_tables()
    yield
    delete_test_data()

# Sample data for testing
sample_user = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

sample_goal = {
    "name": "Get Fit",
    "goal_description": "Achieve overall fitness"
}

# Unit tests
def test_create_user():
    response = client.post("/user", json=sample_user)
    assert response.status_code == 200

def test_get_users():
    response = client.get("/user")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_goal():
    response = client.post("/goal", json=sample_goal)
    assert response.status_code == 200

def test_get_goals():
    response = client.get("/goal")
    assert response.status_code == 200
    assert len(response.json()) > 0

# Add more tests for other endpoints as needed
