from django.contrib import admin

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import (
    User,
    UserKey,
    OpenSession
)

class OpenSessionInline(admin.TabularInline):
    model = OpenSession
    readonly_fields = (
        'token',
        'key',
    )
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserKeyInline(admin.TabularInline):
    model = UserKey
    readonly_fields = (
        'key',
        'creation_time',
    )

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = '__all__'
        inlines = (UserKeyInline,)

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_admin',
    )
    list_filter = (
        'is_admin',
        'is_active'
    )
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password'
            )
        }),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_admin',
                'is_active'
            )
        }),
        ('Dates', {
            'fields': (
                'registration_date',
                'last_login',
                'first_activation_date',
            )
        }),
    )

    readonly_fields = (
        'registration_date',
        'last_login',
        'first_activation_date',
    )

    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2'
            ),
        }),
    )
    search_fields = (
        'email',
        'last_name',
        'first_name',
    )
    ordering = (
        'email',
    )
    filter_horizontal = ()

    def get_inlines(self, request, obj=None):
        if obj:
            return (UserKeyInline,OpenSessionInline)
        return ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


class UserKeyAdmin(admin.ModelAdmin):
    model = UserKey
    list_display = (
        'key',
        'creation_time',
        'key_type',
    )
    list_filter = (
        'key_type',
    )
    search_fields = (
        'key',
        'user__email',
        'user__last_name',
        'user__first_name',
    )
    readonly_fields = (
        'key',
        'creation_time',
    )

admin.site.register(UserKey, UserKeyAdmin)


class OpenSessionAdmin(admin.ModelAdmin):
    model = OpenSession
    list_display = (
        'key',
        'user',
        'token'
    )
    search_fields = (
        'key',
        'token__key',
        'user__email',
        'user__last_name',
        'user__first_name',
    )
    readonly_fields = (
        'token',
        'key',
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

