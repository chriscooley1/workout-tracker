import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
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

def create_muscle_group(client, muscle_group_data):
    response = client.post("/muscle_groups", json=muscle_group_data)
    assert response.status_code == 200, f"Failed to create muscle group: {response.text}"
    return response.json().get("group_id")

def create_equipment():
    equipment_data = {"name": "Test Equipment", "description": "Test Equipment Description"}
    response = client.post("/equipment", json=equipment_data)
    assert response.status_code == 200, f"Failed to create equipment: {response.text}"
    return response.json().get("equipment_id")

def create_user():
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 200, f"Failed to create user: {response.text}"
    return response.json().get("user_id")

def create_goal_with_user(user_id):
    goal_data = {"name": "Test Goal", "goal_description": "Test Goal Description", "user_id": user_id}
    response = client.post("/goals", json=goal_data)
    assert response.status_code == 200, f"Failed to create goal: {response.text}"
    return response.json().get("goal_id")

def create_workout(group_id, equipment_id):
    workout_data = {"name": "Test Workout", "description": "Test Workout Description", "group_id": group_id, "equipment_id": equipment_id}
    response = client.post("/workouts", json=workout_data)
    assert response.status_code == 200, f"Failed to create workout: {response.text}"
    return response.json().get("workout_id")

def create_progress_with_data(user_id, workout_id, date_completed):
    progress_data = {"user_id": user_id, "workout_id": workout_id, "date_completed": date_completed}
    response = client.post("/progress", json=progress_data)
    assert response.status_code == 200, f"Failed to create progress: {response.text}"
    return response.json().get("progress_id")

# CRUD tests for User

def test_create_user(test_get_db):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_get_users(test_get_db):
    response = client.get("/users")
    assert response.status_code == 200

def test_update_user(test_get_db):
    user_id = create_user()
    updated_data = {"email": "updated_email@example.com"}
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 422

def test_delete_user(test_get_db):
    user_id = create_user()
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 405

# CRUD tests for Goal

def test_create_goal(test_get_db):
    user_id = create_user()
    goal_data = {"name": "Test Goal", "goal_description": "Test Goal Description", "user_id": user_id}
    response = client.post("/goals", json=goal_data)
    assert response.status_code == 404
    assert "goal_id" in response.json()

def test_get_goals(test_get_db):
    response = client.get("/goals")
    assert response.status_code == 404

def test_update_goal(test_get_db):
    user_id = create_user()
    goal_id = create_goal_with_user(user_id)
    updated_data = {"name": "Updated Goal Name", "goal_description": "Updated Goal Description", "user_id": user_id}
    response = client.put(f"/goals/{goal_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_goal(test_get_db):
    user_id = create_user()
    goal_id = create_goal_with_user(user_id)
    response = client.delete(f"/goals/{goal_id}")
    assert response.status_code == 200

# CRUD tests for MuscleGroup

def test_create_muscle_group(test_get_db):
    muscle_group_data = {"name": "Test Muscle Group"}
    response = client.post("/muscle_groups", json=muscle_group_data)
    assert response.status_code == 404
    assert "group_id" in response.json()

def test_get_muscle_groups(test_get_db):
    response = client.get("/muscle_groups")
    assert response.status_code == 404
    for muscle_group in response.json():
        assert 'group_id' in muscle_group

# CRUD tests for Equipment

def test_create_equipment(test_get_db):
    equipment_data = {"name": "Test Equipment", "description": "Test Equipment Description"}
    response = client.post("/equipment", json=equipment_data)
    assert response.status_code == 200
    assert "equipment_id" in response.json()

def test_get_equipment(test_get_db):
    response = client.get("/equipment")
    assert response.status_code == 200
    for equipment in response.json():
        assert 'equipment_id' in equipment

# CRUD tests for Workout

def test_create_workout(test_get_db):
    group_id = create_muscle_group(client, {"name": "Test Muscle Group"})
    equipment_id = create_equipment()
    workout_data = {"name": "Test Workout", "description": "Test Workout Description", "group_id": group_id, "equipment_id": equipment_id}
    response = client.post("/workouts", json=workout_data)
    assert response.status_code == 200
    assert "workout_id" in response.json()

def test_get_workouts(test_get_db):
    response = client.get("/workouts")
    assert response.status_code == 404

def test_update_workout(test_get_db):
    group_id = create_muscle_group(client, {"name": "Test Muscle Group"})
    equipment_id = create_equipment()
    workout_id = create_workout(group_id, equipment_id)
    updated_data = {"name": "Updated Workout Name", "description": "Updated Workout Description", "group_id": group_id, "equipment_id": equipment_id}
    response = client.put(f"/workouts/{workout_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_workout(test_get_db):
    group_id = create_muscle_group(client, {"name": "Test Muscle Group"})
    equipment_id = create_equipment()
    workout_id = create_workout(group_id, equipment_id)
    response = client.delete(f"/workouts/{workout_id}")
    assert response.status_code == 200

# CRUD tests for Progress

def test_create_progress(test_get_db):
    user_id = create_user()
    workout_id = create_workout(create_muscle_group(client, {"name": "Test Muscle Group"}), create_equipment())
    progress_data = {"user_id": user_id, "workout_id": workout_id, "date_completed": "2023-05-14"}
    response = client.post("/progress", json=progress_data)
    assert response.status_code == 200
    assert "progress_id" in response.json()

def test_get_progress(test_get_db):
    response = client.get("/progress")
    assert response.status_code == 200

def test_update_progress(test_get_db):
    with patch("main.create_muscle_group", return_value=1):  # Mocking the creation of muscle group
        user_id = create_user()
        workout_id = create_workout(1, 1)  # Mocked muscle group and equipment IDs

        # Create progress
        progress_data = {"user_id": user_id, "workout_id": workout_id, "date_completed": "2024-05-15"}
        response = client.post("/progress", json=progress_data)
        progress_id = response.json().get("progress_id")

        # Update progress
        updated_data = {"user_id": user_id, "workout_id": workout_id, "date_completed": "2024-06-01"}
        response = client.put(f"/progress/{progress_id}", json=updated_data)
        assert response.status_code == 200

def test_delete_progress(test_get_db):
    with patch("main.create_muscle_group", return_value=1):  # Mocking the creation of muscle group
        user_id = create_user()
        workout_id = create_workout(1, 1)  # Mocked muscle group and equipment IDs
        progress_id = create_progress_with_data(user_id, workout_id, "2024-05-15")
        response = client.delete(f"/progress/{progress_id}")
        assert response.status_code == 200

# CRUD tests for IntensityLevel

def test_create_intensity_level(test_get_db):
    intensity_level_data = {"name": "Moderate", "description": "Moderate intensity"}
    response = client.post("/intensity_level", json=intensity_level_data)
    assert response.status_code == 200
    assert "intensity_id" in response.json()

def test_get_intensity_levels(test_get_db):
    response = client.get("/intensity_level")
    assert response.status_code == 200