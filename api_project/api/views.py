from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

# ✅ View to list all books (Only for GET request)
class BookList(ListAPIView):
    queryset = Book.objects.all() # Get all books from the database
    serializer_class = BookSerializer # Serialize the books into JSON format

# ✅ ViewSet to handle full CRUD (Create, Retrieve, Update, Delete)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
