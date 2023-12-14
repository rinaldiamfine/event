#!/usr/bin/env python
# coding: utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import and_, or_
from apps import app, db, celery, sock
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

## To check the celery worker:
# celery -A noah.celery worker --loglevel=info

@manager.command
def celery_status():
    """
    This method used to check celery worker status
    """
    i = celery.control.inspect()
    availability = i.ping()
    stats = i.stats()
    registered_tasks = i.registered()
    active_tasks = i.active()
    scheduled_tasks = i.scheduled()
    result = {
        'availability': availability,
        'stats': stats,
        'registered_tasks': registered_tasks,
        'active_tasks': active_tasks,
        'scheduled_tasks': scheduled_tasks
    }
    return result

@manager.command
@manager.option('-e', '--event', dest='event', default=0)
def generate_qr(event):
    import uuid
    from apps.event.models import (
        EventModel
    )
    from apps.event.helpers import (
        EventRegistrationHelpers
    )
    event_id = EventModel.query.filter(
        or_(
            EventModel.is_deleted==False,
            EventModel.is_deleted==None,
        ),
        EventModel.id==(event),
    ).first()
    if (event_id):
        registartion_ids = EventRegistrationHelpers().get_unsent_invitation(
            event_id=event_id
        )
        event_sequence = event_id.sequence
        for registration_id in registartion_ids:
            reg_no = "{}{}{}".format(
                ## 12IDF2300001
                event_id.event_date.month,
                event_id.code,
                str(event_sequence).zfill(5)
            )
            # registration_id.registration_id = reg_no
            # registration_id.uuid = uuid.uuid4()
            registration_id.save()

            print("Registration ID", registration_id.id)
            status_qr = EventRegistrationHelpers().generate_qr_code(
                message="{}".format(registration_id.registration_id),
                event_id=event_id.id,
                uuid=registration_id.uuid
            )
            event_sequence += 1

        event_id.sequence = event_sequence
        event_id.save()
            
    else:
        print("No Event")

@manager.command
@manager.option('-e', '--event', dest='event', default=0)
def sent_invitation(event):
    from apps.event.models import (
        EventModel
    )
    from apps.event.helpers import (
        EventRegistrationHelpers
    )
    event_id = EventModel.query.filter(
        or_(
            EventModel.is_deleted==False,
            EventModel.is_deleted==None,
        ),
        EventModel.id==(event),
    ).first()
    if (event_id):
        registartion_ids = EventRegistrationHelpers().get_unsent_invitation(
            event_id=event_id
        )
        for registration_id in registartion_ids:
            print("Registration ID", registration_id.id)
            status_email = EventRegistrationHelpers().sent_email_invitation(
                event_id=event_id,
                event_registration_id=registration_id
            )
            registration_id.sent_status = True
            registration_id.save()
            print("Email sent to:", registration_id.email, "with status:", status_email)

            # status_email = EventRegistrationHelpers().sent_whatsapp_invitation(
            #     event_id=event_id,
            #     event_registration_id=registration_id
            # )
            # print("Email whatsapp to:", registration_id.phone, "with status:", status_email)
    else:
        print("No Event")

# @manager.command
# def sps():
#     import os.path
#     from google.auth.transport.requests import Request
#     from google.oauth2.credentials import Credentials
#     from google_auth_oauthlib.flow import InstalledAppFlow
#     from googleapiclient.discovery import build
#     from googleapiclient.errors import HttpError

#     # If modifying these scopes, delete the file token.json.
#     SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

#     # The ID and range of a sample spreadsheet.
#     SAMPLE_SPREADSHEET_ID = "1ZW_uZrfvswNtRmZ8z1M7np-VTtuawxb-O5mrzFgfGOo"
#     SAMPLE_RANGE_NAME = "Class Data!A2:E"


#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "{}/apps/credentials.json".format(os.getenv('BASE_PATH')), SCOPES
#             )
#         creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
    
#     try:
#         service = build("sheets", "v4", credentials=creds)
#         # Call the Sheets API
#         sheet = service.spreadsheets()
#         result = (
#             sheet.values()
#             .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
#             .execute()
#         )
#         values = result.get("values", [])

#         if not values:
#             print("No data found.")
#             return
#         print("Name, Major:")
#         for row in values:
#             # Print columns A and E, which correspond to indices 0 and 4.
#             print(f"{row[0]}, {row[4]}")

#     except HttpError as err:
#         print(err)

if __name__ == '__main__':
    manager.run()
