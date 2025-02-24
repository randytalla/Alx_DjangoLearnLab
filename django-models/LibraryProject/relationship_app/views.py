from django.contrib.auth import authenticate, login, logout  # Authentication functions
from django.contrib.auth.forms import UserCreationForm  # Form for user registration
from django.contrib.auth.decorators import user_passes_test, login_required  # Access control decorators
from django.contrib.auth.decorators import permission_required  # Specifically added this line

from django.shortcuts import render, redirect, get_object_or_404  # View utilities
from django.contrib import messages  # Flash messages for user feedback
from django.core.exceptions import ObjectDoesNotExist  # Exception handling
from django.views.generic.detail import DetailView

from Introduction_to_Django.LibraryProject.bookshelf import models  # Class-based detail view

from .models import UserProfile, Book, Library  # Importing necessary models
from .forms import BookForm  # Form for adding and editing books
from .models import Library
from django.contrib.auth import login









# Role Check Functions
def is_admin(user):
    if user.is_authenticated:
        try:
            return user.userprofile.role == 'Admin'
        except ObjectDoesNotExist:
            return False
    return False

def is_librarian(user):
    if user.is_authenticated:
        try:
            return user.userprofile.role == 'Librarian'
        except ObjectDoesNotExist:
            return False
    return False

def is_member(user):
    if user.is_authenticated:
        try:
            return user.userprofile.role == 'Member'
        except ObjectDoesNotExist:
            return False
    return False

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'relationship_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# Registration View
def register_view(request):
    return render(request, 'relationship_app/register.html')

# Book List View
def list_books(request):
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Home View
def home(request):
    return render(request, 'relationship_app/home.html')

# Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Admin View
@user_passes_test(is_admin, login_url='login')
@login_required
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian View
@user_passes_test(is_librarian, login_url='login')
@login_required
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    established_date = models.DateField()

    def __str__(self):
        return self.name

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Member View
@user_passes_test(is_member, login_url='login')
@login_required
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# Add Book View (Requires can_add_book permission)
@permission_required('relationship_app.can_add_book', login_url='login')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

# Edit Book View (Requires can_change_book permission)
@permission_required('relationship_app.can_change_book', login_url='login')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

# Delete Book View (Requires can_delete_book permission)
@permission_required('relationship_app.can_delete_book', login_url='login')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

# Library Detail View
def library_detail(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    books = library.books.all()  # Get all books in the library
    return render(request, 'relationship_app/library_detail.html', {'library': library, 'books': books})
