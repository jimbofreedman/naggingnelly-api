from django.contrib import admin
from .models import GtdUser, Folder, Context, Action

admin.site.register(GtdUser)
admin.site.register(Folder)
admin.site.register(Context)
admin.site.register(Action)
