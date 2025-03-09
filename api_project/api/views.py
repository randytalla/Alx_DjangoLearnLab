from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly  # Import the custom permission

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing, creating, updating, and deleting books.
    - Read: Anyone can access (GET requests)
    - Write: Only Admin users can create, update, or delete
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]  # Apply custom permission

class BookList(generics.ListAPIView):
    """
    A ListAPIView for retrieving a list of books.
    Only authenticated users can access it.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can see the list