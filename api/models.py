<<<<<<< HEAD
from django.db import models
from django.db.models import Avg
=======
import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
>>>>>>> 93331ef2ea761fce8c2e96f047661e3933ae8b4b

from users.models import User

now = datetime.datetime.now()


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
<<<<<<< HEAD
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
=======
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
>>>>>>> 93331ef2ea761fce8c2e96f047661e3933ae8b4b

    class Meta:
        ordering = ['-id']

    def update_rating(self):
        self.rating = self.review.all().aggregate(Avg('score'))['score__avg']
        self.save()


class Review(models.Model):
<<<<<<< HEAD
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
=======
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
>>>>>>> 93331ef2ea761fce8c2e96f047661e3933ae8b4b
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
<<<<<<< HEAD
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
=======
        'review date', auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date',]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('comment text', blank=False)
>>>>>>> 93331ef2ea761fce8c2e96f047661e3933ae8b4b
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
<<<<<<< HEAD
        auto_now_add=True,
    )
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    def __str__(self):
        return self.text
=======
        'comment date', 
        auto_now_add=True,
    )
    
    class Meta:
        ordering = ['-pub_date']
>>>>>>> 93331ef2ea761fce8c2e96f047661e3933ae8b4b
