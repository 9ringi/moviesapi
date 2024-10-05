from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)  # Use TMDB ID as the primary key
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    director = models.CharField(max_length=100, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_content = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
