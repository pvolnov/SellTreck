import unittest
from filecmp import cmp
from unittest import TestCase
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestPredictHandler(TestCase):
    test_user_id = 1

    def setUp(self):
        response = client.post("/user/", json={"login": "neafiol", "password": "1234", "name": "Petr"})
        self.assertNotIn('detail', response.json())
        self.test_user_id = response.json()["id"]

    def test_edit_user(self):
        response = client.put("/user/", json={"id": self.test_user_id, "name": "Petr Volnov"})
        self.assertNotIn('detail', response.json())

    def test_get_user(self):
        response = client.post("/user/auth/", json={"login": "neafiol", "password": "1234"})
        self.assertNotIn('detail', response.json())

    def tearDown(self):
        response = client.delete("/user/", params={"id": self.test_user_id})
        self.assertNotIn('detail', response.json())
