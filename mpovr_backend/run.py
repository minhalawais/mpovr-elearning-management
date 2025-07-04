import uvicorn
from app.routes import router
from app.database import engine
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware
from app.websocket_handler import websocket_endpoint
from fastapi import FastAPI, Depends, WebSocket
from app.database import get_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # Allow requests from React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

