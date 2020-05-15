from django.contrib import admin

from .models import Client

class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = (
        'session',
        'user',
        'ip',
        'creation_date'
    )
    search_fields = (
        'user__email',
        'user__last_name',
        'user__first_name',
    )
    readonly_fields = (
        'creation_date',
        'deactivating_date',
        'device',
        'browser',
        'os',
        'ip',
        'user',
        'session',
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Client,ClientAdmin)