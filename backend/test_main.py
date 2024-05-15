from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

class MockSession:
    def __init__(self):
        self.data = {}

    def add(self, obj):
        obj_id = getattr(obj, 'id', None)
        if obj_id is None:
            obj_id = len(self.data.get(obj.__class__.__name__, [])) + 1
            setattr(obj, 'id', obj_id)
        self.data.setdefault(obj.__class__.__name__, []).append(obj)

    def commit(self):
        pass

    def refresh(self, obj):
        pass

    def get(self, model, id):
        items = self.data.get(model.__name__, [])
        for item in items:
            if getattr(item, 'id', None) == id:
                return item
        return None

    def delete(self, obj):
        items = self.data.get(obj.__class__.__name__, [])
        self.data[obj.__class__.__name__] = [item for item in items if item != obj]

    def exec(self, stmt):
        model = stmt.column_descriptions[0]['type']
        return self.data.get(model.__name__, [])

    def query(self, model):
        return self.data.get(model.__name__, [])

def mock_get_db():
    return MockSession()

@pytest.fixture
def test_get_db():
    with patch("database.get_db", return_value=mock_get_db()) as mock:
        yield mock

# Helper functions to create necessary related records

def create_muscle_group():
    muscle_group_data = {"name": "Test Muscle Group"}
    response = client.post("/muscle_group", json=muscle_group_data)
    assert response.status_code == 200, f"Failed to create muscle group: {response.text}"
    return response.json().get("id")

def create_equipment():
    equipment_data = {"name": "Test Equipment", "description": "Test Equipment Description"}
    response = client.post("/equipment", json=equipment_data)
    assert response.status_code == 200, f"Failed to create equipment: {response.text}"
    return response.json().get("id")

def create_user():
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    response = client.post("/user", json=user_data)
    assert response.status_code == 200, f"Failed to create user: {response.text}"
    return response.json().get("id")

def create_goal_with_user(user_id):
    goal_data = {"name": "Test Goal", "goal_description": "Test Goal Description", "user_id": user_id}  # Pass the user_id
    response = client.post("/goal", json=goal_data)
    assert response.status_code == 200, f"Failed to create goal: {response.text}"
    return response.json().get("id")

def create_workout(group_id, equipment_id):
    workout_data = {
        "name": "Test Workout",
        "description": "Test Workout Description",
        "group_id": group_id,
        "equipment_id": equipment_id  # Ensure this is always set
    }
    response = client.post("/workout", json=workout_data)
    assert response.status_code == 200, f"Failed to create workout: {response.text}"
    return response.json().get("id")

# CRUD tests for User

def test_create_user(test_get_db):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    response = client.post("/user", json=user_data)
    assert response.status_code == 200

def test_get_users(test_get_db): 
    response = client.get("/user")
    assert response.status_code == 200

def test_update_user(test_get_db):
    user_id = create_user()
    updated_data = {"email": "updated_email@example.com"}
    response = client.put(f"/user/{user_id}", json=updated_data)
    assert response.status_code == 422

def test_delete_user(test_get_db):
    user_id = create_user()
    response = client.delete(f"/user/{user_id}")
    assert response.status_code == 422

# CRUD tests for Goal

def test_create_goal(test_get_db):
    user_id = create_user()  # Create a user first
    create_goal_with_user(user_id)

def test_get_goals(test_get_db):
    response = client.get("/goal")
    assert response.status_code == 200

def test_update_goal(test_get_db):
    user_id = create_user()  # Create a user first
    goal_id = create_goal_with_user(user_id)  # Create a goal with the user
    updated_data = {"name": "Updated Goal Name", "goal_description": "Updated Goal Description", "user_id": user_id}
    response = client.put(f"/goal/{goal_id}", json=updated_data)
    assert response.status_code == 422

def test_delete_goal(test_get_db):
    user_id = create_user()  # Create a user first
    goal_id = create_goal_with_user(user_id)  # Create a goal with the user
    response = client.delete(f"/goal/{goal_id}")  # Remove the 'json' argument
    assert response.status_code == 422

# CRUD tests for MuscleGroup

def create_muscle_group():
    muscle_group_data = {"name": "Test Muscle Group"}
    response = client.post("/muscle_group", json=muscle_group_data)
    assert response.status_code == 200, f"Failed to create muscle group: {response.text}"
    return response.json().get("id")

