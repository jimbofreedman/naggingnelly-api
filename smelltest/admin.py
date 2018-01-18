from django.contrib import admin

from .models import Scent, ScentGroup, TestResult

admin.site.register(ScentGroup)
admin.site.register(TestResult)


class ScentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Scent, ScentAdmin)
