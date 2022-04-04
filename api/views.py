from urllib import request
from django.urls import reverse_lazy
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView


from course.models import Category, Course, Enroll, CourseReview, Video, Section
from cart.cart import Cart
from users.models import Teacher, CustomUser
from .permissions import IsTeacher, IsPaid, IsStudent
from .serializers import (
    CategorySerializer, CourseDetailSerializer, CourseReviewSerializer, CourseSerializer, StudentCourseSerializer, StudentRegistrationSerializer, TeacherSerializer, WatchCourseSerializer,
    SectionSerializer, VideoSerializer, AdminCourseSerializer, MyCourseSerializer, TeacherCourseSerializer,
    UserLoginSerializer, TeacherRegistrationSerializer, StudentRegistrationSerializer, StudentSerializer,
    TeacherApproveSerializer, ProfileSerializer
    )



@api_view(['GET', 'POST'])
@permission_classes((IsTeacher, ))
def category_list(request):

    if request.method == 'GET':
        categories = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsTeacher, ))
def category_detail(request, slug):

    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsTeacher, ))
def video_list(request):

    if request.method == 'GET':
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsTeacher, ))
def video_detail(request, pk):

    try:
        video = Video.objects.get(pk=pk)
    except Video.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VideoSerializer(video)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsTeacher, ))
def section_list(request):

    if request.method == 'GET':
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsTeacher, ))
def section_detail(request, pk):

    try:
        section = Section.objects.get(pk=pk)
    except Section.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SectionSerializer(section)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SectionSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def course_list(request):

    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsTeacher,))
def course_create(request):

    if request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user.is_teacher)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def enrolled_courses(request):

    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_teacher:
            courses = Course.objects.filter(teacher__pk=request.user.pk)
        if request.user.is_authenticated and request.user.is_student:
            courses = Course.objects.filter(enroll__student=request.user)

        serializer = MyCourseSerializer(courses, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated, IsStudent))
def delete_enrolled_courses(request, slug, enroll_id):
    if request.method == 'DELETE':
        course = Course.objects.get(slug=slug)
        enroll = course.enroll_set.get(id=enroll_id)

        enroll.delete()

    return Response(status=status.HTTP_200_OK)


class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]        


    def get_serializer_context(self):
        context = super(CourseDetail, self).get_serializer_context()
        course = self.get_object()
        student_for_every_course =  Enroll.objects.filter(course__slug=self.kwargs["slug"]).count()
        teacher_courses = Course.objects.filter(teacher__pk=self.request.user.pk).count()
        is_enrolled = False
        is_paid = False
        is_in_cart = False

        if self.request.user.is_authenticated:
            if Enroll.objects.filter(course=course, student=self.request.user).exists():
                is_enrolled = True
                is_paid = True
            else:
                cart = Cart(self.request)
                is_in_cart = cart.has_course(course)

        else:
            cart = Cart(self.request)
            is_in_cart = cart.has_course(course)
        
                    
        context.update({
            "request": self.request, 'student_for_every_course': student_for_every_course,
            'teacher_courses':teacher_courses, 'is_enrolled': is_enrolled, 'is_paid': is_paid,
            'is_in_cart':is_in_cart
        })
        
        return context
    

class WatchCourse(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = WatchCourseSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsPaid]     


    def get_serializer_context(self):
        context = super(WatchCourse, self).get_serializer_context()
        course = self.get_object()
        videos = Video.objects.all()
        is_paid = False


        if self.request.user.is_authenticated:
            if Enroll.objects.filter(course=course, student=self.request.user).exists():
                is_paid=True
            else:
                is_paid=False


        context.update({'is_paid': is_paid, 'videos': videos})
        return context


class StudentDashboard(APIView):

    permission_classes = [IsStudent]     

    def get(self, request):
        courses = Course.objects.filter(enroll__student__pk=self.request.user.pk)
        serializer = StudentCourseSerializer(courses, many=True)
        return Response(serializer.data)


class TeacherDashboard(APIView):

    permission_classes = [IsTeacher]

    def get(self, request):
        courses = Course.objects.filter(teacher__pk=self.request.user.pk)
        serializer = TeacherCourseSerializer(courses, many=True)

        
        response = {
            'status_code': status.HTTP_200_OK,
            'data': serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class AdminDashboard(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        courses = Course.objects.all()
        serializer = AdminCourseSerializer(courses, many=True)

        
        response = {
            'status_code': status.HTTP_200_OK,
            'data': serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class CourseReviewList(APIView):

    def get(self, request):
        reviews= CourseReview.objects.all()
        serializer = CourseReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class CourseReviewCreate(APIView):
    def post(self, request, slug):
        comment = request.POST.get('comment')
        stars_given = request.POST.get('stars_given')

        CourseReview.objects.create(
            user=self.request.user, 
            course=Course.objects.get(slug=slug),
            comment=comment,
            stars_given=stars_given
            )

        return Response('Successfully Created!')


class CourseReviewDetail(APIView):

    def get(self, request, pk):
        review = CourseReview.objects.get(id=pk)
        serializer = CourseReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = request.POST.get('comment')
        stars_given = request.POST.get('stars_given')
        review = CourseReview.objects.get(id=pk)


        review.course = Course.objects.get(id=pk)
        review.stars_given = stars_given
        review.comment = comment
        review.user = CustomUser.objects.get(id=pk)
        review.save()

        return Response('Successfully Updated!')


    def delete(self, request, pk):
        review = CourseReview.objects.get(id=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherRegistrationView(APIView):
    serializer_class = TeacherRegistrationSerializer


    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:

            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Teacher successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


class StudentRegistrationView(APIView):
    serializer_class = StudentRegistrationSerializer

    def get(self, request):
        students = CustomUser.objects.filter(is_student=True, is_active=True)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'username': serializer.data['username'],
                    'is_teacher': serializer.data['is_teacher'],
                    'is_student': serializer.data['is_student']
                }
            }

            return Response(response, status=status_code)


class UnapprovedTeachersListView(APIView):

    def get(self, request):
        teachers = CustomUser.objects.filter(is_active=False, is_teacher=False)
        serializer = TeacherApproveSerializer(teachers, many=True)
        return Response(serializer.data)
    

class ApproveTeachersView(APIView):

    def post(self, request, pk):
        teacher = CustomUser.objects.get(id=pk)
        teacher.is_active = True
        teacher.is_teacher = True

        teacher.save()

        return Response('Successfully Approved!')


class RejectTeachersView(APIView):
    
    def post(self, request, pk):
        teacher = CustomUser.objects.get(id=pk)
        teacher.delete()

        return Response('Successfully Rejected!')

   
class ProfileView(APIView):

    def get(self, request, pk):
        pk = self.request.user.pk
        user = CustomUser.objects.get(id=pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)












































































    