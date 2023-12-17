from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
import json
import http.client
from fastapi import Response
from app.tools.background import app_background
from app.participant.models import ParticipantModel
from app.participant.helpers import ParticipantHelper

ParticipantRoute = APIRouter()

@ParticipantRoute.post('/checkin', tags=['Trains'])
def participant_checkin(request: Request, object: ParticipantModel, background_tasks: app_background):
    '''Preparation for document to training'''
    try:
        param = {}
        param['id'] = object.id
        param['name'] = object.name
        param['institution'] = object.institution
        
        participant_helper = ParticipantHelper(**param)
        background_tasks.add_task(participant_helper.sent_to_socket)
            
        return Response(
            content=json.dumps(str("Sended")),
            status_code=http.client.OK,
            media_type='application/json'
        )
        
    except Exception as e:
        return Response(
            content=json.dumps(str(e)),
            status_code=http.client.INTERNAL_SERVER_ERROR,
            media_type='application/json'
        )