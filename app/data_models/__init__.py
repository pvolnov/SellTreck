from typing import List, Dict, Tuple

from pydantic.main import BaseModel


class Search(BaseModel):
    id: int
    text: str


class Item(BaseModel):
    name: str
    count: int = 1
    bought: bool = False


class ItemsList(BaseModel):
    count: int
    items: List[Item]


class BaseResponse(BaseModel):
    successful: bool
    comment: str = None


class User(BaseModel):
    name: str = "New user"
    id: int = 0
    login: str = None
    password: str = None
    cart_list: List[Item] = []
    top_treks: List[dict] = []
    state: dict = {}


class UserAuth(BaseModel):
    login: str
    password: str
