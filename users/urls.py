from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.student_and_admin_dashboard, name='student_admin_dashboard'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),

    path("teacher-signup/", views.TeacherSignUpView.as_view(), name="teacher_signup"),
    path("teacher-profile/", views.TeacherProfileView.as_view(), name="teacher_profile"),
    path("teacher-profile/edit/", views.TeacherProfileUpdateView.as_view(), name="teacher_profile_edit"),

    path('unapproved-teachers/', views.UnapprovedUserListView.as_view(), name='unapproved_teachers'),
    path('approve-teacher/<int:pk>/', views.approve_teacher, name='approve_teacher'),
]