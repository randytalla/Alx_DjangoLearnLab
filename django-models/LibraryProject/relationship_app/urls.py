from django.urls import path
from . import views  # Import views from the same directory
from .views import LibraryDetailView, list_books, add_book, edit_book, delete_book
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books


urlpatterns = [
    path('', views.home, name='home'),  # Home view
    path('books/', list_books, name='list_books'),  # List books
    path('register/', views.register_view, name='register'),  # Registration
    path('login/', views.login_view, name='login'),  # Custom Login View
    path('logout/', views.logout_view, name='logout'),  # Custom Logout View
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),

    # Authentication Views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Book Management
    path('add_book/', add_book, name='add_book'),  # Add book
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),  # Edit book
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),  # Delete book

    # Library Detail View
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
