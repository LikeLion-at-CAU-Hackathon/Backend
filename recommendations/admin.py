from django.contrib import admin

from .models import (
    VisitSession,
    VisitHistory,
    StyleProfile,
)


admin.site.register(VisitSession)
admin.site.register(VisitHistory)
admin.site.register(StyleProfile)