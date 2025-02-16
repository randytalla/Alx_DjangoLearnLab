from django.contrib import admin
from .models import Book

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns to display
    list_filter = ('publication_year',)  # Sidebar filter by publication year
    search_fields = ('title', 'author')  # Enables search by title & author

admin.site.register(Book, BookAdmin)