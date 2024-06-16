import threading
import time


def background_task():
    from .models import Tenancy
    while True:
        print("Hey Background task is running...")
        time.sleep(10)  # Adjust sleep time as needed

class DaemonThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        

    def run(self):
        background_task()
