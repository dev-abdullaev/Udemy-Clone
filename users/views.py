from urllib import request
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, ListView
from .forms import CustomUserCreationForm, UserUpdateForm, TeacherForm, TeacherUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from django.db.models import Count
from course.models import Course, Enroll



@login_required
def student_and_admin_dashboard(request):
    # These are related to students
    enrolled_courses = Course.objects.all().filter(enroll__student=request.user)
    std_course_count = Enroll.objects.all().filter(student__id=request.user.id).count()
    completed_course_count = Course.objects.filter(is_completed=True).count() 
    total_students = Enroll.objects.annotate(Count('student')).count()

    teacher_course_count = Course.objects.filter(teacher__id=request.user.is_staff).count()
    teacher_courses = Course.objects.filter(teacher__id=request.user.is_staff)
    enrolls = Enroll.objects.all()


    context = {
        'enrolls': enrolls,
        'enrolled_courses': enrolled_courses,
        'std_course_count':std_course_count,
        'total_students': total_students,
        'completed_course_count':completed_course_count,
        'teacher_course_count': teacher_course_count,
        'teacher_courses':teacher_courses
    }

    return render(request, 'student/dashboard.html', context)


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "profile/profile.html", {"user": request.user})


class ProfileUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)
        return render(request, "profile/update.html", {"form": user_update_form})

    def post(self, request):
        user_update_form = UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )

        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "You have successfully updated your profile.")

            return redirect("profile")

        return render(request, "profile/edit.html", {"form": user_update_form})


class TeacherSignUpView(CreateView):
    model = CustomUser
    form_class = TeacherForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')


class TeacherProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "profile/profile.html", {"user": request.user})


class TeacherProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_update_form = TeacherUpdateForm(instance=request.user)
        return render(request, "profile/profile_update.html", {"form": teacher_update_form})

    def post(self, request):
        teacher_update_form = TeacherUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )

        if teacher_update_form.is_valid():
            teacher_update_form.save()
            messages.success(request, "You have successfully updated your profile.")

            return redirect("profile")


class UnapprovedUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "student/unapproved_teachers.html"
    context_object_name = 'teachers'

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=False, is_staff=False)
        return qs


def approve_teacher(request, pk):
    teacher = CustomUser.objects.get(id=pk)
    teacher.is_active = True
    teacher.is_staff = True

    teacher.save()
    
    return redirect('unapproved_teachers')







































