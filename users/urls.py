from .views import UserViewSet, UsersViewSet
from rest_framework import routers
from .views import AuthViewSet, EmailTokenObtainPairView
from django.urls import path, include

router = routers.DefaultRouter()

router.register('users', UsersViewSet, basename='users')
router.register(r'users/me', UserViewSet, basename='user')
router.register(r'auth/email', AuthViewSet, basename='auth')
urlpatterns = [
    path(
        'v1/',
        include(router.urls),
    ),
]

urlpatterns += [
    path('v1/auth/token/', EmailTokenObtainPairView.as_view())
]