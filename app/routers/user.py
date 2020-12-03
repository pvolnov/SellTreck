from fastapi import APIRouter
from playhouse.shortcuts import model_to_dict

from app.data_models import BaseResponse, User, UserAuth
from app.models.users import Users

router = APIRouter()


@router.post("/", response_model=User)
async def create_user(user: User):
    # print(user.id)
    # if user.login is not None and user.password is not None:
    #     assert Users.get_or_none(Users.login == user.login) is None, "User with this login already exist" \
    #                                                                  ""
    # u = Users.create(name=user.name,
    #                  password=user.password, login=user.login)
    u = Users.get_by_id(user.id)
    return model_to_dict(u)


@router.patch("/", response_model=BaseResponse)
async def update_user(user: User):
    u = Users.get_by_id(user.id)
    if user.state:
        u.state = user.state
    u.save()
    return {"successful": True}


@router.delete("/", response_model=BaseResponse)
async def delete_user(id: int):
    Users.delete_by_id(id)
    return {"successful": True}


@router.get("/", response_model=User)
async def delete_user(user_id: int):
    u = Users.get_by_id(user_id)
    # print(model_to_dict(u))
    return model_to_dict(u)


@router.post("/auth/", response_model=User)
async def get_user(user: UserAuth):
    u = Users.get_or_none((Users.login == user.login) & (Users.password == user.password))
    assert user is not None, "User not found"
    return model_to_dict(u)