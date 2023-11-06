from fastapi import FastAPI, APIRouter, WebSocket
from ..app import ConnectionManager
import requests
import json
from ..db import chat_crud

router = APIRouter(
    prefix="/chat", 
    tags=["chat"],
    responses={404: {"description": "Not Found"}}
    )
manager = ConnectionManager()

@router.websocket("/communicate")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        pass 
    except WebSocketDisconnect:
     pass
