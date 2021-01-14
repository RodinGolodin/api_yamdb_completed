from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.viewsets import ModelViewSet

from api.permissions import ReviewCommentPermission
from users.permissions import IsAdminOrReadOnly

from .models import Category, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          ReviewSerializer)


class GenreViewSet(ModelViewSet):
    pass


class TitleViewSet(ModelViewSet):
    pass


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentPermission]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentPermission]
    
    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
        return review.comments.all().order_by('id')
    
    def perform_create(self, serializer):
        get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user)


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
