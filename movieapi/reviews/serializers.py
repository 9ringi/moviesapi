from rest_framework import serializers
from .models import Movie, Review
from .utils import get_movie_details_by_title

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title']

class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(write_only=True, required=True)
    movie_description = serializers.CharField(source='movie.description', read_only=True)
    movie_director = serializers.CharField(source='movie.director', read_only=True)
    movie_date = serializers.DateField(source='movie.release_date', read_only=True)
    movie_title_output = serializers.CharField(source='movie.title', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    rating = serializers.IntegerField(min_value=1, max_value=5, required=True)
    review_content = serializers.CharField(required=True)

    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'movie_title_output', 'movie_description', 'movie_director', 'movie_date', 'review_content', 'rating', 'user_id', 'created_date']

    def create(self, validated_data):
        movie_title = validated_data.pop('movie_title')
        movie_details = get_movie_details_by_title(movie_title)
        if not movie_details:
            raise serializers.ValidationError("Movie not found in TMDB.")
        
        movie, created = Movie.objects.get_or_create(
            id=movie_details['id'],
            defaults={
                'title': movie_details['title'],
                'description': movie_details['overview'],
                'director': movie_details.get('director', ''),
                'release_date': movie_details.get('release_date')
            }
        )
        review = Review.objects.create(movie=movie, **validated_data)
        return review
