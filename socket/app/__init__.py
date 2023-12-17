from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
import config
import app.metadata as metadatas
import json
from app.tools.socket import socket
from app.participant.routes import ParticipantRoute
# from app.tools.database import engine

app = FastAPI(openapi_tags=metadatas.tags_metadata)
app_socket = socket
configuration = config


@app.websocket("/socket/{index_id}")
async def socket_participant(websocket: WebSocket, index_id: int):
    """
    Websocket for extracting
    """
    await app_socket.connect(websocket, index_id)
    try:
        while True:
            data = await websocket.receive_text()
            data_obj = json.loads(data)
            await websocket.send_text(json.dumps(data_obj))
            
    except WebSocketDisconnect:
        app_socket.disconnect(websocket, index_id)

app.include_router(ParticipantRoute)