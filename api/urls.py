from django.urls import path
from . import views

urlpatterns = [

    path('', views.course_list, name='all-courses'),
    path('course-create/', views.course_create, name='course-create'),
    path('course-detail/<slug:slug>/', views.CourseDetail.as_view(), name='course-detail'),
    path('enrolled-courses/', views.enrolled_courses, name='enrolled-courses'),
    path('delete-enrolled-courses/<str:slug>/<int:enroll_id>/', views.delete_enrolled_courses, name='delete-enrolled-courses'),
    path('watch-course/<slug:slug>/', views.WatchCourse.as_view(), name='watch-course'),

    path('category-list/', views.category_list, name='category-list'),
    path('category-detail/<slug:slug>/', views.category_detail, name='category-detail'),

    path('video-list/', views.video_list, name='video-list'),
    path('video-detail/<int:pk>/', views.video_detail, name='video-detail'),

    path('section-list/', views.section_list, name='section-list'),
    path('section-detail/<int:pk>/', views.section_detail, name='section-detail'),

    path('review-list/', views.CourseReviewList.as_view(), name='review-list'),
    path('review-create/<slug:slug>/', views.CourseReviewCreate.as_view(), name='review-create'),
    path('review-detail/<int:pk>/', views.CourseReviewDetail.as_view(), name='review-detail'),

    path('student-dashboard/', views.StudentDashboard.as_view(), name='student-dashboard'),
    path('teacher-dashboard/', views.TeacherDashboard.as_view(), name='teacher-dashboard'),
    path('admin-dashboard/', views.AdminDashboard.as_view(), name='admin-dashboard'),

    path('student-register/', views.StudentRegistrationView.as_view(), name='student-register/'),
    path('teacher-register/', views.TeacherRegistrationView.as_view(), name='teacher-register/'),
    path('login', views.AuthUserLoginView.as_view(), name='login'),

    path('unapproved-teachers/', views.UnapprovedTeachersListView.as_view(), name='unapproved-teachers'),
    path('approve-teachers/<int:pk>/', views.ApproveTeachersView.as_view(), name='approve-teachers'),
    path('reject-teachers/<int:pk>/', views.RejectTeachersView.as_view(), name='reject-teachers'),

    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),

]

