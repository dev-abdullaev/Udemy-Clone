from django.contrib import admin

from .models import Category, Course, Section, Video, CourseReview, Enroll



admin.site.register(Section)
admin.site.register(Video)
admin.site.register(Enroll)


class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('course', "id", 'user')

admin.site.register(CourseReview, CourseReviewAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category, CategoryAdmin)



class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    

admin.site.register(Course, CourseAdmin)

