from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from cart.cart import Cart

from .forms import CourseReviewForm, SectionForm, VideoForm, CourseForm, CategoryForm
from .models import Course, CourseReview, Section, Video, Enroll, Category



def index(request):
    return render(request, 'index.html')


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "course/all_courses.html"
    context_object_name = 'courses'


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "course/course_detail.html"
    form_class = CourseReviewForm


    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        slug_field = self.get_slug_field()
        queryset = queryset.filter(**{slug_field: slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object(self.get_queryset())
        context['teacher_courses'] = Course.objects.filter(teacher__id=self.request.user.is_staff).count()
        context['student_for_every_course'] = Enroll.objects.filter(course__slug=self.kwargs["slug"]).count()
        context['form'] = CourseReviewForm()

        
        if self.request.user.is_authenticated:
            if Enroll.objects.filter(course=course, student=self.request.user).exists():
                context['is_enrolled'] = True
                context['is_paid'] = True
            else:
                cart = Cart(self.request)
                context['is_in_cart'] = cart.has_course(course)

        else:
            cart = Cart(self.request)
            context['is_in_cart'] = cart.has_course(course)
        return context


@login_required
def watch_course(request, slug):
    course = Course.objects.get(slug=slug)
    video = Video.objects.all()

    if request.user.is_authenticated:
        if Enroll.objects.filter(course=course, student=request.user).exists():
            is_paid = True
        else:
            is_paid = False


    
    context = {
        'course': course, 'video': video, 'is_paid': is_paid
    }
    return render(request, 'course/watch_course.html', context)


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    template_name = "course/add_course.html"
    form_class = CourseForm
    success_url = reverse_lazy('sections')


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    template_name = "course/update_course.html"
    form_class = CourseForm
    success_url = reverse_lazy('sections')


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "course/delete_course.html"
    success_url = reverse_lazy('sections')


class SectionCreateView(LoginRequiredMixin, CreateView):
    model = Section
    template_name = "section/add_section.html"
    form_class = SectionForm
    success_url = reverse_lazy('sections')


class SectionListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = "section/section_list.html"
    context_object_name = 'sections'
    paginate_by = 4


class SectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Section
    template_name = "section/update_section.html"
    form_class = SectionForm
    success_url = reverse_lazy('sections')


class SectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Section
    template_name = "section/delete_section.html"
    success_url = reverse_lazy('sections')


class VideoListView(LoginRequiredMixin, ListView):
    model = Video
    template_name = "video/video_list.html"
    context_object_name = 'videos'
    paginate_by = 4


class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    template_name = "video/add_video.html"
    form_class = VideoForm
    success_url = reverse_lazy('videos')


class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    template_name = "video/update_video.html"
    form_class = VideoForm
    success_url = reverse_lazy('videos')


class VideoDeleteView(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = "video/delete_video.html"
    success_url = reverse_lazy('videos')


class AddReviewView(LoginRequiredMixin, View):

    def post(self, request, slug):
        course = Course.objects.get(slug=slug)
        review_form = CourseReviewForm(data=request.POST)

        if review_form.is_valid():
            CourseReview.objects.create(
                course=course,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )

            return redirect(reverse("course_detail", kwargs={"slug": course.slug }))

        return render(request, "course/course_detail.html", {"course": course, "review_form": review_form})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, slug, review_id):
        course = Course.objects.get(slug=slug)
        review = course.coursereview_set.get(id=review_id)
        review_form = CourseReviewForm(instance=review)

        return render(request, "course/review_update.html", {"course": course, "review": review, 'review_form': review_form})

        
    def post(self, request, slug, review_id):
        course = Course.objects.get(slug=slug)
        review = course.coursereview_set.get(id=review_id)
        review_form = CourseReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("course_detail", kwargs={"slug": course.slug}))

        return render(request, "course/review_update.html", {"course": course, 'review': review, "review_form": review_form})


@login_required
def ReviewDeleteView(request, slug, review_id):
    course = Course.objects.get(slug=slug)
    review = course.coursereview_set.get(id=review_id)

    review.delete()
    return redirect(reverse("course_detail", kwargs={"slug": course.slug}))


class MyEnrolledCoursesListView(LoginRequiredMixin, ListView):
    model = Enroll
    template_name = "course/enrolled_courses.html"
    context_object_name = 'enrolls'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('course').filter(student=self.request.user)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrolled_students'] = Enroll.objects.filter(student__id=self.request.user.id).count()
        return context


@login_required
def MyEnrolledCourseDeleteView(request, slug, enroll_id):
    course = Course.objects.get(slug=slug)
    enroll = course.enroll_set.get(id=enroll_id)

    enroll.delete()

    return redirect(reverse("enrolled_courses"))


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "category/category_list.html"
    context_object_name = 'categories'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "category/add_category.html"
    form_class = CategoryForm
    success_url = reverse_lazy('categories')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "category/update_cat.html"
    form_class = CategoryForm
    success_url = reverse_lazy('categories')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "category/delete_cat.html"
    success_url = reverse_lazy('categories')


def searchView(request):
    query = request.GET.get("query", "")
    courses = Course.objects.filter(Q(name__icontains=query))

    context = {"query": query, "courses": courses}
    return render(request, "course/search.html", context)







































































