from apps.event.models import (
    EventModel,
    EventInvitationModel,
    EventRegistrationModel,
)
from apps.event.schemas import (
    # Events
    EventSchema,
    EventListSchema,

    EventRegistrationSchema,
)
import os
import base64
import pandas as pd
import segno
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

class EventHelpers:
    def __init__(
        self,
        api=None,
        method=None,
    ):
        self.api = api
        self.method = method

    def read(self, params: dict):
        # session.query(MyClass).filter(MyClass.name == 'some name')
        query_event_ids = EventModel.base_query()
        if (params['keywords'] != ''):
            query_event_ids = query_event_ids.filter(
                EventModel.name == params['keywords'],
            )
        query_event_ids = query_event_ids.offset(
            params['offset']
        ).limit(
            params['limit']
        )
        event_ids = query_event_ids.all()
        result_dump = EventSchema(many=True).dump(event_ids)
        print(result_dump)
        result = {
            "data": result_dump,
            "limit": params.get('limit'),
            "offset": params.get('offset'),
            "keywords": params['keywords'] if params.get('keywords') else '',
            "total": len(event_ids)
        }
        return True, result

    def create(self, values: dict):
        # try:
            event_id = EventModel(
                name=values.get('name'),
                code=values.get('code'),
                sequence=1,
                event_date=values.get('event_date'),
                created_uid=0,
                updated_uid=0
            )
            event_id.save()
            return True, event_id
        # except Exception as e:
        #     return False, e
    
    def delete(self, id: int, user_id: int):
        event_id = EventModel.base_query().filter_by(
            id=id,
            user_id=user_id,
        ).first()
        if not event_id:
            return False, "Event not found"
        event_id.delete()
        return True, event_id
    
    def update(self, values: dict):
        event_id = EventModel.base_query().filter(
            EventModel.id == values.get('id'),
        ).first()
        if not event_id:
            return False, "Event not found"
        print(values)
        event_id.update(**values)
        return event_id

    def sent_invitation(self, event_id=0):
        print("send email invitations")
        print("event_id:", event_id)
        query_event_invitation_ids = EventModel().base_query().first()
        event_invitation_ids = query_event_invitation_ids
        print(event_invitation_ids)

class EventLineHelpers:
    def __init__(self):
        pass

    def create(self, values: dict):
        pass

class EventRegistrationHelpers:
    def __init__(
        self,
        api=None,
        method=None,
    ):
        self.api = api
        self.method = method

    def create(self, values: dict):
        event_id = EventModel.base_query().filter_by(
            id=values.get('event_id'),
        ).first()
        ## 12IDF2300001
        reg_no = "{}{}{}{}".format(
            event_id.start_date.month,
            event_id.code,
            event_id.start_date.year,
            event_id.sequence.zfill(5)
        )
        event_registration_id = EventRegistrationModel(
            event_id=values.get('event_id'),
            name=values.get('name'),
            reg_no=reg_no,
            email=values.get('email'),
            phone=values.get('phone'),
            is_on_behalf=values.get('is_on_behalf'),
            on_behalf=values.get('on_behalf'),
        )
        event_registration_id.save()
        event_id.sequence += 1
        event_id.save()
        return event_registration_id
    
    def create_qr(self, values):
        print(values)
        event_registration_id = EventRegistrationModel.base_query().filter_by(
            id=values.get('reg_id'),
            event_id=values.get('event_id')
        ).first()
        self.generate_qr_code(
            message="{}".format(event_registration_id.reg_no),
            event_id=values.get('event_id'),
            registration_id=event_registration_id.id
        )
        return True
    
    def check_path(self, event_id):
        qr_dir = os.getenv('QR_PATH')
        path_dir = os.path.join(qr_dir, str(event_id))
        status = os.path.exists(path_dir)
        if (status):
            return True
        else:
            os.mkdir(path_dir)
            return True

    def generate_qr_code(self, message="", event_id=0, registration_id=0):
        qrcode = segno.make_qr(
            message,
        )
        self.check_path(event_id)
        filename = "{}.png".format(str(registration_id))
        store_path = os.path.join( os.getenv('QR_PATH'), str(event_id), filename)
        qrcode.save(
            store_path,
            scale=10,
        )
        return True

    def registration_detail(self, args):
        print("", args)
        event_reg_id = EventRegistrationModel.base_query().filter_by(
            id=args.get('reg_id'),
            event_id=args.get('event_id')
        ).first()
        filename = "{}.png".format(str(args.get('reg_id')))
        store_path = os.path.join( os.getenv('QR_PATH'), str(args.get('event_id')), filename)
        with open(store_path, 'rb') as image_file:
            base64_bytes = base64.b64encode(image_file.read())
            base64_string = base64_bytes.decode()
            qr_code = base64_string

        return True, {
            "name": event_reg_id.name,
            "email": event_reg_id.email,
            "phone": event_reg_id.phone,
            "qr_code": qr_code,
        }
    