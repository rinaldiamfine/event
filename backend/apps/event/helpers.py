from jinja2 import Environment, FileSystemLoader
import os
import uuid
import base64
# import pandas as pd
import requests
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
    CouponModel,

    ## Enum
    RegistrationType
)
from apps.committee.models import CommitteeModel
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
                sent_status=True,
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
            self.sent_email_invitation(
                event_id=event_id, 
                event_registration_id=event_registration_id
            )

            result_dump = EventRegistrationSchema().dump(event_registration_id)
            result = {
                "success": True,
                "message": "Participant successfully registered",
                "data": result_dump,
            }
            return True, result
        except Exception as e:
            print(e)
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
            # if (event_registration_id.is_attendance == True):
            #     result_attendance_dump = EventRegistrationAttendanceSchema().dump(event_registration_id)
            if not event_registration_id:
                return True, {
                    "success": False,
                    "message": "QR code is not valid",
                    "data": None
                }
            
            seminarkit_id = CouponModel.query.filter(
                CouponModel.coupon_id==event_registration_id.registration_id,
                CouponModel.coupon_type=="seminar kit"
            ).first()
            souvenir_id = CouponModel.query.filter(
                CouponModel.coupon_id==event_registration_id.registration_id,
                CouponModel.coupon_type=="seminar kit"
            ).first()
            result = {
                "success": True,
                "message": "Participant details successfully fetched",
                "data": {
                    "participant": result_participant_dump,
                    "checkin": {
                        "datetime": str(event_registration_id.date_attendance) if (event_registration_id.date_attendance) else None,
                        "checkinby": event_registration_id.user_attendance
                    },
                    "coupon": [
                        {
                            "status": True if seminarkit_id else False,
                            "coupon_type": "seminar kit",
                            "coupon_id": event_registration_id.registration_id,
                            "scannedAt": str(seminarkit_id.created) if seminarkit_id else None,
                            "scannedBy": seminarkit_id.user_scan if seminarkit_id else None
                        },
                        {
                            "status": True if souvenir_id else False,
                            "coupon_type": "souvenir",
                            "coupon_id": event_registration_id.registration_id,
                            "scannedAt": str(souvenir_id.created) if souvenir_id else None,
                            "scannedBy": souvenir_id.user_scan if souvenir_id else None
                        },
                    ]
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
    
    def sent_email_invitation(self, event_id, event_registration_id):
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
            "registration_type": event_registration_id.registration_type.name,
            "current_year": str(datetime.now().year),
        }
        template_render = email_template.render(
            template_data
        )
        message = MIMEMultipart()
        message['To'] = event_registration_id.email
        message['Subject'] = "RSVP - {}".format(event_id.name)
        message['Bcc'] = os.getenv('SMTP_LIST_BCC')
        message['From'] = formataddr(("Sekretariat IDF 2023", email_manager.user))
        message.attach(MIMEText(template_render, "html"))
        email_manager.send_email(message)
        return True

    def sent_whatsapp_invitation(self, val: dict):
        # 12IDF2300001
        event_registration_id = EventRegistrationModel.query.filter(
            EventRegistrationModel.registration_id==val.get('reg_id')
        ).first()
        url = "{}/api/{}".format(
            os.getenv('WHATSAPP_VENDOR_URL'),
            os.getenv('WHATSAPP_IMAGE_PREFIX'),
        )
        current_date = datetime.now()
        headers = {}
        caption = '''*KONFIRMASI REGISTRASI*
Indonesia Development Forum (IDF) Tahun 2023
Kepulauan Riau, 18-19 Desember 2023

*Kepada Yth.*
*{}*
{}

Nomor Registrasi: {}

Bapak/Ibu, terima kasih sudah melakukan registrasi dalam acara Indonesia Development Forum (IDF) 2023. Di atas adalah barcode yang dapat digunakan saat melakukan re-registrasi.

Informasi lebih lengkap perihal kegiatan IDF 2023: https://linktr.ee/IDF2023Agenda

*_CATATAN PENTING:_*

* Re-registrasi dibuka pada tanggal *18 Desember 2023 dari pukul 07.30 WIB* di Radisson Golf & Convention Center Batam.
* Jika diperlukan informasi lebih lanjut silahkan menghubungi Sekretrariat IDF di sekretariat.idf@gmail.com ditujukan kepada Sdri. Anne atau dengan nomor (+62812 1486 1113 - hanya WA chat) 

*Dresscode Acara*
* Acara puncak: Smart Casual Nuansa Biru (dapat menggunakan celana/bawahan blue jeans)
* ⁠Gala Dinner: Casual tema pakaian laut/baju pantai/nuansa kekayaan bahari dengan aksesoris pelengkap

Demikian disampaikan. Atas perhatian dan kerjasamanya, diucapkan terima kasih.

Sekretariat Indonesia Development Forum 2023'''.format(
    event_registration_id.name,
    event_registration_id.institution,
    event_registration_id.registration_id
)
        payloads = {
            "token": os.getenv('WHATSAPP_TOKEN'),
            "number": "+6282382284450",
            "file": "https://batamtech.com/qr-events/1/{}.png".format(event_registration_id.uuid),
            "caption": caption,
            "date": "{}-{}-{}".format(
                current_date.year,
                current_date.month,
                current_date.day
            ),
            "time": "{}:{}:{}".format(
                current_date.hour,
                current_date.minute,
                current_date.second
            )
        }
        response = requests.request("POST", url, headers=headers, data=payloads)
        print(response.text)
        return True, {
            "success": True,
            "message": "Success sent",
            "data": response.text,
        }

    def get_unsent_invitation(self, event_id):
        query_event_registration_ids = EventRegistrationModel.query.filter(
            or_(
                EventRegistrationModel.is_deleted==False,
                EventRegistrationModel.is_deleted==None,
            ),
            EventRegistrationModel.sent_status==False,
            EventRegistrationModel.event_id==event_id.id
        )
        return query_event_registration_ids.all()

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

class CouponHelpers:
    def __init__(
        self,
        api=None,
        method=None,
    ):
        self.api = api
        self.method = method

    def checkin(self, values: dict):
        try:
            event_registration_id = EventRegistrationModel.query.filter(
                or_(
                    EventRegistrationModel.is_deleted==False,
                    EventRegistrationModel.is_deleted==None,
                ),
                EventRegistrationModel.registration_id==values.get('coupon')
            ).first()
            committee_id = CommitteeModel.query.filter(
                CommitteeModel.id==values.get('committee_id')
            ).first()
            if not committee_id:
                return True, {
                    "success": False,
                    "message": "Committee is not valid",
                    "data": None,
                }
            if event_registration_id:
                coupon_id = CouponModel.query.filter(
                    CouponModel.coupon_id==event_registration_id.registration_id,
                    CouponModel.coupon_type=="seminar kit"
                ).first()
                if coupon_id:
                    return True, {
                        "success": False,
                        "message": "You already checkin",
                        "data": {
                            "coupon_type": "seminar kit",
                            "coupon_id": coupon_id.coupon_id,
                            "scannedAt": str(coupon_id.created),
                            "scannedBy": coupon_id.user_scan
                        },
                    }
                else:
                    create_coupon_id = CouponModel(
                        coupon_id = event_registration_id.registration_id,
                        coupon_type = "seminar kit",
                        user_scan = committee_id.name,
                        user_scan_id = committee_id.id
                    )
                    create_coupon_id.save()

                    event_registration_id.date_attendance = datetime.now()
                    event_registration_id.updated_uid = committee_id.id
                    event_registration_id.user_attendance = committee_id.name
                    event_registration_id.save()

                    return True, {
                        "success": True,
                        "message": "Success checkin",
                        "data": {
                            "coupon_type": "seminar kit",
                            "coupon_id": create_coupon_id.coupon_id,
                            "scannedAt": str(create_coupon_id.created),
                            "scannedBy": create_coupon_id.user_scan
                        },
                    }
            else:
                return True, {
                    "success": False,
                    "message": "QR-Code is not valid",
                    "data": None,
                }
    
        except Exception as e:
            return False, e
        
    def claim_coupons(self, values: dict):
        try:
            event_registration_id = EventRegistrationModel.query.filter(
                or_(
                    EventRegistrationModel.is_deleted==False,
                    EventRegistrationModel.is_deleted==None,
                ),
                EventRegistrationModel.registration_id==values.get('coupon')
            ).first()
            committee_id = CommitteeModel.query.filter(
                CommitteeModel.id==values.get('committee_id')
            ).first()
            if not committee_id:
                return True, {
                    "success": False,
                    "message": "Committee is not valid",
                    "data": None,
                }
            if event_registration_id:
                coupon_id = CouponModel.query.filter(
                    CouponModel.coupon_id==event_registration_id.registration_id,
                    CouponModel.coupon_type=="souvenir"
                ).first()
                if coupon_id:
                    create_coupon_id = CouponModel(
                        coupon_id = event_registration_id.registration_id,
                        coupon_type = "souvenir",
                        user_scan = committee_id.name,
                        user_scan_id = committee_id.id
                    )
                    create_coupon_id.save()
                    return True, {
                        "success": False,
                        "message": "Coupon is claimed, but you can enter",
                        "data": {
                            "coupon_type": "souvenir",
                            "coupon_id": coupon_id.coupon_id,
                            "scannedAt": str(coupon_id.created),
                            "scannedBy": coupon_id.user_scan
                        },
                    }
                else:
                    create_coupon_id = CouponModel(
                        coupon_id = event_registration_id.registration_id,
                        coupon_type = "souvenir",
                        user_scan = committee_id.name,
                        user_scan_id = committee_id.id
                    )
                    create_coupon_id.save()
                    return True, {
                        "success": True,
                        "message": "Success claim coupon",
                        "data": {
                            "coupon_type": "souvenir",
                            "coupon_id": create_coupon_id.coupon_id,
                            "scannedAt": str(create_coupon_id.created),
                            "scannedBy": create_coupon_id.user_scan
                        },
                    }
            else:
                return True, {
                    "success": False,
                    "message": "QR-Code is not valid",
                    "data": None,
                }
    
        except Exception as e:
            return False, e