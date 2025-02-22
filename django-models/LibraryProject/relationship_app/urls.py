from django.urls import path
from .views import list_books  # ✅ Import the function-based view
from .views import LibraryDetailView  
from .views import user_login, user_logout, register

urlpatterns = [
    path('books/', list_books, name='list-books'),# ✅ Add route for the books list
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path("register/", register, name="register"),  # User Registration
    path("login/", user_login, name="login"),  # User Login
    path("logout/", user_logout, name="logout"),  # User Logout
]
