from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "id", "email", "role", "is_active",
        "is_staff", "is_superuser", "created_at"
    )
    list_display_links = ("id", "email")
    search_fields = ("email",)
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    ordering = ("id",)

    # Fields shown on the user detail page
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("role",)}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", "is_superuser",
            "groups", "user_permissions"
        )}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    # Fields shown when creating a new user from admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2",
                "role", "is_active", "is_staff", "is_superuser"
            )}
        ),
    )

    # Optional: bulk actions
    actions = ["activate_users", "deactivate_users"]

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) activated.")

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} user(s) deactivated.")
