from django.contrib import admin

from app.models import Pass, Worker


@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    pass


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass
