
from app.tools.socket import socket
app_socket = socket
import json

class ParticipantHelper:
    def __init__(self, id, name, institution):
        self.id = id
        self.name = name
        self.institution = institution

    def get_specific_socket(self):
        data_socket = app_socket.active_connections
        for socket in data_socket:
            if socket['id'] == self.id:
                return socket

    async def sent_to_socket(self):
        data_socket = self.get_specific_socket()
        await data_socket['socket'].send_text(json.dumps({
            "name": self.name,
            "institution": self.institution
        }))
        return {
            "success": True,
            "message": "success sent to socket"
        }