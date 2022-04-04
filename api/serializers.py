from rest_framework import serializers
from users.models import Teacher, CustomUser
from course.models import Course, Section, Video, Category, CourseReview, Enroll
from rest_framework_simplejwt.tokens import RefreshToken


class StudentRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        
        fields = ('pk', 'first_name','last_name','email', 'username','password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_student = True
        user.is_active = True
        user.save()
        return user
        

class TeacherRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('pk', 'first_name','last_name','email', 'username','password', 'is_teacher', 'is_active')
        read_only_fields = ['is_teacher', 'is_active']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_student = False
        user.is_active = False
        teacher = Teacher.objects.create(user=user)
        teacher.save()
        user.save()
        return user

    
class UserLoginSerializer(serializers.ModelSerializer):

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username,
                'is_teacher': is_teacher,
                'is_student': is_student
            }

            return validation
        except AuthUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

        
class TeacherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name', read_only=True)
    profile_picture = serializers.FileField(source='profile_pic')

    class Meta:
        model = Teacher
        fields = ['pk','name', 'profile_picture']


class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['pk','name', 'profile_picture', 'is_student']
        read_onyl_fields = ['is_student']


class VideoSerializer(serializers.ModelSerializer):
    video_duration = serializers.CharField(source='get_video_length_time')


    class Meta:
        model = Video
        fields = ['name', 'link', 'video_duration']


class SectionSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True, many=True)


    class Meta:
        model = Section
        fields = ['name', 'video']


class ReviewUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = CustomUser
        fields = ['full_name']
   

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'price']


class CourseReviewSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer(read_only=True)
    

    class Meta:
        model = CourseReview
        fields = ['id', 'user', 'comment', 'stars_given']


class CourseDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    overall_rating = serializers.CharField(source='get_rating', read_only=True)
    ratings = serializers.IntegerField(source='get_number_of_rating', read_only=True)
    lectures = serializers.IntegerField(source='get_total_lectures', read_only=True)
    duration = serializers.CharField(source='total_course_length', read_only=True)
    section = serializers.StringRelatedField(many=True, read_only=True)
    teacher_course_count = serializers.SerializerMethodField('teacher_course')
    numbers_of_students_in_each_course = serializers.SerializerMethodField("student_numbers_in_each_course")
    is_enrolled = serializers.SerializerMethodField('enrolled')
    is_paid = serializers.SerializerMethodField('paid')
    is_in_cart =  serializers.SerializerMethodField('in_cart')
    coursereview_set = CourseReviewSerializer(read_only=True, many=True)



    def student_numbers_in_each_course(self, obj):
        return self.context['student_for_every_course']

    def teacher_course(self, obj):
        return self.context['teacher_courses']

    def enrolled(self, obj):
        return self.context['is_enrolled']

    def paid(self, obj):
        return self.context['is_paid']

    def in_cart(self, obj):
        return self.context['is_in_cart']   

       

    class Meta:
        model = Course
        fields = [
            'id','category', 'section', 'teacher', 'name', 'description', 'image', 'price', 'video_link', 
            'difficulty', 'requirements', 'to_whom', 'updated', 'learning_goal','overall_rating', 'ratings',
            'lectures', 'duration', 'teacher_course_count', 'numbers_of_students_in_each_course', 'is_enrolled',
            'is_paid', 'is_in_cart', 'coursereview_set'
        ]
        

class MyCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'image']


class WatchCourseSerializer(serializers.ModelSerializer):
    duration = serializers.CharField(source='total_course_length', read_only=True)
    section = SectionSerializer(many=True)
    is_paid = serializers.SerializerMethodField('paid')

    def paid(self, obj):
        return self.context['is_paid']


    class Meta:
        model = Course
        fields = [
            'id', 'name', 'section',  'duration', 'is_paid'
        ]


class StudentCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name']


class TeacherCourseSerializer(serializers.ModelSerializer):
    students_in_each_course = serializers.CharField(source="course_student")
    

    class Meta:
        model = Course
        fields = ['id', 'name', 'students_in_each_course']


class AdminCourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    students_in_each_course = serializers.CharField(source="course_student")
    all_students = serializers.CharField(source="total_students")
        

    class Meta:
        model = Course
        fields = ['id', 'teacher', 'name', 'students_in_each_course', 'all_students']


class EnrollSerializer(serializers.ModelSerializer):
    student = StudentCourseSerializer(read_only=True, many=True)
    course = CourseSerializer(many=True)

    
    class Meta:
        model = Enroll
        fields = ['student', 'course', 'is_paid']


class TeacherApproveSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    
    
    class Meta:
        model = Teacher
        fields = ['teacher']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['pk', 'first_name', 'last_name', 'username', 'email', 'profile_picture']














































