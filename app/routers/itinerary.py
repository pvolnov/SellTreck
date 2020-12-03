from typing import List, Tuple, Dict

from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel

from app.data_models import BaseResponse, ItemsList, User
from app.streck.TrekNavigator import TrekNavigator
from app.models.users import Users

router = APIRouter()


class GenerateRequest(BaseModel):
    user_id: int


class Trek(BaseModel):
    """
    keypoints: list of pair (latitude, longitude)
    """
    price: float
    duration: float
    yandex_url: str = ""
    keypoints: List[Tuple[float, float]]
    cart_by_stores: List[dict]


@router.get("/", response_model=List[Trek])
async def generate_treks_for_user(user_id: int):
    """
    returns multiple route options between stores that contain products from the list
    """
    user = Users.get_by_id(user_id)

    return user.top_treks


@router.post("/init", response_model=List[Trek])
async def generate_treks_for_user(req: GenerateRequest):
    """
    generate multiple route options between stores that contain products from the list
    """
    user = Users.get_by_id(req.user_id)
    st = (59.964446, 30.310948)
    treks = TrekNavigator().generate_traks_for_cart(st, user.cart_list)
    for t in treks:
        t['quality'] = t['price'] + t['duration'] * 2

    treks = sorted(treks, key=lambda x: x['quality'])[:4]
    result = []
    prices = []
    for t in treks:
        if t['price'] not in prices:
            prices.append(t['price'])
            result.append(t)

    user.top_treks = result
    user.save()

    return result
