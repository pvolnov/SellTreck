import uvicorn
from fastapi import FastAPI

from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# uvicorn app.main:app --host 0.0.0.0 --port 8080