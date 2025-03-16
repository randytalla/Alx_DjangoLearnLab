from django_filters import rest_framework as filters  # Added missing import
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, filters  # Added filters.OrderingFilter import
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly  # Custom permission

class BookListView(generics.ListAPIView):
    """
    Retrieves a list of all books.
    Allows GET requests only.
    Supports filtering, searching, and ordering.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single book by ID.
    Allows GET requests only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    Creates a new book entry.
    Requires authentication.
    Allows POST requests.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom logic to validate and create a book.
        Ensures that book title is unique and the publication year is valid.
        """
        title = serializer.validated_data.get('title')
        publication_year = serializer.validated_data.get('publication_year')

        if Book.objects.filter(title=title).exists():
            raise ValidationError({'title': 'A book with this title already exists.'})

        if publication_year > 2024:
            raise ValidationError({'publication_year': 'Publication year cannot be in the future.'})

        serializer.save(owner=self.request.user)

class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing book entry.
    Requires authentication.
    Only the book owner can update.
    Allows PUT and PATCH requests.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        """
        Custom logic to validate and update a book.
        Ensures that title remains unique and the publication year is valid.
        """
        title = serializer.validated_data.get('title', None)
        publication_year = serializer.validated_data.get('publication_year', None)
        instance = self.get_object()

        if title and Book.objects.exclude(pk=instance.pk).filter(title=title).exists():
            raise ValidationError({'title': 'A book with this title already exists.'})

        if publication_year and publication_year > 2024:
            raise ValidationError({'publication_year': 'Publication year cannot be in the future.'})

        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes an existing book entry.
    Requires authentication.
    Only the book owner can delete.
    Allows DELETE requests.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
