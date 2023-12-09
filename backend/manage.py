#!/usr/bin/env python
# coding: utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
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
def sent_invitation(event):
    from apps.event.helpers import (
        EventHelpers
    )
    EventHelpers().sent_email_invitation(event=event)

    
if __name__ == '__main__':
    manager.run()
