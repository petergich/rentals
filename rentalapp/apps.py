from django.apps import AppConfig
from django.db.models.signals import post_migrate
# django.core.management import Command.handle
import logging
import time
import threading
from .daemon_thread import DaemonThread
# from  .management.commands.run_background_task import charges
logger = logging.getLogger(__name__)
class RentalappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rentalapp'
    def ready(self):
        

        if not any(isinstance(thread, DaemonThread) for thread in threading.enumerate()):
            daemon_thread = DaemonThread()
            daemon_thread.start()