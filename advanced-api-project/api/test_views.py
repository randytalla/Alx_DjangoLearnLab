from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book

class BookAPITestCase(APITestCase):
    """
    Test case for CRUD operations and filtering/searching on Book API.
    """

    def setUp(self):
        """Set up test data including a test user and some books."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
        self.book1 = Book.objects.create(title='Book One', author='Author A', publication_year=2020, owner=self.user)
        self.book2 = Book.objects.create(title='Book Two', author='Author B', publication_year=2021, owner=self.user)
        self.book3 = Book.objects.create(title='Another Book', author='Author C', publication_year=2022, owner=self.user)
        self.book_url = '/api/books/'

    def test_get_books_list(self):
        """Ensure we can retrieve a list of books."""
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_book(self):
        """Ensure an authenticated user can create a book."""
        data = {'title': 'New Book', 'author': 'Author D', 'publication_year': 2023}
        response = self.client.post(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_update_book(self):
        """Ensure a user can update their own book."""
        data = {'title': 'Updated Book'}
        response = self.client.patch(f'{self.book_url}{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book')

    def test_delete_book(self):
        """Ensure a user can delete their own book."""
        response = self.client.delete(f'{self.book_url}{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_filter_books_by_author(self):
        """Ensure filtering by author works."""
        response = self.client.get(self.book_url, {'author': 'Author A'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Author A')

    def test_search_books_by_title(self):
        """Ensure searching books by title works."""
        response = self.client.get(self.book_url, {'search': 'Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # Should return books with 'Book' in title

    def test_order_books_by_year(self):
        """Ensure ordering books by publication year works."""
        response = self.client.get(self.book_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))

    def test_permissions(self):
        """Ensure authentication is required for modifying books."""
        self.client.logout()
        response = self.client.post(self.book_url, {'title': 'Unauthorized Book', 'author': 'Hacker'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
