import os
from unittest import TestCase

from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestPredictHandler(TestCase):

    def test_get_itinerary_list(self):
        response = client.get("/itinerary/", params={"id": 12})
        self.assertNotIn('detail', response.json())
