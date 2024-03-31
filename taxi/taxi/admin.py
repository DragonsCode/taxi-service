from django.contrib import admin
from .models import Driver, Client, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("first_name", "last_name", "email", "is_staff", "is_active",)
    list_filter = ("first_name", "last_name", "email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name", "last_name",
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
admin.site.register(Driver)
admin.site.register(Client)
