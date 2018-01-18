from django.contrib import admin

from .models import Action, Context, Folder, GtdUser

admin.site.register(GtdUser)
admin.site.register(Folder)
admin.site.register(Context)
admin.site.register(Action)
