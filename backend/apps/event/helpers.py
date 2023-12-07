from apps.event.models import (
    Event,
    EventRegistration,
)
from apps.event.schemas import (
    EventSchema,
    EventRegistrationSchema
)
import os
import pandas as pd
import segno
from dotenv import load_dotenv
load_dotenv()

class EventHelpers:
    def __init__(
        self,
        api=None,
        method=None,
    ):
        self.api = api
        self.method = method

    # def list(self, values: dict):
    #     ticket_ids = Event.base_query().filter(
            
    #     ).all()
    #     result_dump = EventSchema(many=True).dump(ticket_ids)
    #     result = TicketListSchema().load(
    #         {
    #             "ticket": result_dump,
    #             "limit": values.get('limit'),
    #             "offset": values.get('offset'),
    #             "keywords": values['keywords'] if values.get('keywords') else '',
    #             "total": len(ticket_ids)
    #         }
    #     )
    #     return result

    def create(self, values: dict):
        event_id = Event(
            name=values.get('name'),
            code=values.get('code'),
        )
        event_id.save()
        return event_id
    
    def delete(self, id: int, user_id: int):
        event_id = Event.base_query().filter_by(
            id=id,
            user_id=user_id,
        ).first()
        if not event_id:
            return False, "Event not found"
        event_id.delete()
        return True, event_id
    
    def update(self, values: dict):
        event_id = Event.base_query().filter(
            Event.id == values.get('id'),
        ).first()
        if not event_id:
            return False, "Event not found"
        print(values)
        event_id.update(**values)
        return event_id

class EventRegistrationHelpers:
    def __init__(
        self,
        api=None,
        method=None,
    ):
        self.api = api
        self.method = method

    def create(self, values: dict):
        # event_id = Event.base_query().filter(
        #     Event.id == values.get('event_id'),
        # ).first()
        event_registration_id = EventRegistration(
            event_id=values.get('event_id'),
            name=values.get('name'),
            reg_no=values.get('reg_no'),
            email=values.get('email'),
            phone=values.get('phone'),
            is_on_behalf=values.get('is_on_behalf'),
            on_behalf=values.get('on_behalf'),
        )
        event_registration_id.save()
        return event_registration_id

    def generate_qr_code(self, message=""):
        qrcode = segno.make_qr(
            message,
        )
        filename = "sample.png"
        store_path = os.path.join( os.getenv('QR_PATH'), filename)
        qrcode.save(
            store_path,
            scale=10,
        )
    