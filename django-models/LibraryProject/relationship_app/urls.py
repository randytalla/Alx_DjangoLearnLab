from django.urls import path
from .views import list_books  # ✅ Import the function-based view
from .views import LibraryDetailView  

urlpatterns = [
    path('books/', list_books, name='list-books'),# ✅ Add route for the books list
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]
