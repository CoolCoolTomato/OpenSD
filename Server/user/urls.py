from .views import CustomTokenObtainPairView, UserRegistrationView, CustomTokenRefreshView, logout_view, \
    current_user_view
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name='token_obtain_pair'),
    path('logout/', logout_view, name='logout'),
    path('getuser/', current_user_view, name='current-user'),
]
