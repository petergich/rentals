import threading
import time
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

def background_task():
    
    while True:
        from .models import Tenancy, Rent
        current_date = datetime.now()
        tenancies=Tenancy.objects.filter(is_current=True)
        for ten in tenancies:
            if ten.room: 
                if ten.room.rate=="daily":
                    difference = datetime.today().date() - ten.last_charged
                    if difference.days >= 1:
                        Rent.objects.create(
                                amount=ten.room.price,
                                tenancy=ten,
                                name=f"Rent for day{ten.last_charged + relativedelta(days=1)} to {ten.last_charged + relativedelta(days=2)}", 
                                start_date=ten.last_charged + relativedelta(days=1)
                            )
                        ten.arrears=ten.arrears+ten.room.price
                        ten.last_charged=ten.last_charged + relativedelta(days=1)
                        ten.save()
                if ten.room.rate=="weekly":
                    difference = datetime.today().date() - ten.last_charged
                    if difference.days >= 7:
                        Rent.objects.create(
                                amount=ten.room.price,
                                tenancy=ten,
                                name=f"Rent for week {ten.last_charged + relativedelta(days=7)} to {ten.last_charged + relativedelta(days=14)}", 
                                start_date=ten.last_charged + relativedelta(days=7)
                            )
                        ten.arrears=ten.arrears+ten.room.price
                        ten.last_charged=ten.last_charged + relativedelta(days=7)
                        ten.save()
                if ten.room.rate=="monthly":
                    

                    # Calculate the difference in months
                    difference_in_months = (int(current_date.year) - int(ten.last_charged.year)) * 12 + current_date.month - ten.last_charged.month
                    
                    # Check if the difference is greater than or equal to one month
                    if difference_in_months >= 1:
                        Rent.objects.create(
                                amount=ten.room.price,
                                tenancy=ten,
                                name=f"Rent for month {ten.last_charged + relativedelta(months=1)} to {ten.last_charged + relativedelta(months=2)}", 
                                start_date=ten.last_charged + relativedelta(months=1)
                            )
                        ten.arrears=ten.arrears+ten.room.price
                        ten.last_charged=ten.last_charged + relativedelta(months=1)
                        ten.save()
                if ten.room.rate=="yearly":
                    difference = current_date.year - ten.last_charged.year
                    if difference >= 1:
                        Rent.objects.create(
                                amount=ten.room.price,
                                tenancy=ten,
                                name=f"Rent for month {ten.last_charged + relativedelta(years=1)} to {ten.last_charged + relativedelta(years=2)}", 
                                start_date=ten.last_charged + relativedelta(years=1)
                            )
                        ten.arrears=ten.arrears+ten.room.price
                        ten.last_charged=ten.last_charged + relativedelta(years=1)
                        ten.save()
        
        time.sleep(10)  # Adjust sleep time as needed

class DaemonThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        

    def run(self):
        background_task()
