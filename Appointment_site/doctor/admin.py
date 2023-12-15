from django.contrib import admin
from .models import Appointment
# Register your models here.

#class AppointmentAdmin(admin.ModelAdmin):
#    list_display=('id','first_name', 'last_name','email','phone','message','sent_date','accepted','accepted_date')

admin.site.register(Appointment)

#SuperUser  admin admin123