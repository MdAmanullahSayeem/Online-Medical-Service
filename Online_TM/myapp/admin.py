from django.contrib import admin
from .models import Profile, Account, Appointment, Message, Health, Prescription, Notification, Password, DocProfile

# Register your models here.
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(Account)
admin.site.register(Appointment)
admin.site.register(Message)
admin.site.register(Health)
admin.site.register(Prescription)
admin.site.register(Password)
admin.site.register(DocProfile)
