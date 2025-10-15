from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentData
from core.admins.student import *

class StudentInline(admin.StackedInline):
    model = StudentData
    can_delete = False
    verbose_name_plural = "Student profile"

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [StudentInline]
    list_display = ("email", "full_name", "role", "is_active")
    list_filter = ("role", "is_active")

admin.site.register(StudentData)