from django.contrib import admin
from .models import APIUser, Role

# Register your models here.
admin.site.register(APIUser)
admin.site.register(Role)
