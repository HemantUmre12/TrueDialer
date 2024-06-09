from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Contact, CustomUser, SpamReport


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "name",
                    "email",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal info", {"fields": ("name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("phone_number", "name", "email", "is_staff", "is_active")
    search_fields = ("phone_number", "name", "email")
    ordering = ("phone_number",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(SpamReport)
