from rest_framework import viewsets, permissions, status, filters, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.core import exceptions
from api.models import User
from .serializers import UserSerializer, TokenSerializer, SignUpSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsAdmin
import uuid


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)


class EmailSignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            confirmation_code = uuid.uuid4()
            User.objects.create(
                email=email, username=str(email),
                confirmation_code=confirmation_code, is_active=False
            )
            send_mail(
                'Account verification',
                'Your activation key {}'.format(confirmation_code),
                DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            return Response(
                {'result': 'A confirmation code has been sent to your email'},
                status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(
                email=serializer.data['email'],
                confirmation_code=serializer.data['confirmation_code']
            )
        except exceptions.ValidationError:
            return Response(
                data={'detail': 'Invalid email or code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user.is_active = True
            user.save()
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh_token.access_token)
            })
