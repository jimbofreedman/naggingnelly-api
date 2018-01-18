from django.contrib import admin

from .models import BadThing, BadThingType

admin.site.register(BadThingType)
admin.site.register(BadThing)
