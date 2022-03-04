from django.urls import path 
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('all-courses/', views.CourseListView.as_view(), name='all_courses'),
    path('my-courses/', views.MyEnrolledCoursesListView.as_view(), name='enrolled_courses'),
    path('delete-my-enrolled-course/<str:slug>/<int:enroll_id>/', 
        views.MyEnrolledCourseDeleteView, name='delete_my_course'),
    path('watch-course/<slug:slug>/', views.watch_course, name='watch_course'),
    path('add-course/', views.CourseCreateView.as_view(), name='add_course'),
    path('update-course/<int:pk>/', views.CourseUpdateView.as_view(), name='update_course'),
    path('delete-course/<int:pk>/', views.CourseDeleteView.as_view(), name='delete_course'),
    path("search/", views.searchView, name="search"),


    path("reviews/<slug:slug>/", views.AddReviewView.as_view(), name="reviews"),
    path('edit-course-comment/<slug:slug>/<int:review_id>/',
        views.EditReviewView.as_view(), name='edit_course_review'),
    path('delete-course-comment/<slug:slug>/<int:review_id>/',
        views.ReviewDeleteView, name='delete_course_comment'),
    

    path('add-section/', views.SectionCreateView.as_view(), name='add_section'),
    path('sections/', views.SectionListView.as_view(), name='sections'),
    path('update-section/<int:pk>/', views.SectionUpdateView.as_view(), name='update_section'),
    path('delete-section/<int:pk>/', views.SectionDeleteView.as_view(), name='delete_section'),


    path('add-video/', views.VideoCreateView.as_view(), name='add_video'),
    path('videos/', views.VideoListView.as_view(), name='videos'),
    path('update-video/<int:pk>/', views.VideoUpdateView.as_view(), name='update_video'),
    path('delete-video/<int:pk>/', views.VideoDeleteView.as_view(), name='delete_video'),


    path('add-category/', views.CategoryCreateView.as_view(), name='add_category'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('update-category/<str:slug>/', views.CategoryUpdateView.as_view(), name='update_category'),
    path('delete-category/<str:slug>/', views.CategoryDeleteView.as_view(), name='delete_category'),


]