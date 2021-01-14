from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .serializers import EmailAuthSerializer
from .views import UserViewSet, send_confirmation_code

router = DefaultRouter()

router.register(r'users', UserViewSet)
auth_patterns = [
    path(
        'email/',
        send_confirmation_code,
    ),
    path(
        'token/',
        TokenObtainPairView.as_view(serializer_class=EmailAuthSerializer),
        name='token_obtain_pair',
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
]

urlpatterns = [
    path(
        'v1/auth/',
        include(auth_patterns),
    ),
    path(
        'v1/',
        include(router.urls),
    ),
]
