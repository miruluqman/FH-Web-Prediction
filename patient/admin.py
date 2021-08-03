from django.contrib import admin
from .models import patient, cholesterol, LDL, log, HDL, TG

admin.site.register(patient)
admin.site.register(cholesterol)
admin.site.register(LDL)
admin.site.register(log)
admin.site.register(HDL)
admin.site.register(TG)