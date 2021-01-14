from datetime import date
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import related
from users.models import User


class Genre(models.Model):
    pass


class Category(models.Model):
    pass


class Title(models.Model):
    name = models.CharField('Title', max_length=200,
                            help_text='Category name', null=True)
    year = models.SmallIntegerField(null=True)
    description = models.TextField(null=True)
    
    genre = models.ForeignKey(Genre, null=True,
                              on_delete=models.SET_NULL,
                              related_name='titles')
    category = models.ForeignKey(Category, null=True,
                              on_delete=models.SET_NULL,
                              related_name='titles')


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'date published', auto_now_add=True, blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        
    def __str__(self):
        return self.text


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
    
    def __str__(self):
        return self.text
