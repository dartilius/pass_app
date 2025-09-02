from django.contrib import admin

from app.models import Pass


@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    pass
