from django.contrib import admin

from .models import Action, ActionRecurrence, Context, Folder, GtdUser

admin.site.register(GtdUser)
admin.site.register(Folder)
admin.site.register(Context)


class ActionRecurrenceInline(admin.TabularInline):
    model = ActionRecurrence
    extra = 0


class ActionAdmin(admin.ModelAdmin):
    inlines = [
        ActionRecurrenceInline,
    ]


admin.site.register(Action, ActionAdmin)
