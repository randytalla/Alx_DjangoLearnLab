from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)  # ✅ Correct syntax
    content = models.TextField()  # ✅ Correct syntax
    published_date = models.DateTimeField(auto_now_add=True)  # ✅ Correct syntax
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # ✅ Correct syntax

    def __str__(self):
        return self.title  # String representation of the Post
