from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RoomObjectIdentifiers,DataSensorObjects,Room,OperatorID,SerialConfigurationObjectA,SerialConfigurationObjectB

admin.site.register(Room)
admin.site.register(SerialConfigurationObjectA)
admin.site.register(SerialConfigurationObjectB)
admin.site.register(OperatorID)
admin.site.register(RoomObjectIdentifiers)
admin.site.register(DataSensorObjects)