from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Tag Model to define tags for blog posts
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Post Model for blog posts
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)  # Add the published_date field
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)  # Establish a many-to-many relationship with Tag

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

# Comment Model for blog comments
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)  # Link to the Post
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User who wrote the comment
    content = models.TextField()  # The content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the comment was last updated

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})
