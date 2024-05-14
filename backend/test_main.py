from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

class MockSession:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

def mock_get_db():
    return MockSession()

@pytest.fixture
def test_get_db():
    with patch("database.get_db", return_value=mock_get_db()) as mock:
        yield mock

# CRUD tests for User

def test_create_user(test_get_db):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    response = client.post("/user", json=user_data)
    assert response.status_code == 200

def test_get_users(test_get_db): 
    response = client.get("/user")
    assert response.status_code == 200

def test_update_user(test_get_db):
    user_id = 1
    updated_data = {"email": "updated_email@example.com"}
    response = client.put(f"/user/{user_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_user(test_get_db):
    user_id = 1
    response = client.delete(f"/user/{user_id}")
    assert response.status_code == 200

# CRUD tests for Goal

def test_create_goal(test_get_db):
    goal_data = {"name": "Test Goal", "goal_description": "Test Goal Description", "user_id": 1}
    response = client.post("/goal", json=goal_data)
    assert response.status_code == 200

def test_get_goals(test_get_db):
    response = client.get("/goal")
    assert response.status_code == 200

def test_update_goal(test_get_db):
    goal_id = 1
    updated_data = {"name": "Updated Goal Name"}
    response = client.put(f"/goal/{goal_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_goal(test_get_db):
    goal_id = 1
    response = client.delete(f"/goal/{goal_id}")
    assert response.status_code == 200

# CRUD tests for MuscleGroup

def test_create_muscle_group(test_get_db):
    muscle_group_data = {"name": "Test Muscle Group"}
    response = client.post("/muscle_group", json=muscle_group_data)
    assert response.status_code == 200

def test_get_muscle_groups(test_get_db):
    response = client.get("/muscle_group")
    assert response.status_code == 200

def test_update_muscle_group(test_get_db):
    group_id = 1
    updated_data = {"name": "Updated Muscle Group Name"}
    response = client.put(f"/muscle_group/{group_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_muscle_group(test_get_db):
    group_id = 1
    response = client.delete(f"/muscle_group/{group_id}")
    assert response.status_code == 200

# CRUD tests for Equipment

def test_create_equipment(test_get_db):
    equipment_data = {"name": "Test Equipment", "description": "Test Equipment Description"}
    response = client.post("/equipment", json=equipment_data)
    assert response.status_code == 200

def test_get_equipment(test_get_db):
    response = client.get("/equipment")
    assert response.status_code == 200

def test_update_equipment(test_get_db):
    equipment_id = 1
    updated_data = {"name": "Updated Equipment Name"}
    response = client.put(f"/equipment/{equipment_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_equipment(test_get_db):
    equipment_id = 1
    response = client.delete(f"/equipment/{equipment_id}")
    assert response.status_code == 200

# CRUD tests for Workout

def test_create_workout(test_get_db):
    workout_data = {"name": "Test Workout", "description": "Test Workout Description", "group_id": 1, "equipment_id": 1}
    response = client.post("/workout", json=workout_data)
    assert response.status_code == 200

def test_get_workouts(test_get_db):
    response = client.get("/workout")
    assert response.status_code == 200

def test_update_workout(test_get_db):
    workout_id = 1
    updated_data = {"name": "Updated Workout Name"}
    response = client.put(f"/workout/{workout_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_workout(test_get_db):
    workout_id = 1
    response = client.delete(f"/workout/{workout_id}")
    assert response.status_code == 200

# CRUD tests for Progress

def test_create_progress(test_get_db):
    # Create related User and Workout
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    user_response = client.post("/user", json=user_data)
    assert user_response.status_code == 200
    user_id = user_response.json()["user_id"]
    
    workout_data = {"name": "Test Workout", "description": "Test Workout Description", "group_id": 1, "equipment_id": 1}
    workout_response = client.post("/workout", json=workout_data)
    assert workout_response.status_code == 200
    workout_id = workout_response.json()["workout_id"]

    progress_data = {"user_id": user_id, "workout_id": workout_id, "date_completed": "2024-05-15"}
    response = client.post("/progress", json=progress_data)
    assert response.status_code == 200

def test_get_progress(test_get_db):
    response = client.get("/progress")
    assert response.status_code == 200

def test_update_progress(test_get_db):
    # Create related User and Workout
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    user_response = client.post("/user", json=user_data)
    assert user_response.status_code == 200
    user_id = user_response.json()["user_id"]
    
    workout_data = {"name": "Test Workout", "description": "Test Workout Description", "group_id": 1, "equipment_id": 1}
    workout_response = client.post("/workout", json=workout_data)
    assert workout_response.status_code == 200
    workout_id = workout_response.json()["workout_id"]

    progress_data = {"user_id": user_id, "workout_id": workout_id, "date_completed": "2024-05-15"}
    progress_response = client.post("/progress", json=progress_data)
    assert progress_response.status_code == 200
    progress_id = progress_response.json()["progress_id"]

    updated_data = {"date_completed": "2024-05-16"}
    response = client.put(f"/progress/{progress_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_progress(test_get_db):
    # Create related User and Workout
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    user_response = client.post("/user", json=user_data)
    assert user_response.status_code == 200
    user_id = user_response.json()["user_id"]
    
    workout_data = {"name": "Test Workout", "description": "Test Workout Description", "group_id": 1, "equipment_id": 1}
    workout_response = client.post("/workout", json=workout_data)
    assert workout_response.status_code == 200
    workout_id = workout_response.json()["workout_id"]

    progress_data = {"user_id": user_id, "workout_id": workout_id, "date_completed": "2024-05-15"}
    progress_response = client.post("/progress", json=progress_data)
    assert progress_response.status_code == 200
    progress_id = progress_response.json()["progress_id"]

    response = client.delete(f"/progress/{progress_id}")
    assert response.status_code == 200

    # Verify it was deleted
    response = client.get(f"/progress/{progress_id}")
    assert response.status_code == 404

# CRUD tests for IntensityLevel

def test_create_intensity_level(test_get_db):
    intensity_level_data = {"name": "Test Intensity", "description": "Test Intensity Description"}
    response = client.post("/intensity_level", json=intensity_level_data)
    assert response.status_code == 200
    assert "intensity_id" in response.json()  # Ensure the response contains the ID

def test_get_intensity_levels(test_get_db):
    response = client.get("/intensity_level")
    assert response.status_code == 200  

def test_update_intensity_level(test_get_db):
    # First, create an intensity level to ensure it exists
    intensity_level_data = {"name": "Test Intensity", "description": "Test Intensity Description"}
    response = client.post("/intensity_level", json=intensity_level_data)
    assert response.status_code == 200
    intensity_id = response.json()["intensity_id"]

    # Now update the intensity level
    updated_data = {"name": "Updated Intensity Level Name"}
    response = client.put(f"/intensity_level/{intensity_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_intensity_level(test_get_db):
    # First, create an intensity level to ensure it exists
    intensity_level_data = {"name": "Test Intensity", "description": "Test Intensity Description"}
    response = client.post("/intensity_level", json=intensity_level_data)
    assert response.status_code == 200
    intensity_id = response.json()["intensity_id"]

    # Now delete the intensity level
    response = client.delete(f"/intensity_level/{intensity_id}")
    assert response.status_code == 200

    # Verify it was deleted
    response = client.get(f"/intensity_level/{intensity_id}")
    assert response.status_code == 405