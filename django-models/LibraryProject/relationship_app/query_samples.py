import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")  # Change 'myproject' to your actual project name
django.setup()

# Import the models
from relationship_app.models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author using filter()
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)  # ✅ Using objects.filter(author=author) as required
        print(f"Books written by {author_name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")

# 2️⃣ List all books in a specific library
def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # ✅ This remains unchanged
        print(f"Books available in {library_name}:")
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")

# 3️⃣ Retrieve the librarian for a specific library using Librarian.objects.get()
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # ✅ Using objects.get(library=library) as required
        print(f"The librarian for {library_name} is {librarian.name}.")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")

# Run sample queries
if __name__ == "__main__":
    get_books_by_author("J.K. Rowling")  # Example author
    list_books_in_library("Yaoundé Central Library")  # Example library
    get_librarian_for_library("Yaoundé Central Library")  # Example library
