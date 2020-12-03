from typing import List, Optional

import grequests
from fastapi import APIRouter, Depends
from pydantic.main import BaseModel

from app.data_models import BaseResponse, ItemsList
from app.streck import dictionary
from app.models.items import Items
from app.models.users import Users

router = APIRouter()


class ListRequest(BaseModel):
    user_id: int
    name: str
    count: int = 1


class UpdateCartRequest(BaseModel):
    user_id: int
    cart_id: int
    type: str


@router.patch("/update", response_model=BaseResponse)
async def purchased_item(req: UpdateCartRequest):
    if req.type == "purchased":
        user = Users.get_by_id(req.user_id)
        if "bought" in user.cart_list[req.cart_id]:
            user.cart_list[req.cart_id]['bought'] ^= 1
        else:
            user.cart_list[req.cart_id]['bought'] = True

        user.save()
        return {"successful": True}

    return {"successful": False}


@router.patch("/", response_model=BaseResponse)
async def add_item_to_list(req: ListRequest):
    user = Users.get_by_id(req.user_id)
    for it in user.cart_list:
        if it["name"] == req.name:
            it["count"] = req.count
            user.save()
            return {"successful": True}

    user.cart_list.append({
        "count": 1,
        "name": req.name,
        "bought":False
    })
    user.save()
    return {"successful": True, "comment": req.name}


@router.delete("/", response_model=BaseResponse)
async def delete_item_from_list(user_id: int, cart_id: int):
    user = Users.get_by_id(user_id)
    del user.cart_list[cart_id]
    user.save()

    return {"successful": True}


@router.get("/", response_model=ItemsList)
async def get_list_of_items(user_id: int) -> ItemsList:
    user = Users.get_by_id(user_id)
    return ItemsList(**{
        "count": 12,
        "items": user.cart_list
    })


@router.get("/search")
async def search(text: str) -> List[dict]:
    """
    Get list of items with similar names.
    """
    # options = dictionary.get_similiar_words(text)
    # res = []
    # for o in options:
    #     res.append(" ".join(text.split(" ")[:-1]) + " " + o)
    print(text)
    r = grequests.get("https://sbermarket.ru/api/stores/70/search_suggestions",
                      params={
                          "q": text
                      })
    res = grequests.map([r])[0].json()["suggestion"]["offers"]
    res = [{
        "price": i["instamart_price"],
        "name": i["product"]['name'],
        "img": i["product"]['images'][0]['mini_url'],
    } for i in res]

    return res
