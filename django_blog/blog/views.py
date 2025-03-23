from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Post, Tag, Comment  # Import Comment model
from .forms import UserRegisterForm, PostForm
from django.contrib.auth.forms import UserChangeForm
from django.db.models import Q  # Import Q for complex queries

# Home View
def home(request):
    return render(request, 'blog/home.html')

# User Authentication Views
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}.')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Redirect to 'next' if provided
            next_url = request.GET.get('next') or request.POST.get('next') or 'profile'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'blog/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

# Profile View (Handles Profile Updates)
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'blog/profile.html', {'user': request.user, 'form': form})

# CRUD Views for Blog Posts

# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

# View a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# Create a new post (Only authenticated users)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

# Update an existing post (Only author can edit)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    # Redirect unauthenticated users or users who are not authors
    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to edit this post.')
        return redirect('post-list')

# Delete a post (Only author can delete)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

    # Redirect unauthenticated users or users who are not authors
    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to delete this post.')
        return redirect('post-list')

# Comment CRUD Views

# Create a new comment
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})

# Update an existing comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.get_object().post.pk})

# Delete a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.get_object().post.pk})

# Search Functionality
def search(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(tags__name__icontains=query)
        ).distinct()  # Ensure unique posts if they appear under multiple tags
    else:
        posts = Post.objects.all()

    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

# Tag Filtering Functionality
def tag_posts(request, tag_name):
    # Find the tag by name
    tag = Tag.objects.filter(name=tag_name).first()

    # If the tag exists, filter posts by that tag
    if tag:
        posts = Post.objects.filter(tags=tag)
    else:
        posts = Post.objects.none()  # If no posts match the tag, return an empty queryset

    return render(request, 'blog/tag_posts.html', {'posts': posts, 'tag_name': tag_name})
