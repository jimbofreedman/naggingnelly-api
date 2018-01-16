from django.contrib import admin
from .models import ScentGroup, Scent, TestResult

admin.site.register(ScentGroup)
admin.site.register(TestResult)


class ScentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Scent, ScentAdmin)
