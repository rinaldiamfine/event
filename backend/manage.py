#!/usr/bin/env python
# coding: utf-8
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import and_, or_
from apps import app, db, celery
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
            registration_id.registration_id = reg_no
            registration_id.uuid = uuid.uuid4()
            registration_id.save()
            event_sequence += 1

            print("Registration ID", registration_id.id)
            status_qr = EventRegistrationHelpers().generate_qr_code(
                message="{}".format(registration_id.registration_id),
                event_id=event_id.id,
                uuid=registration_id.uuid
            )

        event_id.sequence = event_sequence
        event_id.save()
            
    else:
        print("No Event")

@manager.command
def generate_pdf():
    print("GENERATE PDF")
    import pdfkit
    from jinja2 import Environment, FileSystemLoader
    from apps.event.models import (
        EventRegistrationModel
    )
    event_registration_id = EventRegistrationModel.query.filter(
        EventRegistrationModel.id==1,
    ).first()
    print(event_registration_id)
    load_path = os.path.join(os.getenv('BASE_PATH'), "apps", "templates")
    file_load_env = Environment(
        loader=FileSystemLoader(load_path)
    )
    email_template = file_load_env.get_template('pdf_registration.html')
    filename = "{}.png".format(event_registration_id.uuid)
    output_name = "{}.html".format(event_registration_id.uuid)
    pdfname = "{}.pdf".format(event_registration_id.uuid)
    qr_store_path = os.path.join('qr-events', str(1), filename)
    html_store_path = os.path.join(os.getenv('QR_PATH'), str(1), output_name)
    pdf_store_path = os.path.join(os.getenv('QR_PATH'), str(1), pdfname)
    template_data = {
        "qr_code_link": "{}/{}".format(os.getenv('APP_EVENT_URL'), qr_store_path),
        "registration_no": event_registration_id.registration_id,
        "username": event_registration_id.name,
        "institution": event_registration_id.institution if event_registration_id.institution != None else "-",
        "registration_type": event_registration_id.registration_type.name,
    }
    template_render = email_template.render(
        template_data
    )
    with open(html_store_path, "w") as text_file:
        text_file.write(str(template_render))

    # print(template_render)
    pdfkit.from_file(
        html_store_path,
        pdf_store_path
    )

@manager.command
def test_wa():
    from apps.event.helpers import (
        EventRegistrationHelpers
    )
    from apps.event.models import (
        EventRegistrationModel
    )
    event_registration_id = EventRegistrationModel.query.filter(
        EventRegistrationModel.id==1
    ).first()
    EventRegistrationHelpers().sent_whatsapp_invitation(event_registration_id)



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


@manager.command
@manager.option('-i', '--id', dest='id', default=0)
@manager.option('-n', '--name', dest='name', default="")
@manager.option('-in', '--institution', dest='institution', default="")
def test_socket(id, name, institution):
    from apps.event.helpers import (
        CouponHelpers
    )
    sts = CouponHelpers().socket_trigger(
        id, name, institution
    )
    print(sts)

if __name__ == '__main__':
    manager.run()

