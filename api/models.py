from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.fields import related

from users.models import User


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
    name = models.TextField('title', max_length=200,
                            null=True)
    year = models.IntegerField(null=True)
    description = models.CharField(max_length=200, null=True,
                                   blank=True)
    genre = models.ManyToManyField(Genre, blank=True, db_index=True,
                                   related_name='titles')
    category = models.ForeignKey(Category, null=True, 
                                 on_delete=models.SET_NULL,
                                 blank=True, related_name='titles')    

    def __str__(self):
        return self.name


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
