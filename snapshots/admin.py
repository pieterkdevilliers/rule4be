from django.contrib import admin
from .models import AreaOfLife, Snapshot

# Register your models here.

class AreaOfLifeAdmin(admin.ModelAdmin):
    """
    Admin Interface Display Settings
    """
    list_display = ('owner', 'name', 'description')
    ordering = ['owner', 'name']


class SnapshotsAdmin(admin.ModelAdmin):
    """
    Admin Interface Display Settings
    """
    list_display = ('owner', 'area_of_life', 'body', 'created')
    readonly_fields=('created',)
    ordering = ['owner', 'area_of_life', 'created']


admin.site.register(AreaOfLife, AreaOfLifeAdmin)
admin.site.register(Snapshot, SnapshotsAdmin)