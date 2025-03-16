# Advanced API Project

This project is built using Django REST Framework to demonstrate CRUD operations with Books.

## API Endpoints

### Book Endpoints
- `GET /api/books/` → Retrieves all books.
- `GET /api/books/<int:pk>/` → Retrieves a book by ID.
- `POST /api/books/create/` → Adds a book (**Authenticated Users Only**).
- `PUT /api/books/<int:pk>/update/` → Updates a book (**Only Owner**).
- `DELETE /api/books/<int:pk>/delete/` → Deletes a book (**Only Owner**).

## Authentication
- Uses Django’s built-in authentication.
- Permissions enforce that only authenticated users can modify data.

## Features
- Uses Django Generic Views (`ListAPIView`, `RetrieveAPIView`, etc.).
- Implements **permissions** to protect the API.
- Supports **searching** books by `publication_year`.
