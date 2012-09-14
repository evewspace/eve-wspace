from Map.models import *
from django.contrib import admin

class SystemAdmin(admin.ModelAdmin):
    fields = ['occupied', 'info']

admin.site.register(System, SystemAdmin)
admin.site.register(Map)
admin.site.register(MapSystem)
admin.site.register(Signature)
admin.site.register(SignatureType)
admin.site.register(Wormhole)
