from django.contrib import admin

from .models import UserKey

class UserKeyAdmin(admin.ModelAdmin):
    model = UserKey
    list_display = ('key', 'creation_time', 'key_type')
    search_fields = ('key', 'user__email', 'user__last_name', 'user__first_name',)
    readonly_fields = ('key', 'creation_time',)

admin.site.register(UserKey, UserKeyAdmin)
