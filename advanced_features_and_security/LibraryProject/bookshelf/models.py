from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        permissions = [
            ("can_view_dashboard", "Can view admin dashboard"),
            ("can_manage_users", "Can manage user accounts"),
            ("can_edit_profile", "Can edit user profile"),
        ]

    def __str__(self):
        return self.email


# Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField(default=timezone.now)
    isbn = models.CharField(max_length=13, unique=True)  # Unique ISBN field
    summary = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='books_added')

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_publish_books", "Can publish books"),
            ("can_archive_books", "Can archive books"),
            ("can_edit_books", "Can edit book details"),
            ("can_create", "Can create new books"),
            ("can_delete", "Can delete books"),
        ]
        ordering = ['-published_date']
