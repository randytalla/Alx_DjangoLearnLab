from django.urls import path
from . import views

urlpatterns = [
    # User Authentication URLs
    path('', views.home, name='home'),  # Home Page
    path('register/', views.register, name='register'),  # User Registration
    path('login/', views.user_login, name='login'),  # User Login
    path('logout/', views.user_logout, name='logout'),  # User Logout
    path('profile/', views.profile, name='profile'),  # User Profile

    # CRUD URLs for Blog Posts
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),  # Delete a post
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),  # Update a post
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),  # Create a new post

    # Comment URLs
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),  # Update a comment
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),  # Delete a comment
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),  # Create a new comment

    # Search URL
    path('search/', views.search, name='search'),  # Search results page

    # Tag filtering URL
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='tag-posts'),  # Posts filtered by tag
]
