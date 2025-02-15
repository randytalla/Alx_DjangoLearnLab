# Delete the book
book = Book.objects.get(id=1)
book.delete()

# Check if the book was deleted
deleted_book = Book.objects.all()
print(deleted_book)  # Output: <QuerySet []>