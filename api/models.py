from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=300)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=300)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField(null=True, blank=True)
    description = models.CharField(max_length=400, blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.name
    
    @property
    def rating(self):
        reviews = self.reviews.all()
        score_avg = reviews.aggregate(models.Avg('score')).get('score__avg')
        return None if score_avg is None else int(score_avg)


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
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.title}, {self.score}, {self.author}'


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
        db_index=True
    )

    def __str__(self):
        return f'{self.author}, {self.pub_date:%d.%m.%Y}, {self.text[:50]}'
