from django import views
from django.urls import path
from .views import list_books  # ✅ Import the function-based view
from .views import LibraryDetailView  
from .views import user_login, user_logout, register
from django.contrib.auth.views import LoginView, LogoutView, RegisterView


urlpatterns = [
    path('books/', list_books, name='list-books'),# ✅ Add route for the books list
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path("register/", views.register, name="register"),  # User Registration
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),  # User Login
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),  # User Logout  # Built-in logout
]
