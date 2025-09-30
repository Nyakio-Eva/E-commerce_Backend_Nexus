# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        'id', 'email', 'role', 'is_staff', 'is_active', 
        'is_email_verified', 'created_at'
    ]
    list_display_links = ['id', 'email']
    list_filter = ['role', 'is_staff', 'is_active', 'is_email_verified', 'created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Email Verification', {'fields': ('is_email_verified',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_active')
        }),
    )
    
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'date_joined', 'last_login']
    
    # Custom actions to manage users
    actions = ['make_admin', 'make_customer', 'activate_users', 'deactivate_users']
    
    def make_admin(self, request, queryset):
        """Promote selected users to admin"""
        updated = queryset.update(role=User.ADMIN, is_staff=True)
        self.message_user(request, f"{updated} user(s) promoted to admin.")
    make_admin.short_description = "Promote selected users to admin"
    
    def make_customer(self, request, queryset):
        """Demote selected users to customer"""
        # Prevent demoting superusers
        queryset = queryset.exclude(is_superuser=True)
        updated = queryset.update(role=User.CUSTOMER, is_staff=False)
        self.message_user(request, f"{updated} user(s) demoted to customer.")
    make_customer.short_description = "Demote selected users to customer"
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) activated.")
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        # Prevent deactivating superusers
        queryset = queryset.exclude(is_superuser=True)
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} user(s) deactivated.")
    deactivate_users.short_description = "Deactivate selected users"