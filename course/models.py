from decimal import Decimal
from django.db import models
from users.models import CustomUser, Teacher
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from .helpers import get_timer



COURSE_LEVEL = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard')
)


class Category(models.Model):
    title = models.CharField(max_length=25)
    slug = models.SlugField(max_length=150, unique=True)


    class Meta:
        ordering = ["title"]
        verbose_name = "category"
        verbose_name_plural = "categories"   


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    section = models.ManyToManyField("Section")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    video_link = models.CharField(max_length=1000, null=True, blank=True)
    difficulty = models.CharField(choices=COURSE_LEVEL, default='Easy', max_length=50)
    requirements = models.CharField(max_length=250, default='Nothing required')
    to_whom = models.CharField(max_length=250, default='For Everyone')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)


    def get_rating(self):
        total = sum(int(review['stars_given']) for review in self.coursereview_set.all().values())

        if self.coursereview_set.all().count() > 0:
            return total / self.coursereview_set.all().count()
        else:
            return 0
    
    def get_number_of_rating(self):
        total = sum(int(review['stars_given']) for review in self.coursereview_set.all().values())

        if self.coursereview_set.all().count() > 0:
            return self.coursereview_set.all().count()
        else:
            return 0

    def get_total_lectures(self):
        videos = 0
        for section in self.section.all():
            videos += len(section.video.all())
        return videos


    def total_course_length(self):
        length = Decimal(0.0)
        for sec in self.section.all():
            for video in sec.video.all():
                length += video.length

        return get_timer(length, type='short')


    def get_completed_course(self):
        total = Course.objects.filter(customuser=self.is_completed).count()
        return total


class Section(models.Model):
    name = models.CharField(max_length=250)
    video = models.ManyToManyField("Video")

    def __str__(self):
        return self.name


    def total_length(self):
        total = Decimal(0.0)

        for vid in self.video.all():
            total += vid.length

        return get_timer(total, type='min')


class Video(models.Model): 
    name = models.CharField(max_length=250)
    files = models.FileField(upload_to='course_videos', blank=True)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(max_length=1000, blank=True)


    def __str__(self):
        return self.name


    # def get_video_length(self):
    #     try:
    #         video = mp4(self.files)
    #         return video.info.length
    #     except mp4.MP4StreamInfoError:
    #         return 0.0



    def get_video_length_time(self):
        return get_timer(self.length)


    # def get_absolute_url(self):
    #     return 'http://localhost:8000'+self.files


    # def save(self, *args, **kwargs):
    #     self.length = self.get_video_length()
    #     return super().save(*args, **kwargs)  


class CourseReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stars_given} stars for {self.course.name} by {self.user.username}"

    
class Enroll(models.Model):

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    
    def __str__(self):
        return f'{self.course.name} by {self.course.teacher}'
    


    def get_std_num_for_every_course(self, slug):
        stds = Enroll.objects.filter(course__slug=self.slug).count()
        return stds





# def send_notification_to_admin(sender, instance, created, **kwargs):
#     admin_email = 'developer.abdullaev@gmail.com'
#     if created:
#         message = "I want to teach on Educative"
#         subject = "Teaching on Educative"
#         send_mail(subject, message, admin_email, [instance.email])

# post_save.connect(send_notification_to_admin, sender=Teacher)














