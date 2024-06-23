from django.contrib import admin
from .models import *


admin.site.register(Tenant)
admin.site.register(Owner)
admin.site.register(Tenancy)
admin.site.register(House)
admin.site.register(Photo)
admin.site.register(Room)
admin.site.register(Rent)
admin.site.register(Payment)
admin.site.register(Extra)
# Register your models here.
