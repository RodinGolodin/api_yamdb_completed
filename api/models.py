from django.db import models
from django.db.models import Avg

from users.models import User


class Genre(models.Model):
    name = models.CharField(
        max_length=25,
    )
    slug = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=25,
    )
    slug = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name
    

class Title(models.Model):
    name = models.TextField(
        'title',
        max_length=200,
        null=True,
    )
    year = models.IntegerField(
        null=True,
    )
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='titles',
    )

    def __str__(self):
        return self.name

    def update_rating(self):
        self.rating = self.review.all().aggregate(Avg('score'))['score__avg']
        self.save()


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    def __str__(self):
        return self.text
