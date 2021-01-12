from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import get_email_code
from .serializers import CustomJWTSerializer


urlpatterns1 = [
    path('auth/email/', get_email_code),
    path('auth/token/', TokenObtainPairView.as_view(
        serializer_class=CustomJWTSerializer
    )
         )
]

urlpatterns = [
    path(
        'v1/',
        include(urlpatterns1),
    ),
]

