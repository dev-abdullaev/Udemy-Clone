
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, TeacherForm, TeacherUpdateForm, UserUpdateForm
from .models import CustomUser, Teacher


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = [ "username", 'first_name', 'last_name', "email", "is_staff", 'is_active']


    def is_teacher(self, obj):
        return f'{obj.teacher.is_teacher}'

admin.site.register(CustomUser, CustomUserAdmin)


class TeacherAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    model = Teacher
    list_display = ["full_name", 'username', 'email', 'is_active', 'is_staff']

    def full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'


    def email(self, obj):
        return f'{obj.user.email}'

    def is_active(self, obj):
        return f'{obj.user.is_active}'

    def is_staff(self, obj):
        return f'{obj.user.is_staff}'

    def username(self, obj):
        return f'{obj.user.username}'


admin.site.register(Teacher, TeacherAdmin)

# admin.site.register(Teacher)