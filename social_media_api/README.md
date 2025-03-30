#  Social Media API

A Django-based RESTful API that enables users to create posts, comment, follow other users, and interact with a dynamic social feed. This project is built using Django REST Framework (DRF) and supports authentication, CRUD operations, and real-time interactions.

##  Features

- **User Authentication**: Signup, login, and token-based authentication.
- **Posts & Comments**: Create, read, update, and delete posts and comments.
- **User Follow System**: Follow/unfollow users and view their posts in a personalized feed.
- **API Pagination & Filtering**: Optimize API responses with pagination and filtering.
- **Real-time Updates**: WebSockets (future enhancement) for real-time notifications.
- **Admin Dashboard**: Django admin interface for managing content.
- **Secure & Scalable**: Implemented best security practices with SSL, CSRF protection, and role-based permissions.

## Technologies Used

- **Backend**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL (or SQLite for development)
- **Authentication**: JWT (JSON Web Tokens) / Token-based authentication
- **Deployment**: PythonAnywhere (Live API)

##  Project Structure

social_media_api/ │── social_media_api/ │ │── settings.py │ │── urls.py │ │── wsgi.py │── users/ │ │── models.py │ │── views.py │ │── serializers.py │── posts/ │ │── models.py │ │── views.py │ │── serializers.py │── comments/ │ │── models.py │ │── views.py │ │── serializers.py │── requirements.txt │── README.md │── manage.py


##  Installation & Setup

### ** Clone the Repository**
```sh
git clone https://github.com/YOUR_USERNAME/social-media-api.git
cd social-media-api

Create a Virtual Environment & Install Dependencies
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

Configure Environment Variables
Create a .env file and add:
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url

Apply Migrations & Create a Superuser
python manage.py migrate
python manage.py createsuperuser

Run the Server
python manage.py runserver

API Endpoints
Method	Endpoint	Description
POST	/api/auth/signup/	Register a new user
POST	/api/auth/login/	Authenticate user
GET	/api/posts/	Get all posts
POST	/api/posts/	Create a new post
GET	/api/posts/{id}/	Get a single post
PUT	/api/posts/{id}/	Update a post
DELETE	/api/posts/{id}/	Delete a post
POST	/api/posts/{id}/comments/	Add a comment
POST	/api/users/{id}/follow/	Follow/unfollow a user

Deployment (PythonAnywhere)
Upload your project to PythonAnywhere.

Create a virtual environment and install dependencies.

Configure the web app settings in PythonAnywhere.

Set up the database and static files.

Restart the app and test the live API.

License
This project is licensed under the MIT License.


Live API: [Your PythonAnywhere URL]
Author: [Your Name]


---

### Next Steps:
- Replace `"YOUR_USERNAME"` with your GitHub username.
- Replace `"Your PythonAnywhere URL"` with the actual deployed link.

This `README.md` file provides a **clear** and **structured** guide for users and developers working on your Social Media API. Let me know if you want to add or modify anything! 
