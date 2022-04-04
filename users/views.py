from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from .forms import CustomUserCreationForm, UserUpdateForm, TeacherForm, TeacherUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Teacher
from django.db.models import Count
from course.models import Course, Enroll



@login_required
def student_dashboard(request):
    enrolled_courses = Course.objects.all().filter(enroll__student=request.user)
    std_course_count = Enroll.objects.all().filter(student__id=request.user.id).count()


    context = {
        'enrolled_courses': enrolled_courses,
        'std_course_count':std_course_count,

    }

    return render(request, 'dashboards/student_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    teacher_course_count = Course.objects.filter(teacher__pk=request.user.pk).count()
    teacher_courses = Course.objects.filter(teacher__pk=request.user.pk)


    context = {
        'teacher_course_count': teacher_course_count,
        'teacher_courses': teacher_courses
    }

    return render(request, 'dashboards/teacher_dashboard.html', context)


@login_required
def admin_dashboard(request):
    teachers = Teacher.objects.all()
    courses = Course.objects.all()
    students = Enroll.objects.select_related().annotate(std_count=Count('student_id')).count()
            

    context = {
        'students': students,
        "courses": courses,
        'teachers':teachers
    }

    return render(request, 'dashboards/admin_dashboard.html', context)


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


@login_required
def UnapprovedUserListView(request):
    teachers = CustomUser.objects.filter(is_active=False, is_teacher=False)


    context = {'teachers': teachers}
    return render(request, 'dashboards/unapproved_teachers.html', context)


def approve_teacher(request, pk):
    teacher = CustomUser.objects.get(id=pk)
    teacher.is_active = True
    teacher.is_teacher = True

    teacher.save()
    
    return redirect('unapproved_teachers')


def reject_teacher(request, pk):
    teacher = CustomUser.objects.get(id=pk)
    teacher.delete()
    
    return redirect('unapproved_teachers')





































