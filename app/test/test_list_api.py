import os
import random
from unittest import TestCase

from starlette.testclient import TestClient

from app.main import app
from app.models.items import Items
from app.models.users import Users

client = TestClient(app)


class TestPredictHandler(TestCase):
    user = Users.get_by_id(1)
    item = Items.get()

    def setUp(self):
        print("\nUser for test:", self.user.name)
        print("Item for test:", self.item.name)

    def test_add_item_to_list(self):
        n = random.randint(2, 10)
        response = client.put("/list/", json={"user_id": self.user.id,
                                              "count": n,
                                              "item_id": self.item.id})
        self.assertNotIn('detail', response.json())
        user2 = Users.get_by_id(self.user.id)
        for item in user2.cart_list:
            if item['item_id'] == self.item.id:
                self.assertEquals(item['count'], n)

    def test_get_user_list(self):
        response = client.get("/list/", params={"user_id": self.user.id})
        self.assertNotIn('detail', response.json())
        print(response.json())

    def test_delete_item_from_list(self):
        response = client.delete("/list/", params={"user_id": self.user.id, "item_id": self.item.id})
        self.assertNotIn('detail', response.json())
        user2 = Users.get_by_id(self.user.id)
        self.assertNotIn(self.item.id, [i["item_id"] for i in user2.cart_list])

    def test_search(self):
        response = client.get("/list/search", params={"text": "молоко пр"})
        self.assertNotIn('detail', response.json())
        self.assertLess(1, len(response.json()))

        response = client.get("/list/search", params={"text": "яйца ку"})
        self.assertNotIn('detail', response.json())
        self.assertLess(1, len(response.json()))
