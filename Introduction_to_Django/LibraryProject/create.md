# Create a book
Book.objects.create(title=“1984”, author= “George Orwell”, publication_year=1949)

# Get all books
all_books = Book.objects.all()
print(all_books)  

# Output: <QuerySet [<Book: The Alchemist>]>
