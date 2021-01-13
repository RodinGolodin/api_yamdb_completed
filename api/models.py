from django.db import models
from users.models import User


class Review(models.Model):
    pass


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'date published', 
        auto_now_add=True,
        blank=True
    )
    
    class Meta:
        ordering = ('-pub_date',)