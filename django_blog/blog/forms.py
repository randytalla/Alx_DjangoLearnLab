from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple  # Importing CheckboxSelectMultiple widget directly from widgets module
from .models import Post, Tag, Comment  # Import Comment model

# Custom TagWidget (optional, depends on your needs)
class TagWidget(CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'custom-tag-widget'})  # You can add custom classes or attributes if needed

# User Registration Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Post Form (For Creating and Editing Posts)
class PostForm(forms.ModelForm):
    # Add a field for selecting tags using the custom TagWidget
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('name'),  # Sort tags alphabetically
        required=False,  # Allow posts without tags
        widget=TagWidget(),  # Use the custom TagWidget for tag selection
        label="Select Tags"
    )

    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the title of the post'}),
        label='Post Title'
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write the content of your post here'}),
        label='Post Content'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Include the 'tags' field

# Comment Form (For Creating and Editing Comments)
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your comment here', 'rows': 3}),
        label='Comment'
    )

    class Meta:
        model = Comment
        fields = ['content']  # Only include the 'content' field for comments
