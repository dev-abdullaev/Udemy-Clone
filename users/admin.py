
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, TeacherForm
from .models import CustomUser, Teacher


UserAdmin.fieldsets += ('Custom fields set', {'fields': ('is_teacher', 'is_student')}),

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = [ "username", 'first_name', 'last_name', "email", 'is_teacher', 'is_active', 'is_student']



admin.site.register(CustomUser, CustomUserAdmin)


class TeacherAdmin(admin.ModelAdmin):
    add_form = TeacherForm
    model = Teacher
    list_display = ["full_name", 'username', 'email', 'is_active', 'is_teacher' ]

    def full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def email(self, obj):
        return f'{obj.user.email}'

    def is_active(self, obj):
        return f'{obj.user.is_active}'

    def is_teacher(self, obj):
        return f'{obj.user.is_teacher}'

    def username(self, obj):
        return f'{obj.user.username}'


admin.site.register(Teacher, TeacherAdmin)

# admin.site.register(Teacher)