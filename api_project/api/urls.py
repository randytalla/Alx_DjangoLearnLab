from .views import BookList
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# ✅ Step 1: Create a router
router = DefaultRouter()

# ✅ Step 2: Register the BookViewSet with the router
router.register(r'books_all', BookViewSet, basename='book_all')

# ✅ Step 3: Include the router's URLs
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),  # This will generate all book-related URLs automatically
]
