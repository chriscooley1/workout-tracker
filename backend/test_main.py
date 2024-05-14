import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlmodel import Session
from main import app
from models import User

client = TestClient(app)

class TestUserEndpoints(unittest.TestCase):

    @patch('main.get_db')
    def test_get_users(self, mock_get_db):
        # Mock the database session and the query
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_users = []
        mock_db.exec.return_value.all.return_value = mock_users

        response = client.get("/user")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('main.get_db')
    def test_create_user(self, mock_get_db):
        # Mock the database session
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db

        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        response = client.post("/user", json=user_data)
        self.assertEqual(response.status_code, 200)

        # Ensure the user was added to the database
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_update_user(self, mock_get_db):
        # Mock the database session and the get method
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_user = User(user_id=1, username="testuser", email="test@example.com", password="password123")
        mock_db.get.return_value = mock_user

        user_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "password": "newpassword123"
        }
        response = client.put("/user/1", json=user_data)
        self.assertEqual(response.status_code, 200)

        # Ensure the user was updated in the database
        self.assertEqual(mock_user.username, "updateduser")
        self.assertEqual(mock_user.email, "updated@example.com")
        self.assertEqual(mock_user.password, "newpassword123")
        mock_db.commit.assert_called_once()

    @patch('main.get_db')
    def test_delete_user(self, mock_get_db):
        # Mock the database session and the get method
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value = mock_db
        mock_user = User(user_id=1, username="testuser", email="test@example.com", password="password123")
        mock_db.get.return_value = mock_user

        response = client.delete("/user/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User deleted successfully"})

        # Ensure the user was deleted from the database
        mock_db.delete.assert_called_once_with(mock_user)
        mock_db.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
