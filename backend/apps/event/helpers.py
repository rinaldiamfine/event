from jinja2 import Environment, FileSystemLoader
import os
import uuid
import base64
import pandas as pd
import segno
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import and_, or_
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from apps.tools.email import EmailManager
load_dotenv()
from apps.event.models import (
    EventModel,
    EventLineModel,
    EventInvitationModel,
    EventRegistrationModel,
    EventSouvenirClaimModel,

    ## Enum
    RegistrationType
)
from apps.event.schemas import (
    # Events
    EventSchema,
    ListEventSchema,
    EventLineSchema,

    EventRegistrationSchema,
    ListEventRegistrationSchema
)

class EventHelpers:
    def __init__(
        self,
        api=None,
        method=None,
    ):
        self.api = api
        self.method = method

    def list(self, params: dict):
        # session.query(MyClass).filter(MyClass.name == 'some name')
        query_event_ids = EventModel.query.filter(
            or_(
                EventModel.is_deleted==False,
                EventModel.is_deleted==None,
            )
        )
        if (params.get('keywords') != None and params['keywords'] != ''):
            query_event_ids = query_event_ids.filter(
                EventModel.name.ilike('%{}%'.format(params['keywords']))
            )
        if (params.get('offset') != None and params.get('limit') != None):
            query_event_ids = query_event_ids.offset(
                params['offset']
            ).limit(
                params['limit']
            )
        event_ids = query_event_ids.all()
        result_dump = ListEventSchema(many=True).dump(event_ids)
        result = {
            "success": True,
            "message": "List of event successfully fetched!",
            "data": result_dump,
            "limit": params.get('limit'),
            "offset": params.get('offset'),
            "keywords": params['keywords'] if params.get('keywords') else '',
            "total": len(event_ids)
        }
        return True, result

    def create(self, values: dict):
        try:
            event_id = EventModel(
                name=values.get('name'),
                code=values.get('code'),
                venue=values.get('venue'),
                event_time=values.get('event_time'),
                event_date=values.get('event_date'),
                created_uid=0,
                updated_uid=0
            )
            event_id.save()
            result_dump = EventSchema().dump(event_id)
            result = {
                "success": True,
                "message": "Event successfully created",
                "data": result_dump,
            }
            return True, result
        except Exception as e:
            return False, e
    
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

    def sent_email_invitation(self, event=0):
        print("send email invitations")
        print("event_id:", event)
        event_id = EventModel.query.filter(
            EventModel.id==event,
            or_(
                EventModel.is_deleted==False,
                EventModel.is_deleted==None,
            )
        ).first()
        query_event_invitation_ids = EventInvitationModel.query.filter(
            or_(
                EventInvitationModel.is_deleted==False,
                EventInvitationModel.is_deleted==None,
            ),
            EventInvitationModel.event_id==event
        )
        event_invitation_ids = query_event_invitation_ids.all()
        email_manager = EmailManager()
        load_path = os.path.join(os.getenv('BASE_PATH'), "apps", "templates")
        file_load_env = Environment(
            loader=FileSystemLoader(load_path)
        )
        email_template = file_load_env.get_template('email_invitation.html')
        for invitation in event_invitation_ids:
            print("invitation to:", invitation.email)
            template_data = {
                "username": invitation.name,
                "event_name": event_id.name,
                "event_date": event_id.event_date.strftime("%d %B %Y"),
                "event_time": event_id.event_time,
                "event_venue": event_id.venue,
                "event_line_ids": event_id.event_line_ids,
                "current_year": str(datetime.now().year),
                "reservation_link": "---"
            }
            template_render = email_template.render(
                template_data
            )
            message = MIMEMultipart()
            message['To'] = invitation.email
            message['Subject'] = "Invitation - {}".format(event_id.name)
            message['From'] = formataddr(("Admin Event {}".format(event_id.code), email_manager.user))
            message.attach(MIMEText(template_render, "html"))
            email_manager.send_email(message)

