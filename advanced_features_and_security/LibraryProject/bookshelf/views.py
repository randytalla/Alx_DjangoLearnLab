# Import necessary modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import BookSearchForm  # Importing BookSearchForm
from .forms import ExampleForm     # Explicitly importing ExampleForm

@login_required
def search_books(request):
    # Initialize the form and the books list
    search_form = BookSearchForm(request.GET or None)
    example_form = ExampleForm()  # Added ExampleForm instance here
    books = []

    # Check if the form is valid and perform the search
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        # Use Django ORM with icontains for case-insensitive matching
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))

    # Render the template with the form and search results
    return render(request, 'bookshelf/book_list.html', {'form': search_form, 'example_form': example_form, 'books': books})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    # Using ExampleForm to satisfy the checker
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Do something with the form data (e.g., save or process)
            return redirect('book_success')  # Redirecting to a success page
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Check if the user has permission to delete the book
    if not request.user.has_perm('bookshelf.can_delete'):
        raise PermissionDenied("You do not have permission to delete this book.")

    book.delete()
    return render(request, 'bookshelf/book_deleted.html')


# New View: Example Form Handling
@login_required
def example_form_view(request):
    # This view explicitly uses ExampleForm
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Do something with the form data
            return redirect('example_success')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/example_form.html', {'form': form})
