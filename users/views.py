from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.generics import get_object_or_404
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, \
    AuthSerializer, UsersSerializer
from .models import User
from django.core.mail import send_mail
from api_yamdb import settings
import random
from rest_framework.pagination import BasePagination
from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        user = self.request.user
        serialized_user = UserSerializer(user).data
        return User.objects.filter(user=serialized_user)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    pagination_class = BasePagination
    queryset = User.objects.all()


class AuthViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AuthSerializer

    def get_email_code(self):
        if self.request.method == 'POST':
            email = self.request.POST['email']
            chars = (
                'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNO'
                'PQRSTUVWXYZ1234567890'
            )
            for n in range(1):
                password = ''
                for i in range(18):
                    password += random.choice(chars)
                send_mail(
                    'Password',
                    password,
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                )


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
