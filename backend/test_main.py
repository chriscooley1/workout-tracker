import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlmodel import Session
from main import app
from models import User, Goal, MuscleGroup, Equipment, Workout, Progress, IntensityLevel

client = TestClient(app)

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        self.updated_user_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "password": "newpassword123"
        }

    @patch('main.get_db')
    def test_get_users(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_users = []
        mock_db.exec.return_value.all.return_value = mock_users

        response = client.get("/user")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('main.get_db')
    def test_create_user(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db

        response = client.post("/user", json=self.user_data)
        self.assertEqual(response.status_code, 200)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_user(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_user = User(user_id=1, **self.user_data)
        mock_db.get.return_value = mock_user

        response = client.put("/user/1", json=self.updated_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_user.username, self.updated_user_data["username"])
        self.assertEqual(mock_user.email, self.updated_user_data["email"])
        self.assertEqual(mock_user.password, self.updated_user_data["password"])
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_delete_user(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_user = User(user_id=1, **self.user_data)
        mock_db.get.return_value = mock_user

        response = client.delete("/user/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User deleted successfully"})

        mock_db.delete.assert_called_once_with(mock_user)
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_nonexistent_user(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_db.get.return_value = None

        response = client.put("/user/99", json=self.updated_user_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})

    @patch('main.get_db')
    def test_delete_nonexistent_user(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_db.get.return_value = None

        response = client.delete("/user/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})

class TestGoalEndpoints(unittest.TestCase):
    def setUp(self):
        self.goal_data = {
            "name": "testname",
            "goal_description": "goal_description123"
        }
        self.updated_goal_data = {
            "name": "updatedname",
            "goal_description": "newgoal_description123"
        }

    @patch('main.get_db')
    def test_get_goals(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_goals = []
        mock_db.exec.return_value.all.return_value = mock_goals

        response = client.get("/goal")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('main.get_db')
    def test_create_goal(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db

        response = client.post("/goal", json=self.goal_data)
        self.assertEqual(response.status_code, 200)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_goal(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_goal = Goal(goal_id=1, **self.goal_data)
        mock_db.get.return_value = mock_goal

        response = client.put("/goal/1", json=self.updated_goal_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_goal.name, self.updated_goal_data["name"])
        self.assertEqual(mock_goal.goal_description, self.updated_goal_data["goal_description"])
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_delete_goal(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_goal = Goal(goal_id=1, **self.goal_data)
        mock_db.get.return_value = mock_goal

        response = client.delete("/goal/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Goal deleted successfully"})

        mock_db.delete.assert_called_once_with(mock_goal)
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_nonexistent_goal(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_db.get.return_value = None

        response = client.put("/goal/99", json=self.updated_goal_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Goal not found"})

    @patch('main.get_db')
    def test_delete_nonexistent_goal(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_db.get.return_value = None

        response = client.delete("/goal/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Goal not found"})

class TestMuscleGroupEndpoints(unittest.TestCase):
    def setUp(self):
        self.muscle_group_data = {
            "name": "testname"
        }
        self.updated_muscle_group_data = {
            "name": "updatedname"
        }

    @patch('main.get_db')
    def test_get_muscle_groups(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_muscle_groups = []
        mock_db.exec.return_value.all.return_value = mock_muscle_groups

        response = client.get("/muscle_group")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('main.get_db')
    def test_create_muscle_group(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db

        response = client.post("/muscle_group", json=self.muscle_group_data)
        self.assertEqual(response.status_code, 200)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_muscle_group(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_muscle_group = MuscleGroup(group_id=1, **self.muscle_group_data)
        mock_db.get.return_value = mock_muscle_group

        response = client.put("/muscle_group/1", json=self.updated_muscle_group_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_muscle_group.name, self.updated_muscle_group_data["name"])
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_delete_muscle_group(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_muscle_group = MuscleGroup(group_id=1, **self.muscle_group_data)
        mock_db.get.return_value = mock_muscle_group

        response = client.delete("/muscle_group/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Muscle group deleted successfully"})

        mock_db.delete.assert_called_once_with(mock_muscle_group)
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_nonexistent_muscle_group(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_db.get.return_value = None

        response = client.put("/muscle_group/99", json=self.updated_muscle_group_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Muscle group not found"})

    @patch('main.get_db')
    def test_delete_nonexistent_muscle_group(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_db.get.return_value = None

        response = client.delete("/muscle_group/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Muscle group not found"})

class TestEquipmentEndpoints(unittest.TestCase):
    def setUp(self):
        self.equipment_data = {
            "name": "testname",
            "description": "description123"
        }
        self.updated_equipment_data = {
            "name": "updatedname",
            "description": "newdescription123"
        }

    @patch('main.get_db')
    def test_get_equipment(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_equipment = []
        mock_db.exec.return_value.all.return_value = mock_equipment

        response = client.get("/equipment")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('main.get_db')
    def test_create_equipment(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db

        response = client.post("/equipment", json=self.equipment_data)
        self.assertEqual(response.status_code, 200)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_equipment(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_equipment = Equipment(equipment_id=1, **self.equipment_data)
        mock_db.get.return_value = mock_equipment

        response = client.put("/equipment/1", json=self.updated_equipment_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_equipment.name, self.updated_equipment_data["name"])
        self.assertEqual(mock_equipment.description, self.updated_equipment_data["description"])
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_delete_equipment(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_equipment = Equipment(equipment_id=1, **self.equipment_data)
        mock_db.get.return_value = mock_equipment

        response = client.delete("/equipment/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Equipment deleted successfully"})

        mock_db.delete.assert_called_once_with(mock_equipment)
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_nonexistent_equipment(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_db.get.return_value = None

        response = client.put("/equipment/99", json=self.updated_equipment_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Equipment not found"})

    @patch('main.get_db')
    def test_delete_nonexistent_equipment(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_db.get.return_value = None

        response = client.delete("/equipment/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Equipment not found"})

class TestWorkoutEndpoints(unittest.TestCase):
    def setUp(self):
        self.workout_data = {
            "name": "testworkout",
            "description": "workout description",
            "user_id": 1
        }
        self.updated_workout_data = {
            "name": "updatedworkout",
            "description": "new workout description",
            "user_id": 1
        }

    @patch('main.get_db')
    def test_get_workouts(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_workouts = []
        mock_db.exec.return_value.all.return_value = mock_workouts

        response = client.get("/workout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('main.get_db')
    def test_create_workout(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db

        response = client.post("/workout", json=self.workout_data)
        self.assertEqual(response.status_code, 200)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_workout(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_workout = Workout(workout_id=1, **self.workout_data)
        mock_db.get.return_value = mock_workout

        response = client.put("/workout/1", json=self.updated_workout_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_workout.name, self.updated_workout_data["name"])
        self.assertEqual(mock_workout.description, self.updated_workout_data["description"])
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_delete_workout(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_workout = Workout(workout_id=1, **self.workout_data)
        mock_db.get.return_value = mock_workout

        response = client.delete("/workout/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Workout deleted successfully"})

        mock_db.delete.assert_called_once_with(mock_workout)
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_nonexistent_workout(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_db.get.return_value = None

        response = client.put("/workout/99", json=self.updated_workout_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Workout not found"})

    @patch('main.get_db')
    def test_delete_nonexistent_workout(self, mock_get_db):
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_db.get.return_value = None

        response = client.delete("/workout/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Workout not found"})

class TestProgressEndpoints(unittest.TestCase):
    @patch('main.get_db')
    def test_get_progress(self, mock_get_db):
        # Mock the database session and the query
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_progress = []
        mock_db.exec.return_value.all.return_value = mock_progress

        response = client.get("/progress")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('main.get_db')
    def test_create_progress(self, mock_get_db):
        # Mock the database session
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db

        progress_data = {
            "user_id": 1,
            "workout_id": 1,
            "date_completed": "2024-01-01"
        }
        response = client.post("/progress", json=progress_data)
        self.assertEqual(response.status_code, 200)

        # Ensure the progress was added to the database
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_progress(self, mock_get_db):
        # Mock the database session and the get method
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_progress = Progress(progress_id=1, user_id=1, workout_id=1, date_completed="2024-01-01")
        mock_db.get.return_value = mock_progress

        progress_data = {
            "user_id": 1,
            "workout_id": 1,
            "date_completed": "2024-02-01"
        }
        response = client.put("/progress/1", json=progress_data)
        self.assertEqual(response.status_code, 200)

        # Ensure the progress was updated in the database
        self.assertEqual(mock_progress.date_completed, "2024-02-01")
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_delete_progress(self, mock_get_db):
        # Mock the database session and the get method
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_progress = Progress(progress_id=1, user_id=1, workout_id=1, date_completed="2024-01-01")
        mock_db.get.return_value = mock_progress

        response = client.delete("/progress/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Progress deleted successfully"})

        # Ensure the progress was deleted from the database
        mock_db.delete.assert_called_once_with(mock_progress)
        mock_db.commit.assert_called_once()

class TestIntensityLevelEndpoints(unittest.TestCase):
    @patch('main.get_db')
    def test_get_intensity_levels(self, mock_get_db):
        # Mock the database session and the query
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_intensity_levels = []
        mock_db.exec.return_value.all.return_value = mock_intensity_levels

        response = client.get("/intensity_level")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('main.get_db')
    def test_create_intensity_level(self, mock_get_db):
        # Mock the database session
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db

        intensity_level_data = {
            "name": "High",
            "description": "High intensity level"
        }
        response = client.post("/intensity_level", json=intensity_level_data)
        self.assertEqual(response.status_code, 200)

        # Ensure the intensity level was added to the database
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_intensity_level(self, mock_get_db):
        # Mock the database session and the get method
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_intensity_level = IntensityLevel(intensity_id=1, name="High", description="High intensity level")
        mock_db.get.return_value = mock_intensity_level

        intensity_level_data = {
            "name": "Moderate",
            "description": "Moderate intensity level"
        }
        response = client.put("/intensity_level/1", json=intensity_level_data)
        self.assertEqual(response.status_code, 200)

        # Ensure the intensity level was updated in the database
        self.assertEqual(mock_intensity_level.name, "Moderate")
        self.assertEqual(mock_intensity_level.description, "Moderate intensity level")
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_delete_intensity_level(self, mock_get_db):
        # Mock the database session and the get method
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_intensity_level = IntensityLevel(intensity_id=1, name="High", description="High intensity level")
        mock_db.get.return_value = mock_intensity_level

        response = client.delete("/intensity_level/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Intensity Level deleted successfully"})

        # Ensure the intensity level was deleted from the database
        mock_db.delete.assert_called_once_with(mock_intensity_level)
        mock_db.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
