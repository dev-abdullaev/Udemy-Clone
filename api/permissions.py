
from django.shortcuts import redirect
from rest_framework import permissions

from course.models import Course, Enroll, Video



class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_teacher:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_teacher:
            return True
        return False


class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_student:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_student:
            return True
        return False


class IsOwnerOfVideo(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_teacher:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.__class__.objects.filter(section__course__teacher__pk=request.user.pk)



class IsPaid(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        per = Enroll.objects.filter(is_paid=True)

        if per:
            return True
        return False
    