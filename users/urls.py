from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CodeConfirmView, EmailSignUpView, UserViewSet

router = DefaultRouter()


router.register(r'users', UserViewSet)

auth_patterns = [
    path(
        'email/',
        EmailSignUpView.as_view()
    ),
    path(
        'token/',
        CodeConfirmView.as_view(),
        name='token_obtain_pair',
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