class EventLineHelpers:
    def __init__(
        self,
        api=None,
        method=None,
    ):
        self.api = api
        self.method = method

    def create(self, values: dict):
        try:
            event_line_id = EventLineModel(
                event_id=values.get('event_id'),
                name=values.get('name'),
                souvenir_cupons=values.get('souvenir_cupons'),
                created_uid=0,
                updated_uid=0
            )
            event_line_id.save()
            result_dump = EventLineSchema().dump(event_line_id)
            result = {
                "success": True,
                "message": "Event line successfully created",
                "data": result_dump,
            }
            return True, result
        except Exception as e:
            return False, e

class EventRegistrationHelpers:
    def __init__(
        self,
        api=None,
        method=None,
    ):
        self.api = api
        self.method = method

    def create(self, values: dict):
        try:
            event_id = EventModel.query.filter(
                EventModel.id==values.get('event_id'),
                or_(
                    EventModel.is_deleted==False,
                    EventModel.is_deleted==None,
                )
            ).first()
            registration_id = "{}{}{}".format(
                ## 12IDF2300001
                event_id.event_date.month,
                event_id.code,
                str(event_id.sequence).zfill(5)
            )
            ## Default type is audience
            registration_type = RegistrationType.AUDIENCE
            if RegistrationType.SPEAKER.value == values.get('type'):
                registration_type = RegistrationType.SPEAKER
            event_registration_id = EventRegistrationModel(
                event_id=values.get('event_id'),
                name=values.get('name'),
                uuid=uuid.uuid4(),
                registration_id=registration_id,
                email=values.get('email'),
                phone=values.get('phone'),
                institution=values.get('institution'),
                on_behalf=values.get('on_behalf'),
                registration_type=registration_type,
                created_uid=0,
                updated_uid=0
            )

            ## Generate QR-Code
            self.generate_qr_code(
                message="{}".format(event_registration_id.registration_id),
                event_id=event_id.id,
                uuid=event_registration_id.uuid
            )
            event_id.sequence += 1
            event_id.save()
            event_registration_id.save()

            ## Send succesfully registration on email message
            email_manager = EmailManager()
            load_path = os.path.join(os.getenv('BASE_PATH'), "apps", "templates")
            file_load_env = Environment(
                loader=FileSystemLoader(load_path)
            )
            email_template = file_load_env.get_template('email_registration.html')
            filename = "{}.png".format(event_registration_id.uuid)
            qr_store_path = os.path.join('qr-events', str(event_id.id), filename)
            template_data = {
                "qr_code_link": "{}/{}".format(os.getenv('APP_EVENT_URL'), qr_store_path),
                "registration_no": event_registration_id.registration_id,
                "username": event_registration_id.name,
                "institution": event_registration_id.institution if event_registration_id.institution != None else "-",
                "event_name": event_id.name,
                "event_date": event_id.event_date.strftime("%d %B %Y"),
                "event_time": event_id.event_time,
                "event_venue": event_id.venue,
                "current_year": str(datetime.now().year),
            }
            template_render = email_template.render(
                template_data
            )
            message = MIMEMultipart()
            message['To'] = event_registration_id.email
            message['Subject'] = "RSVP - {}".format(event_id.name)
            message['From'] = formataddr(("Admin Event {}".format(event_id.code), email_manager.user))
            message.attach(MIMEText(template_render, "html"))
            email_manager.send_email(message)

            result_dump = EventRegistrationSchema().dump(event_registration_id)
            result = {
                "success": True,
                "message": "Participant successfully registered",
                "data": result_dump,
            }
            return True, result
        except Exception as e:
            return False, e
    
    def create_qr(self, values):
        print(values)
        event_registration_id = EventRegistrationModel.base_query().filter_by(
            id=values.get('reg_id'),
            event_id=values.get('event_id')
        ).first()
        self.generate_qr_code(
            message="{}".format(event_registration_id.registration_id),
            event_id=values.get('event_id'),
            uuid=""
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

    def generate_qr_code(self, message="", event_id=0, uuid="0"):
        qrcode = segno.make_qr(
            message,
        )
        self.check_path(event_id)
        filename = "{}.png".format(uuid)
        store_path = os.path.join( os.getenv('QR_PATH'), str(event_id), filename)
        qrcode.save(
            store_path,
            scale=10,
        )
        return True

    def list(self, params: dict):
        if (params.get('registerId') != None):
            query_event_registration_id = EventRegistrationModel.query.filter(
                or_(
                    EventRegistrationModel.is_deleted==False,
                    EventRegistrationModel.is_deleted==None,
                ),
                EventRegistrationModel.registration_id==params['registerId']
            )
            event_registration_id = query_event_registration_id.first()
            result_participant_dump = EventRegistrationSchema().dump(event_registration_id)
            result_attendance_dump = None
            # if (event_registration_id.is_attendance == True):
            #     result_attendance_dump = EventRegistrationAttendanceSchema().dump(event_registration_id)
            result = {
                "success": True,
                "message": "Participant details successfully fetched",
                "data": {
                    "participant": result_participant_dump,
                    "attendance": result_attendance_dump,
                    "coupon": []
                },
            }
            return True, result
        else:
            query_event_registration_ids = EventRegistrationModel.query.filter(
                or_(
                    EventRegistrationModel.is_deleted==False,
                    EventRegistrationModel.is_deleted==None,
                )
            )
            if (params.get('keywords') != None and params.get('keywords') != ""):
                query_event_registration_ids = query_event_registration_ids.filter(
                    EventRegistrationModel.name.ilike('%{}%'.format(params['keywords']))
                )
            if (params.get('offset') != None and params.get('limit') != None):
                query_event_registration_ids = query_event_registration_ids.offset(
                    params['offset']
                ).limit(
                    params['limit']
                )
            event_registration_ids = query_event_registration_ids.all()
            result_dump = EventRegistrationSchema(many=True).dump(event_registration_ids)
            result = {
                "success": True,
                "message": "List of participant successfully fetched",
                "data": result_dump,
                "limit": params.get('limit'),
                "offset": params.get('offset'),
                "keywords": params['keywords'] if params.get('keywords') else '',
                "total": len(event_registration_ids)
            }
            return True, result
    
    def detail(self, uid):
        event_registration_id = EventRegistrationModel().query.filter(
            or_(
                EventRegistrationModel.is_deleted==False,
                EventRegistrationModel.is_deleted==None,
            ),
            EventRegistrationModel.id==uid
        ).first()
        event = event_registration_id.event_id
        event_line_ids = EventLineModel.query.with_entities(
            EventLineModel,
            EventSouvenirClaimModel
        ).outerjoin(
            EventSouvenirClaimModel, EventLineModel.id == EventSouvenirClaimModel.event_line_id
        ).filter(
            or_(
                EventLineModel.is_deleted==False,
                EventLineModel.is_deleted==None,
            ),
            EventLineModel.event_id==event
        ).order_by(
            EventLineModel.id
        ).all()
        print(event_registration_id.event_id, event_line_ids)
        return True, ""
    
class EventSouvenirClaimHelpers:
    def __init__(
        self,
        api=None,
        method=None,
    ):
        self.api = api
        self.method = method

    def create(self, values: dict):
        ## check condition
        event_registration_id = EventRegistrationModel.query.filter(
            or_(
                EventRegistrationModel.is_deleted==False,
                EventRegistrationModel.is_deleted==None,
            ),
            EventRegistrationModel.registration_id==values.get('registration_id')
        ).first()
        check_event_souvenir_ids = EventSouvenirClaimModel.query.filter(
            or_(
                EventSouvenirClaimModel.is_deleted==False,
                EventSouvenirClaimModel.is_deleted==None,
            ),
            EventSouvenirClaimModel.event_registration_id==event_registration_id.id,
            EventSouvenirClaimModel.event_line_id==values.get('event_line_id')
        ).all()
        if (len(check_event_souvenir_ids)>0):
            return False, "You're already claim this souvenir."
        event_souvenir_id = EventSouvenirClaimModel(
            event_line_id=values.get('event_line_id'),
            event_registration_id=event_registration_id.id,
            date_claim=datetime.now(),
            created_uid=0,
            updated_uid=0
        )
        event_souvenir_id.save()
        return True, event_souvenir_id
