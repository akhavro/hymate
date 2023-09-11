from django.contrib import admin

from core.models import Producer, Consumer, GridAccess, Storage


admin.site.register(Producer)
admin.site.register(Consumer)
admin.site.register(GridAccess)
admin.site.register(Storage)
