from django.urls import path

from . import views

urlpatterns = [
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),

    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path("teacher-signup/", views.TeacherSignUpView.as_view(), name="teacher_signup"),
    path("teacher-profile/", views.TeacherProfileView.as_view(), name="teacher_profile"),
    path("teacher-profile/edit/", views.TeacherProfileUpdateView.as_view(), name="teacher_profile_edit"),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('unapproved-teachers/', views.UnapprovedUserListView, name='unapproved_teachers'),
    path('approve-teacher/<int:pk>/', views.approve_teacher, name='approve_teacher'),
]