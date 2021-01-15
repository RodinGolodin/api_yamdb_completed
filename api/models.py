import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

now = datetime.datetime.now()


class Genre(models.Model):
    name = models.CharField(max_length=25)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=25)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(db_index=True, max_length=100)
    year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(int(now.year))],
        default=None
    )
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='genres', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='categories',
        blank=True,
        null=True
    )
    rating = models.IntegerField(null=True, default=None)

    class Meta:
        ordering = ['-id']


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(blank=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'review score',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'review date', auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date', ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('comment text', blank=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'comment date',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
