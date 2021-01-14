from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.permissions import CustomPermission

from .models import Comment, Review
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(ModelViewSet):
    pass


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CustomPermission,)
    
    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
        return review.comments.all().order_by('id')
    