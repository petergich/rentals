from django.contrib import admin
from .models import *


admin.site.register(Tenant)
admin.site.register(Owner)
admin.site.register(Tenancy)
admin.site.register(House)
admin.site.register(Photo)
admin.site.register(Room)
# Register your models here.
