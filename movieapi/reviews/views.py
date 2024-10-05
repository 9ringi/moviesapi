from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer


class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ReviewFilter(filters.FilterSet):
    movie_title = filters.CharFilter(field_name='movie__title', lookup_expr='icontains')
    rating = filters.NumberFilter(field_name='rating', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['movie_title', 'rating']

class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,  OrderingFilter)
    filterset_class = ReviewFilter
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['rating', 'created_date']
    ordering = ['-created_date']  # Default ordering

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to perform this action.")
        return obj