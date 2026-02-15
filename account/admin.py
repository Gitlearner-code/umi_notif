from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .views import send_account_creation_email

class CustomUserAdmin(UserAdmin):
    # Which fields to display in the list view
    list_display = ('username', 'first_name', 'last_name', 'email', 'user_type', 'function', 'departement')

    # Organize fields into sections
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('User type', {'fields': ('user_type', 'function', 'departement')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add fields when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 👇 Removed 'username' here, it will be auto-generated
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'user_type', 'function', 'departement'),
        }),
    )

    # Optional: filter by user type
    list_filter = ('user_type', 'function', 'departement', 'is_staff', 'is_superuser')

    def save_model(self, request, obj, form, change):
        # Auto-generate username if creating a new user
        if not change and not obj.username:
            # Combine first_name and last_name, normalize spaces, lowercase
            full_name = f"{obj.first_name.strip()} {obj.last_name.strip()}"
            # Collapse multiple spaces into one
            base_username = " ".join(full_name.split()).lower()

            new_username = base_username
            counter = 1
            # Ensure uniqueness
            while User.objects.filter(username=new_username).exists():
                counter += 1
                new_username = f"{base_username} {counter}"
                

            obj.username = new_username

        super().save_model(request, obj, form, change)


        # Send email only when creating a new user
        if not change:
            send_account_creation_email(request, obj)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            if obj.user_type == 'EXEC':
                return (
                    (None, {'fields': ('username', 'password')}),
                    ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
                    ('Executif info', {'fields': ('function',)}),
                    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                )
            elif obj.user_type == 'REP':
                return (
                    (None, {'fields': ('username', 'password')}),
                    ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
                    ('Representant info', {'fields': ('departement',)}),
                    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                )
        return fieldsets


admin.site.register(User, CustomUserAdmin)