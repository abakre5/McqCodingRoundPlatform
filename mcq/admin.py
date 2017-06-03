from django.contrib import admin
from .models import Qrecord,Profile,Qattempt,SeniorQrecord, SeniorQattempt

# Register your models here.

admin.site.register(Qrecord)
admin.site.register(Profile)
admin.site.register(Qattempt)
admin.site.register(SeniorQrecord)
admin.site.register(SeniorQattempt)
