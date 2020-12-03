from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import list, user, itinerary

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def main_page():
    return "Server is ranning v 1.0"


app.include_router(list.router)
app.include_router(
    list.router,
    prefix="/list",
    responses={404: {"description": "Not found"}})

app.include_router(
    user.router,
    prefix="/user",
    responses={404: {"description": "Not found"}},
)
app.include_router(
    itinerary.router,
    prefix="/itinerary",
    responses={404: {"description": "Not found"}},
)
