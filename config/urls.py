from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [

    path('auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),

    path('mine/', admin.site.urls),
    path('', include('course.urls')),
    path('', include('cart.urls')),
    
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)