from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoice.settings')
app = Celery('invoice')   
app.conf.enable_utc=False

app.conf.timezone='Asia/Kolkata'

# Using a string here means the worker will not have to
# pickle the object when using Windows.

app.config_from_object(settings, namespace='CELERY')  ##### Letting my app know what the default settings for celery
                                                      ##### from django settings file

####### This will set a celery beat schedule that will add a task to database whenever we start the program ########
app.conf.beat_schedule={
    #  'send-mail-every-day-at-8': {
    #      'task': 'trial.tasks.rem_email',
    #      'schedule': 15,
    #      'args': ({"email_fr":"abhiqwik01@gmail.com","email_to":"abhiramganesh98@gmail.com",
    #      'Rem_date_day':"1",'Rem_date_month':"1",'Rem_date_year':"2022"},)
    # }
}

app.autodiscover_tasks() ########## Celery automatically reads tasks.py file in our folder and links them directly in
                         ########## the functions we call.


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')