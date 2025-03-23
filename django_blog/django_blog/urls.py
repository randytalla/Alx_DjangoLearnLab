from django.contrib import admin
from django.urls import path, include
from blog import views  # Import your blog views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Home Page (Redirect to the home view of the blog)
    path('', views.home, name='home'),

    # User Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),  # Use your custom login view
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Include blog app URLs
    path('blog/', include('blog.urls')),  # This line will include the 'blog' app's URLs

    # Password reset and change URLs (using Django's built-in views)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