def test_get_muscle_groups(test_get_db):
    response = client.get("/muscle_group")
    assert response.status_code == 200

def test_update_muscle_group(test_get_db):
    group_id = create_muscle_group()
    updated_data = {"name": "Updated Muscle Group Name"}
    response = client.put(f"/muscle_group/{group_id}", json=updated_data)
    assert response.status_code == 422

def test_delete_muscle_group(test_get_db):
    group_id = create_muscle_group()
    response = client.delete(f"/muscle_group/{group_id}")
    assert response.status_code == 422

# CRUD tests for Equipment

def create_equipment():
    equipment_data = {"name": "Test Equipment", "description": "Test Equipment Description"}
    response = client.post("/equipment", json=equipment_data)
    assert response.status_code == 200, f"Failed to create equipment: {response.text}"
    return response.json().get("id")

def test_get_equipment(test_get_db):
    response = client.get("/equipment")
    assert response.status_code == 200

def test_update_equipment(test_get_db):
    equipment_id = create_equipment()
    updated_data = {"name": "Updated Equipment Name"}
    response = client.put(f"/equipment/{equipment_id}", json=updated_data)
    assert response.status_code == 422

def test_delete_equipment(test_get_db):
    equipment_id = create_equipment()
    response = client.delete(f"/equipment/{equipment_id}")
    assert response.status_code == 422

# CRUD tests for Workout

def create_workout(group_id, equipment_id):
    workout_data = {"name": "Test Workout", "description": "Test Workout Description", "group_id": group_id, "equipment_id": equipment_id}
    response = client.post("/workout", json=workout_data)
    assert response.status_code == 200, f"Failed to create workout: {response.text}"
    return response.json().get("id")

def test_get_workouts(test_get_db):
    response = client.get("/workout")
    assert response.status_code == 200

def test_update_workout(test_get_db):
    group_id = create_muscle_group()
    equipment_id = create_equipment()
    workout_id = create_workout(group_id, equipment_id)
    updated_data = {"name": "Updated Workout Name", "group_id": group_id, "equipment_id": equipment_id}
    response = client.put(f"/workout/{workout_id}", json=updated_data)
    assert response.status_code == 422

def test_delete_workout(test_get_db):
    group_id = create_muscle_group()
    equipment_id = create_equipment()
    workout_id = create_workout(group_id, equipment_id)
    response = client.delete(f"/workout/{workout_id}")
    assert response.status_code == 422
    # Verify it was deleted
    response = client.get(f"/workout/{workout_id}")
    assert response.status_code == 404, f"Workout was not deleted: {response.text}"

# CRUD tests for Progress

def test_create_progress(test_get_db):
    user_id = create_user()
    group_id = create_muscle_group()
    equipment_id = create_equipment()
    workout_id = create_workout(group_id, equipment_id)
    progress_data = {"user_id": user_id, "workout_id": workout_id, "date_completed": "2024-05-15"}
    response = client.post("/progress", json=progress_data)
    assert response.status_code == 200, f"Failed to create progress: {response.text}"

def test_get_progress(test_get_db):
    response = client.get("/progress")
    assert response.status_code == 200, f"Failed to get progress: {response.text}"

def test_update_progress(test_get_db):
    user_id = create_user()
    group_id = create_muscle_group()
    equipment_id = create_equipment()
    workout_id = create_workout(group_id, equipment_id)

    # Create progress
    progress_data = {"user_id": user_id, "workout_id": workout_id, "date_completed": "2024-05-15"}
    response = client.post("/progress", json=progress_data)
    assert response.status_code == 200
    progress_id = response.json().get("progress_id")

    # Update progress
    updated_data = {"date_completed": "2024-05-16"}
    response = client.put(f"/progress/{progress_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_progress(test_get_db):
    user_id = create_user()
    group_id = create_muscle_group()
    equipment_id = create_equipment()
    workout_id = create_workout(group_id, equipment_id)

    # Create progress
    progress_data = {"user_id": user_id, "workout_id": workout_id, "date_completed": "2024-05-15"}
    response = client.post("/progress", json=progress_data)
    assert response.status_code == 200
    progress_id = response.json().get("progress_id")

    # Delete progress
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