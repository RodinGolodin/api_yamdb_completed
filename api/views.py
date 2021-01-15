from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import ReviewCommentPermission
from users.permissions import IsAdminOrReadOnly

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleWriteSerializer
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    search_fields = ('name', 'year')

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleWriteSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.rating = instance.reviews.all().aggregate(Avg('score'))['score__avg']
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Category view class. Allowed only GET, POST and DELETE methods.
    Search by slug field is possible.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    