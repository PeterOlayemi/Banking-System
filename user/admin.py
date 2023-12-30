from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(CustomerAccount)
admin.site.register(StaffAccount)
admin.site.register(Message)
