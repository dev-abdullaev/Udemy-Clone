from django import forms 
from django.forms import Textarea
from .models import Category, CourseReview, Video, Section, Course


class CourseReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = CourseReview
        fields = ('stars_given', 'comment')
        widgets = {
          'comment': Textarea(attrs={'rows':5, 'cols':20}),
        }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name','files', 'link', 'length']


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'video']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'category', 'section', 'name', 'description', 'requirements', 'to_whom', 'teacher',
            'image', 'price', 'video_link', 'difficulty', 'is_active'
        ]
        widgets = {
          'description': Textarea(attrs={'rows':5, 'cols':20}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']





