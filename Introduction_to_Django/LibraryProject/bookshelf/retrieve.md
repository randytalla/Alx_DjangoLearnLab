# Retrieve all books from the database
all_books = Book.objects.all()
print(all_books)  
# Output: <QuerySet [<Book: “1984”>]>