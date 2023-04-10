from django.contrib import admin
from .models import Task, Client,  Slave, Image, Reveiw

# Register your models here.
admin.site.register(Task)
admin.site.register(Client)
admin.site.register(Slave)
admin.site.register(Image)
admin.site.register(Reveiw)