from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsOwnerOrReadOnly

from .models import Review, Genre, Category, Title
from .serializers import CommentSerializer, ReviewSerializer


class GenreViewSet(ModelViewSet):
    pass


class CategoryViewSet(ModelViewSet):
    pass


class TitleViewSet(ModelViewSet):
    pass


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
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